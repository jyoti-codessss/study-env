"""
Core Study Environment logic.
Implements reset(), step(), state() — no external dependencies needed.
"""


class StudyEnvironment:
    """
    A simple RL environment where an agent completes study tasks.

    Tasks:
        1. Math
        2. Python
        3. DBMS

    Reward:
        +1.0 for each task completed
        +0.0 for invalid or already-done task
        Full episode ends when all 3 tasks are done.
    """

    def __init__(self):
        self.state_data = None

    def reset(self):
        """Reset the environment to start a new episode."""
        self.state_data = {
            "tasks": [
                {"id": 1, "subject": "Math",   "done": False},
                {"id": 2, "subject": "Python",  "done": False},
                {"id": 3, "subject": "DBMS",    "done": False},
            ],
            "completed": 0,
            "step_count": 0,
        }
        return self.state_data

    def step(self, action: dict):
        """
        Take one step: complete a task by its ID.

        Args:
            action: dict with key "complete_task_id" (int)

        Returns:
            dict with keys: observation, reward, done, info
        """
        if self.state_data is None:
            raise RuntimeError("Call reset() before step()")

        task_id = action.get("complete_task_id")
        reward = 0.0
        info = {}

        if task_id is None:
            info["error"] = "Missing complete_task_id in action"
        else:
            matched = False
            for task in self.state_data["tasks"]:
                if task["id"] == task_id:
                    matched = True
                    if task["done"]:
                        info["error"] = f"Task {task_id} already completed"
                    else:
                        task["done"] = True
                        self.state_data["completed"] += 1
                        reward = 1.0
                        info["completed_subject"] = task["subject"]
                    break
            if not matched:
                info["error"] = f"Task id {task_id} does not exist"

        self.state_data["step_count"] += 1
        done = self.state_data["completed"] == len(self.state_data["tasks"])

        # Build observation
        observation = {
            "tasks":     self.state_data["tasks"],
            "completed": self.state_data["completed"],
            "done":      done,
            "reward":    reward,
            "metadata":  {"step_count": self.state_data["step_count"]},
        }

        return {
            "observation": observation,
            "reward":      reward,
            "done":        done,
            "info":        info,
        }

    def state(self):
        """Return current raw state dict."""
        if self.state_data is None:
            raise RuntimeError("Call reset() first")
        return self.state_data