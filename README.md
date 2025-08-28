# Customer Service AI Agent

A simple yet powerful **AI Customer Service Agent** that can:
- Answer customer questions  
- Recommend available services  
- Enroll users when eligible  
- Handle multiple users concurrently  
- Remember past conversations  

> 🚀 This project demonstrates how to build a production-style AI assistant with **RAG, LangGraph orchestration, and a full-stack setup**.  

---

## 🔎 How It Works

- **RAG (Retrieval-Augmented Generation)** → powered by [LlamaIndex](https://github.com/jerryjliu/llama_index)  
  - Service catalogs, descriptions, and pricing are indexed  
  - Context stored in **ChromaDB**  

- **Orchestration** → [LangGraph](https://github.com/langchain-ai/langgraph) + [LangChain](https://github.com/langchain-ai/langchain)  
  - Multi-step reasoning and workflow handling  

- **Backend** → Flask REST API  
- **Frontend** → [Streamlit](https://streamlit.io/) web interface  

---

## 📸 Demo

Amazon is just a **sample dataset** (not affiliated).  
*(Insert GIF/screenshot of your demo here)*  
[Watch the demo](https://youtu.be/R7gtjDmP00I)

---

## ⚙️ Installation

Clone the repo:  
```bash
git clone https://github.com/MagdiWaleed/customer-service-backend.git
cd customer-service-backend
````

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend (Flask):

```bash
python run.py
```

Run frontend (Streamlit):

[Set Up and Run The Frontend](https://github.com/MagdiWaleed/customer-service-frontend)
* **Note:** Remember to adjust The URL links between the frontend and the backend properly

---

## 🛠 Tech Stack

* **AI/ML** → LlamaIndex, LangChain, LangGraph
* **Database** → ChromaDB
* **Backend** → Flask
* **Language** → Python

---

## 📂 Project Structure

```
.
├── app.py                # Flask backend
├── data_vectorizor.py                 # To embedd the data and added to the db
├── agents/             # Agent, db, and tools
├── instance/                  # Backend db
├── models/               # Database tabels structure
├── requirements.txt
└── README.md
```

---

## 🚀 Future Improvements

* Add authentication & role-based access
* Integrate real company datasets
* Expand multi-turn reasoning with workflows
* Dockerize deployment

---

## 📬 Contact

If you find this project useful, feel free to ⭐ star the repo and connect on [LinkedIn](www.linkedin.com/in/magdi-waleed).

```
```
