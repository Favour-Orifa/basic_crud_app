from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
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

class TaskCreate(BaseModel):
    title: str

@app.post("/tasks", status_code= 201)
def create_task(newtask: TaskCreate):
    if not newtask.title.strip():
        raise HTTPException(status_code= 400, detail= {"error": "title required"})

    next_id = max( task["id"] for task in tasks) + 1
    task = {"id" : next_id, "title" : newtask.title, "done" : False}
    tasks.append(task)
    return task

class TaskUpdate(BaseModel):
    title : str
    done : Optional[bool] = None

@app.put("/tasks/{task_id}")
def update_task(task_id:int, updated : TaskUpdate):
    if not updated.title.strip():
        raise HTTPException(status_code=400, detail={"error": "title required"})
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated.title
            if updated.done is not None:
                task["done"] = updated.done
            return task
    raise HTTPException(status_code= 404, detail= {"error" : f"taskid {task_id} not found"})    

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code= 404, detail = {"error" : f"task {task_id} not found"})    

