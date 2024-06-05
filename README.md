# QuickSheet API

## Overview
This project provides an API that allows users to query and retrieve information from textbooks based on specific questions. The API consists of two main endpoints:

1. `/process` - To process the query and retrieve search results.
2. `/get-book-link` - To get the link to the textbooks based on the semester.

## Endpoints

### 1. `/process`

#### Description
This endpoint processes a query and returns search results from the relevant textbook.

#### URL
`http://127.0.0.1:5000/process`

#### Method
`POST`

#### Request Body
```json
{
    "semester": 1, 
    "subject": "UPEM",
    "question": "What are the types of Motion?"
}
```
#### Response Body
```json
{
    "search results:\n\n[Page no. 95] \"constant speed or varying speed. • How to relate the velocity of a mov- ing body as seen from two different frames of reference. MOTION IN TWO OR THREE DIMENSIONS W hat determines where a batted baseball lands? How do you describe the motion of a roller coaster car along a curved track or the ﬂight of a circling hawk? Which hits the ground ﬁrst: a baseball that you sim- ply drop or one that you throw horizontally? We can’t answer these kinds of questions using the techniques of Chapter 2, in which particles moved only along a straight line. Instead, we need to extend our descriptions of motion to two- and three-dimensional situations. We’ll still use the vector quantities displacement, velocity, and acceleration, but now these quantities will no longer lie along a single line. We’ll find that several important kinds of motion take place in two dimensions only—that\"\n\n[Page no. 130] \"one, two, or three dimen- sions. But what causes bodies to move the way that they do? For example, how can a tugboat push a cruise ship that’s much heavier than the tug? Why is it harder to control a car on wet ice than on dry concrete? The answers to these and similar questions take us into the subject of dynamics, the relationship of motion to the forces that cause it. In this chapter we will use two new concepts, force and mass, to analyze the principles of dynamics. These principles were clearly stated for the ﬁrst time by Sir Isaac Newton (1642–1727); today we call them Newton’s laws of motion. The ﬁrst law states that when the net force on a body is zero, its motion doesn’t change. The second law relates force to acceleration when the net force is not zero. The third law is a relationship\"\n\n[Page no. 61] \"chapter. We are beginning our study of physics with mechanics, the study of the relationships among force, matter, and motion. In this chapter and the next we will study kinematics, the part of mechanics that enables us to describe motion. Later we will study dynamics, which relates motion to its causes. In this chapter we concentrate on the simplest kind of motion: a body moving along a straight line. To describe this motion, we introduce the physical quantities velocity and acceleration. In physics these quantities have deﬁnitions that are more precise and slightly different from the ones used in everyday language. Both velocity and acceleration are vectors: As you learned in Chapter 1, this means that they have both magnitude and direction. Our concern in this chapter is with motion along a straight line only, so we won’t need the full mathematics of vectors just yet. But using vectors will\"\n\n[Page no. 334] \"or of a rigid body. • How the angular momentum of a system changes with time. • Why a spinning gyroscope goes through the curious motion called precession. DYNAMICS OF ROTATIONAL MOTION W e learned in Chapters 4 and 5 that a net force applied to a body gives that body an acceleration. But what does it take to give a body an angular acceleration? That is, what does it take to start a stationary body rotating or to bring a spinning body to a halt? A force is required, but it must be applied in a way that gives a twisting or turning action. In this chapter we will deﬁne a new physical quantity, torque, that describes the twisting or turning effort of a force. We’ll ﬁnd that the net torque acting on a rigid body determines its angular acceleration, in the same way that the net force on\"\n\n[Page no. 304] \"a ceiling fan have in common? None of these can be repre- sented adequately as a moving point; each involves a body that rotates about an axis that is stationary in some inertial frame of reference. Rotation occurs at all scales, from the motions of electrons in atoms to the motions of entire galaxies. We need to develop some general methods for analyz- ing the motion of a rotating body. In this chapter and the next we consider bodies that have deﬁnite size and deﬁnite shape, and that in general can have rotational as well as translational motion. Real-world bodies can be very complicated; the forces that act on them can deform them—stretching, twisting, and squeezing them. We’ll neglect these deformations for now and assume that the body has a perfectly deﬁnite and unchanging shape and size. We call this idealized model a rigid body. This chap- ter and the\"\n\nInstructions: Compose a comprehensive reply to the query using the search results given. Cite each reference using [ Page Number] notation (every result has this number at the beginning). Citation should be done at the end of each sentence. If the search results mention multiple subjects with the same name, create separate answers for each. Only include information found in the results and don't add any additional information. Make sure the answer is correct and don't output false content. If the text does not relate to the query, simply state 'Text Not Found in PDF'. Ignore outlier search results which has nothing to do with the question. Only answer what is asked. The answer should be short and concise. Answer step-by-step. \n\nQuery: {question}\nAnswer: Query: What are the types of Motion?\nAnswer: \n1. The motion of objects in the sky, including a fixed position, is called.\"\n\n2. Linear motion is an object's displacement in the horizontal direction. It is generally represented on a graph as a line that changes in length the same way it changes in any of the other two dimensions. It is the motion of an object along a general straight line.\n\n3. Circular motion is an object's motion around its own center point. It is represented by"
}
```
#### URL
`http://127.0.0.1:5000/get-book-link`

#### Method
`GET`

#### Request Body
```json
{
    "semester": 1
}
```

#### Response Body
```json
{
    
    "Cal1": "http://example.com/book/AD_semester1",
    "DM": "http://example.com/book/Math_semester1",
    "ICP": "http://example.com/book/Math_semester1",
    "PME1": "http://example.com/book/Math_semester1",
    "UPEM": "upem.pdf"
}

```

Example

```bash
curl -X POST http://127.0.0.1:5000/process -H "Content-Type: application/json" -d '{
    "semester": 1, 
    "subject": "UPEM",
    "question": "What are the types of Motion?"
}'
```


```bash
curl -X POST http://127.0.0.1:5000/get-book-link -H "Content-Type: application/json" -d '{
    "semester": 1
}'
```
