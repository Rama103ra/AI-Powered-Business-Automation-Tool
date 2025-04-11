from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.email_processor import EmailProcessor
from core.meeting_scheduler import MeetingScheduler
from core.task_manager import TaskManager
from datetime import datetime

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize core components
email_processor = EmailProcessor()
meeting_scheduler = MeetingScheduler()
task_manager = TaskManager()

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/email", response_class=HTMLResponse)
async def email_page(request: Request):
    return templates.TemplateResponse("email.html", {"request": request})

@app.get("/meeting", response_class=HTMLResponse)
async def meeting_page(request: Request):
    return templates.TemplateResponse("meeting.html", {"request": request})

@app.get("/task", response_class=HTMLResponse)
async def task_page(request: Request):
    return templates.TemplateResponse("task.html", {"request": request})

@app.post("/email/process")
async def process_email(request: Request, content: str = Form(...), sender: str = Form(...)):
    email_data = {"content": content, "sender": sender}
    result = await email_processor.process(email_data)
    return templates.TemplateResponse("email.html", {"request": request, "result": result})



@app.post("/meeting/schedule")
async def schedule_meeting(request: Request, title: str = Form(...), participants: str = Form(...)):
    participants_list = participants.split(",")
    meeting_data = {"title": title, "participants": participants_list}
    result = await meeting_scheduler.schedule(meeting_data)

    # Preprocess the result to make it template-friendly
    if result["success"]:
        result["meeting_details"]["start_time"] = result["meeting_details"]["start_time"].strftime("%Y-%m-%d %H:%M:%S")
        result["meeting_details"]["end_time"] = result["meeting_details"]["end_time"].strftime("%Y-%m-%d %H:%M:%S")
        result["scheduled_time"] = datetime.fromisoformat(result["scheduled_time"]).strftime("%Y-%m-%d %H:%M:%S")

    return templates.TemplateResponse("meeting.html", {"request": request, "result": result})

@app.post("/task/manage")
async def manage_task(request: Request, task_name: str = Form(...), deadline: str = Form(...)):
    task_data = {"name": task_name, "deadline": deadline}
    result = await task_manager.process_task(task_data)

    # Preprocess the task details for template rendering
    if "reminders" in result:
        for reminder in result["reminders"]:
            reminder["time"] = reminder["time"].strftime("%Y-%m-%d %H:%M:%S")

    return templates.TemplateResponse("task.html", {"request": request, "result": result})

# Add this to run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)