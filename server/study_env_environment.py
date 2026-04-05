from server.models import StudyAction, StudyObservation

class StudyEnvironment:
    def __init__(self):
        self.state = None

    def reset(self, seed=None, episode_id=None):
        self.state = {
            "tasks": [
                {"id": 1, "subject": "Math", "done": False},
                {"id": 2, "subject": "Python", "done": False},
                {"id": 3, "subject": "DBMS", "done": False}
            ],
            "completed": 0
        }

        return StudyObservation(
            tasks=self.state["tasks"],
            completed=0,
            done=False,
            reward=0.0
        )

    def step(self, action: StudyAction):
        reward = 0.0

        for task in self.state["tasks"]:
            if task["id"] == action.complete_task_id and not task["done"]:
                task["done"] = True
                self.state["completed"] += 1
                reward = 1.0

        done = self.state["completed"] == len(self.state["tasks"])

        return StudyObservation(
            tasks=self.state["tasks"],
            completed=self.state["completed"],
            done=done,
            reward=reward
        )