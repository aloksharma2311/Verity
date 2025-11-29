# ⚡ **Verity – AI-Verified Short News Platform**

A fast, reliable, and AI-powered platform that verifies news stories *before* they reach the public feed.
Creators upload short news summaries, the backend verifies them using **GNews + LLM reasoning**, and users consume a clean, trustworthy, bias-free feed.

---

# 🌟 Key Features

### 📰 **AI-Verified Feed**

* Only shows *verified* stories.
* Every piece of news passes through an automated fact-checking system.
* Clean, minimal, Cupertino-style UI.

### 🤖 **AI Claim Verification (Chatbot)**

* Enter any news claim or rumor.
* Our AI agent gives:

  * Verdict → **True / False / Mixed / Uncertain**
  * Confidence score (0–100)
  * Bullet-point explanation

### ✍️ **Creator Upload Flow**

* Submit **title + description**.
* Backend runs AI verification.
* Approved → saved to feed.
* Rejected → returns feedback for correction.

### 🔐 **Email + Password Authentication**

* JWT-powered secure login/signup.
* Fast and simple—ideal for rapid publishing.

### 🗄️ **SQLite Backend**

* Lightweight, fast, zero-setup database.
* Perfect for rapid prototyping and hackathon use.

---

# 🧠 AI Verification Workflow

1. User submits a claim or upload text.
2. Backend fetches top related articles using **GNews API**.
3. Claim + articles sent to **LLM (Claude/OpenAI)**.
4. LLM provides structured output:

   * `verdict`: True / False / Mixed / Uncertain
   * `score`: Numerical confidence
   * `bullets`: Short reasoning points
5. If score ≥ threshold (default: **60**) → content marked as verified.
6. Result returned instantly to the app.

---

# 🧩 System Architecture

```
Flutter App  →  FastAPI Backend  →  AI Agent
                   |                   |
                   |         ┌─────────┴─────────┐
                   |         |  GNews API Query   |
                   |         |  LLM Analysis      |
                   |         └─────────┬─────────┘
                   └─────── SQLite DB (Users, News)
```

---

# 🛠️ Tech Stack

### **Frontend (Flutter)**

* Cupertino-style UI
* Riverpod for state management
* Dio for networking
* Secure Storage for JWT

### **Backend (FastAPI)**

* FastAPI + Uvicorn
* SQLite + SQLAlchemy
* Passlib + JWT (python-jose)
* httpx for external APIs
* Dotenv for secrets

### **AI Components**

* **GNews API** for related articles
* **Claude/OpenAI** for reasoning & verdicts

---

# 📡 API Endpoints

### 🔐 Authentication

| Method | Route          | Description     |
| ------ | -------------- | --------------- |
| POST   | `/auth/signup` | Create user     |
| POST   | `/auth/login`  | Login + get JWT |

### 📰 News

| Method | Route          | Description              |
| ------ | -------------- | ------------------------ |
| GET    | `/feed`        | Fetch verified news      |
| POST   | `/news/upload` | Upload + AI verification |

### 🤖 Chatbot

| Method | Route          | Description         |
| ------ | -------------- | ------------------- |
| POST   | `/chat/verify` | Verify claim via AI |

---

# 📂 Project Structure

```
verity/
│
├── backend/
│   └── app/
│       ├── main.py
│       ├── auth.py
│       ├── news.py
│       ├── chat.py
│       ├── ai_agent.py
│       ├── gnews_client.py
│       ├── llm_client.py
│       ├── database.py
│       ├── models.py
│       └── schemas.py
│
└── app/ (Flutter project)
    ├── lib/
    │   ├── core/api_client.dart
    │   ├── features/auth/
    │   ├── features/home/
    │   ├── features/upload/
    │   └── features/chatbot/
    └── pubspec.yaml
```

---

# 🔐 Environment Variables

Create `.env` inside `/backend`:

```
GNEWS_API_KEY=your_key_here
LLM_API_KEY=your_key_here
JWT_SECRET=super_secret_key
```

Add `.env` to `.gitignore`.

---

# ⚙️ Setup Instructions

### **Backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### **Flutter**

```bash
cd app
flutter pub get
flutter run
```

---

# 🚀 Demo Flow

1. **Sign up** as a new user
2. View the **verified news feed**
3. Try the **Chatbot** to verify any claim
4. Upload new story →

   * If authentic → added to feed
   * If misleading → AI gives corrections

---

# 📌 Future Enhancements

* 📸 Video/image uploads with AI validation
* 🌍 Personalized interests and location-aware feed
* 👤 Profile page + logout
* 🛡️ Advanced credibility scoring badges
* 📊 Analytics for creators