import os
import random
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import openai

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

context = {
    "projects": [],
    "students": [],
    "educators": [],
    "techniques": [],
    "results": [],
}

# HTML templates
ADMIN_FORM = """
<!DOCTYPE html>
<html>
<head><title>Admin Input</title></head>
<body>
<h1>Add Context Item</h1>
<form action="/admin" method="get">
    <label>Type:
        <select name="item_type">
            <option value="projects">Project</option>
            <option value="students">Student</option>
            <option value="educators">Educator</option>
            <option value="techniques">Technique</option>
            <option value="results">Result</option>
        </select>
    </label>
    <br/>
    <label>Text: <input name="text" /></label>
    <br/>
    <button type="submit">Add</button>
</form>
</body>
</html>
"""

BOARD_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Team Story Board</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 20%; }
        #story { font-size: 2em; }
    </style>
    <script>
    async function updateStory() {
        const resp = await fetch('/story');
        const data = await resp.json();
        document.getElementById('story').innerText = data.story;
    }
    setInterval(updateStory, 5 * 60 * 1000); // every 5 minutes
    window.onload = updateStory;
    </script>
</head>
<body>
    <div id="story">Loading story...</div>
</body>
</html>
"""

@app.get('/admin', response_class=HTMLResponse)
async def admin(request: Request):
    item_type = request.query_params.get("item_type")
    text = request.query_params.get("text")
    if item_type and text and item_type in context:
        context[item_type].append(text)
    return ADMIN_FORM

@app.get('/board', response_class=HTMLResponse)
async def board():
    return BOARD_PAGE

def generate_story() -> str:
    if not any(context.values()):
        return "No stories yet. Add context via /admin."
    project = random.choice(context['projects']) if context['projects'] else 'a project'
    student = random.choice(context['students']) if context['students'] else 'a student'
    educator = random.choice(context['educators']) if context['educators'] else 'an educator'
    technique = random.choice(context['techniques']) if context['techniques'] else 'a technique'
    result = random.choice(context['results']) if context['results'] else 'great results'
    prompt = (
        "Create a short, upbeat announcement about an AI education project using "
        f"the following context:\n"
        f"Project: {project}\n"
        f"Student: {student}\n"
        f"Educator: {educator}\n"
        f"Technique: {technique}\n"
        f"Result: {result}"
    )
    templates = [
        f"{student} and {educator} are exploring {technique} in {project}, leading to {result}.",
        f"In {project}, {student} works with {educator} using {technique}. They achieved {result}.",
        f"{educator} guides {student} through {project} with {technique}, unveiling {result}.",
    ]
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4.1-nano",
            messages=[
                {
                    "role": "system",
                    "content": "You craft short and enthusiastic announcements about AI education projects."
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=60,
        )
        story = resp.choices[0].message["content"].strip()
        if story:
            return story
    except Exception:
        pass
    return random.choice(templates)

@app.get('/story')
async def story():
    return JSONResponse({"story": generate_story()})

