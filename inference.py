import os
import sys
import json
import time
import requests

# Config
ENV_URL = os.environ.get("ENV_URL", "http://localhost:8000")
HF_TOKEN = os.environ.get("HF_TOKEN", "")
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api-inference.huggingface.co/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.3")

TASKS = ["easy", "medium", "hard"]

def reset(difficulty):
    r = requests.post(f"{ENV_URL}/reset",
                      params={"difficulty": difficulty})
    return r.json()

def step(task_id):
    r = requests.post(f"{ENV_URL}/step",
                      json={"complete_task_id": task_id},
                      headers={"Content-Type": "application/json"})
    return r.json()

def get_action(obs):
    tasks = obs.get("tasks", [])
    for task in tasks:
        if not task["done"]:
            return task["id"]
    return 1

def run_task(difficulty):
    obs = reset(difficulty)
    done = False
    step_num = 0
    total_reward = 0.0

    print(json.dumps({
        "event": "[START]",
        "task_id": difficulty,
        "tasks": [t["subject"] for t in obs.get("tasks", [])]
    }), flush=True)

    while not done and step_num < 20:
        task_id = get_action(obs)
        result = step(task_id)
        reward = result.get("reward", 0.0)
        done = result.get("done", False)
        obs = result.get("observation", obs)
        step_num += 1
        total_reward += reward

        print(json.dumps({
            "event": "[STEP]",
            "task_id": difficulty,
            "step": step_num,
            "action": task_id,
            "reward": reward,
            "done": done,
        }), flush=True)

    score = round(min(1.0, total_reward / max(1, len(obs.get("tasks", [1])))), 4)

    print(json.dumps({
        "event": "[END]",
        "task_id": difficulty,
        "total_steps": step_num,
        "total_reward": round(total_reward, 4),
        "score": score,
    }), flush=True)

    return score

def main():
    print("Study Env Inference", flush=True)
    print(f"ENV_URL: {ENV_URL}", flush=True)

    # Wait for environment
    for i in range(10):
        try:
            r = requests.get(f"{ENV_URL}/health", timeout=5)
            if r.status_code == 200:
                print("Environment ready!", flush=True)
                break
        except:
            pass
        print(f"Waiting... ({i+1}/10)", flush=True)
        time.sleep(3)

    scores = []
    for difficulty in TASKS:
        print(f"\n--- Task: {difficulty} ---", flush=True)
        score = run_task(difficulty)
        scores.append(score)
        print(f"Score: {score}", flush=True)

    avg = sum(scores) / len(scores)
    print(f"\nAverage Score: {avg:.4f}", flush=True)

if __name__ == "__main__":
    main()