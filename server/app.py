import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from env import StudyEnvironment

app = FastAPI(title='Study Env')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

env = StudyEnvironment()

class Action(BaseModel):
    complete_task_id: int

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.get('/')
def root():
    return {'name': 'Study Env', 'endpoints': ['/reset', '/step', '/state', '/health', '/docs']}

@app.post('/reset')
def reset(difficulty: str = 'easy'):
    global env
    env = StudyEnvironment(difficulty=difficulty)
    return env.reset()

@app.post('/step')
def step(action: Action):
    return env.step({'complete_task_id': action.complete_task_id})

@app.get('/state')
def state():
    return env.state()