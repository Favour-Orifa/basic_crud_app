from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Task API", version=1.0)

@app.get("/")
def root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

@app.get("/health")
def health():
    return {"status" : "ok"}

tasks = [
    {"id" : 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "walk the dog", "done": False},
    {"id" : 3, "title": "finish assignment", "done" : True}
]

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id : int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail = {"error": f"Task {task_id} not found"})