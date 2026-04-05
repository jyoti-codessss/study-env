class StudyEnvironment:
    TASKS = {
        "easy":   [{"id": 1, "subject": "Math",   "done": False}],
        "medium": [{"id": 1, "subject": "Math",   "done": False},
                   {"id": 2, "subject": "Python", "done": False}],
        "hard":   [{"id": 1, "subject": "Math",   "done": False},
                   {"id": 2, "subject": "Python", "done": False},
                   {"id": 3, "subject": "DBMS",   "done": False}],
    }

    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty
        self.state_data = None

    def reset(self):
        import copy
        self.state_data = {
            "tasks":      copy.deepcopy(self.TASKS[self.difficulty]),
            "completed":  0,
            "step_count": 0,
            "difficulty": self.difficulty,
        }
        return self.state_data

    def step(self, action):
        if self.state_data is None:
            raise RuntimeError("Call reset() first")
        task_id = action.get("complete_task_id")
        reward = 0.0
        info = {}
        for task in self.state_data["tasks"]:
            if task["id"] == task_id:
                if task["done"]:
                    info["error"] = f"Task {task_id} already done"
                else:
                    task["done"] = True
                    self.state_data["completed"] += 1
                    reward = 1.0
                    info["completed_subject"] = task["subject"]
                break
        else:
            info["error"] = f"Task {task_id} does not exist"
        self.state_data["step_count"] += 1
        done = self.state_data["completed"] == len(self.state_data["tasks"])
        return {
            "observation": {
                "tasks":     self.state_data["tasks"],
                "completed": self.state_data["completed"],
                "done":      done,
                "reward":    reward,
                "metadata":  {"step_count": self.state_data["step_count"],
                              "difficulty": self.difficulty},
            },
            "reward": reward,
            "done":   done,
            "info":   info,
        }

    def state(self):
        return self.state_data