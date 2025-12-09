# AI Workflow Assignment – Workflow Engine (FastAPI)

This project is part of my AI Engineering assignment.  
The goal is to build a simple workflow engine using Python and FastAPI, and show how nodes, edges, and state can be used to run a process step-by-step.

---

## 🎯 Purpose of the Project

The purpose of this project is to build a simple workflow engine that can run a sequence of steps automatically using Python and FastAPI.  
Through this assignment, I learned how nodes, edges, and shared state work together in a workflow, how data moves between steps, and how to design a backend system that can run and track a process.  
To demonstrate the engine, I implemented a basic text-summarization workflow that splits text, summarizes it, merges the results, and refines the final output.

---

## 📌 Features

- Backend built using **FastAPI**
- Create graphs with nodes and edges  
- State is passed from one step to the next  
- Supports looping using `__next__`  
- In-memory storage for graphs and runs  
- API endpoints for:
  - Creating graph  
  - Running graph  
  - Checking run status  

---

## 🧠 Workflow Implemented: Text Summarization

The workflow has **4 simple steps**:

1. **Split Text** – Breaks the input text into smaller chunks  
2. **Generate Summaries** – Creates a short summary for each chunk  
3. **Merge Summaries** – Combines all summaries into one  
4. **Refine Summary** – Shortens the merged summary until it fits a word limit (loops if needed)

This is a simple **rule-based workflow**, created only to demonstrate the workflow engine.

---

## 📂 Project Structure

ai-workflow-assignment/
│── app/
│ ├── main.py
│ ├── models.py
│ ├── graph_engine.py
│ ├── store.py
│ └── workflows/
│ ├── summarization.py
│ └── init.py
│
│── requirements.txt
│── .gitignore

yaml
Copy code

---

## ⚙️ How to Run the Project

### 1️⃣ Create and activate virtual environment
```bash
python -m venv venv
Windows:

bash
Copy code
venv\Scripts\activate
2️⃣ Install requirements
bash
Copy code
pip install -r requirements.txt
3️⃣ Start the server
bash
Copy code
uvicorn app.main:app --reload
Open in browser:

API Base URL → http://127.0.0.1:8000

Swagger Docs → http://127.0.0.1:8000/docs

🧪 How to Test the Workflow
1️⃣ Create a graph
Endpoint: POST /graph/create

Example body:

json
Copy code
{
  "nodes": ["split_text", "generate_summaries", "merge_summaries", "refine_summary"],
  "edges": {
    "split_text": "generate_summaries",
    "generate_summaries": "merge_summaries",
    "merge_summaries": "refine_summary",
    "refine_summary": null
  },
  "start_node": "split_text"
}
2️⃣ Run the graph
Endpoint: POST /graph/run

Example body:

json
Copy code
{
  "graph_id": "<your_graph_id>",
  "initial_state": {
    "text": "This is a sample text used to test the workflow...",
    "chunk_size": 20,
    "max_summary_words": 40,
    "max_refine_loops": 5
  }
}
3️⃣ Check run state
Endpoint: GET /graph/state/<run_id>

You will see:

run_id

graph_id

current status

final output

step-by-step logs

 What I Learned
How a workflow engine works internally

How nodes, edges, and shared state interact

How looping and branching work

Basics of backend development using FastAPI

How to structure a small backend project

👤 Student Details
Name: Sri Krishna
Course: B.Tech Artificial Intelligence
College: SRM Kattankulathur

✔️ Submission
This repository contains the complete assignment with working code, proper structure, and a clean README.
