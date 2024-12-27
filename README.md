### URL Endpoints Documentation  

Below is the documentation on how to access and utilize the API endpoints in my Django application:  

---

#### **1. Login**  
**URL:** `/`  
**Method:** `GET`, `POST`  
**Description:**  
Handles user login. Access this endpoint to authenticate users into the system.  

**Example:**  
```
GET /  
POST / { "username": "example", "password": "password123" }
```

---

#### **2. Notify Results**  
**URL:** `/<int:quiz_id>/notify/`  
**Method:** `POST`  
**Description:**  
Notifies users of the quiz results for a specific quiz.  
- Replace `<int:quiz_id>` with the specific quiz ID.  

**Example:**  
```
POST /5/notify/  
```

---

#### **3. Generate Quiz**  
**URL:** `/quiz/`  
**Method:** `GET`, `POST`  
**Description:**  
Allows users to generate a new quiz.  
- Use `GET` to fetch details of available quizzes or `POST` to create a new quiz.  

**Example:**  
```
GET /quiz/  
POST /quiz/ { "title": "Sample Quiz", "questions": [...] }
```

---

#### **4. Submit Quiz**  
**URL:** `/quiz/<str:quiz_id>/submit/`  
**Method:** `POST`  
**Description:**  
Submits the answers for a specific quiz.  
- Replace `<str:quiz_id>` with the quiz's unique string ID.  

**Example:**  
```
POST /quiz/abc123/submit/  
Payload: { "answers": [...] }
```

---

#### **5. Quiz History**  
**URL:** `/quiz/history/`  
**Method:** `GET`  
**Description:**  
Fetches the history of quizzes attempted by the user.  

**Example:**  
```
GET /quiz/history/  
```

---  
