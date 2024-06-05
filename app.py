from flask import Flask, request, jsonify
import urllib.request
import requests
import os,fitz, re
import numpy as np
import tensorflow_hub as hub
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

book_links = {
    1: {
        "Cal1": "http://example.com/book/AD_semester1",
        "DM": "http://example.com/book/Math_semester1",
        "ICP": "http://example.com/book/Math_semester1",
        "PME1": "http://example.com/book/Math_semester1",
        "UPEM": "upem.pdf",
    },
    2: {
        "Cal2": "https://drive.google.com/file/d/1SdSV3Og8OQ11gV-NFWcEZ_ds0igjQtKN/view?usp=sharing",
        "DSA": "http://example.com/book/Math_semester2",
        "IGT": "igt.pdf",
        "PME2": "pme.pdf",
        "UPS2": "http://example.com/book/Math_semester2"
    },
    3: {
        "ALA1": "http://example.com/book/AD_semester2",
        "CSW1": "http://example.com/book/Math_semester2",
        "DLD": "http://example.com/book/Math_semester2",
        "EVS": "http://example.com/book/Math_semester2",
        "PS": "http://example.com/book/Math_semester2"
    },
    4: {
        "AD2": "http://example.com/book/AD_semester2",
        "ALA": "http://example.com/book/Math_semester2",
        "COA": "coa.pdf",
        "CSW2": "http://example.com/book/Math_semester2",
        "UHV": "uhv.pdf"
    }
}

recommender = None
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {"Authorization": "Bearer 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"}


def text_to_chunks(texts, word_length=150, start_page=1):
    text_toks = [t.split(' ') for t in texts]
    chunks = []

    for idx, words in enumerate(text_toks):
        for i in range(0, len(words), word_length):
            chunk = words[i : i + word_length]
            if (
                (i + word_length) > len(words)
                and (len(chunk) < word_length)
                and (len(text_toks) != (idx + 1))
            ):
                text_toks[idx + 1] = chunk + text_toks[idx + 1]
                continue
            chunk = ' '.join(chunk).strip()
            chunk = f'[Page no. {idx+start_page}]' + ' ' + '"' + chunk + '"'
            chunks.append(chunk)
    return chunks

def load_recommender(path, start_page=1):
    global recommender
    if recommender is None:
        recommender = SemanticSearch()

    texts = pdf_to_text(path, start_page=start_page)
    chunks = text_to_chunks(texts, start_page=start_page)
    recommender.fit(chunks)
    print(f"text is {texts} and chunk is {chunks}")
    return 'Corpus Loaded.'


class SemanticSearch:
    def __init__(self):
        self.use = hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')
        self.fitted = False

    def fit(self, data, batch=1000, n_neighbors=5):
        self.data = data
        self.embeddings = self.get_text_embedding(data, batch=batch)
        n_neighbors = min(n_neighbors, len(self.embeddings))
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        self.nn.fit(self.embeddings)
        self.fitted = True

    def __call__(self, text, return_data=True):
        inp_emb = self.use([text])
        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]

        if return_data:
            return [self.data[i] for i in neighbors]
        else:
            return neighbors

    def get_text_embedding(self, texts, batch=1000):
        embeddings = []
        for i in range(0, len(texts), batch):
            text_batch = texts[i : (i + batch)]
            emb_batch = self.use(text_batch)
            embeddings.append(emb_batch)
        embeddings = np.vstack(embeddings)
        return embeddings

def get_book_link(semester, subject):
    return book_links.get(semester, {}).get(subject, "Book link not found")
def preprocess(text):
    text = text.replace('\n', ' ')
    text = re.sub('\s+', ' ', text)
    return text
    
       
def pdf_to_text(path, start_page=1, end_page=None):
    doc = fitz.open(path)
    total_pages = doc.page_count

    if end_page is None:
        end_page = total_pages

    text_list = []

    for i in range(start_page - 1, end_page):
        text = doc.load_page(i).get_text("text")
        text = preprocess(text)
        text_list.append(text)

    doc.close()
    return text_list

def generate_answer(question):
    topn_chunks = recommender(question)
    prompt = ""
    prompt += 'search results:\n\n'
    for c in topn_chunks:
        prompt += c + '\n\n'

    prompt += (
        "Instructions: Compose a comprehensive reply to the query using the search results given. "
        "Cite each reference using [ Page Number] notation (every result has this number at the beginning). "
        "Citation should be done at the end of each sentence. If the search results mention multiple subjects "
        "with the same name, create separate answers for each. Only include information found in the results and "
        "don't add any additional information. Make sure the answer is correct and don't output false content. "
        "If the text does not relate to the query, simply state 'Text Not Found in PDF'. Ignore outlier "
        "search results which has nothing to do with the question. Only answer what is asked. The "
        "answer should be short and concise. Answer step-by-step. \n\nQuery: {question}\nAnswer: "
    )

    prompt += f"Query: {question}\nAnswer:"
    answer = requests.post(API_URL, headers=headers, json={"inputs":prompt})
    return answer.json()[0]["generated_text"]


@app.route('/get-book-link', methods=['GET'])
def getbook_link():
    data = request.get_json()
    semester = data.get('semester')
    print(type(semester))
    return book_links[semester]

@app.route('/process', methods=['POST'])
def process_request():
    data = request.get_json()
    semester = data.get('semester')
    subject = data.get('subject')
    question = data.get('question')
    
    if semester and subject:
        book_link = get_book_link(semester, subject)
        #text = pdf_to_text(book_link)
        load_recommender(book_link)
        # return generate_answer(question)
        # response = {
        #     'semester': semester,
        #     'subject': subject,
        #     'book_link': book_link,
        #     'book_text' : text
        # }
        return jsonify(generate_answer(question)), 200
    else:
        return jsonify({'error': 'Invalid input'}), 400

if __name__ == '__main__':
    app.run(debug=True)
