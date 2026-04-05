"""
Pydantic models for StudyAction and StudyObservation.
Uses plain Pydantic — no openenv.core dependency required to run locally.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any


class StudyAction(BaseModel):
    """Action: which task to complete."""
    complete_task_id: int = Field(..., description="ID of the task to complete (1, 2, or 3)")


class StudyObservation(BaseModel):
    """Observation returned after each step."""
    tasks:     List[Dict]      = Field(default_factory=list,  description="All tasks with done status")
    completed: int             = Field(default=0,             description="How many tasks are done")
    done:      bool            = Field(default=False,         description="True when all tasks complete")
    reward:    float           = Field(default=0.0,           description="Reward earned this step")
    metadata:  Dict[str, Any]  = Field(default_factory=dict,  description="Extra info like step_count")