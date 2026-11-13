from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=160)
    password: str = Field(min_length=12, max_length=128)


class UserRead(ORMModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=10000)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=10000)
    status: str | None = Field(default=None, pattern="^(planning|active|completed|cancelled)$")


class ProjectRead(ORMModel):
    id: int
    name: str
    description: str
    status: str
    owner_id: int


class AgentRead(ORMModel):
    id: int
    name: str
    role: str
    description: str
    is_active: bool


class ConversationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    agent_id: int
    project_id: int | None = None


class ConversationRead(ORMModel):
    id: int
    title: str
    user_id: int
    agent_id: int
    project_id: int | None


class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=20000)


class MessageRead(ORMModel):
    id: int
    conversation_id: int
    sender_type: str
    content: str


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=10000)
    assignee_id: int | None = None


class TaskUpdate(BaseModel):
    status: str | None = Field(default=None, pattern="^(pending|in_progress|completed|blocked|cancelled)$")
    assignee_id: int | None = None


class TaskRead(ORMModel):
    id: int
    title: str
    description: str
    status: str
    project_id: int
    assignee_id: int | None


class ReviewCreate(BaseModel):
    verdict: str = Field(pattern="^(APPROVED|REJECTED)$")
    findings: str = Field(default="", max_length=20000)
    task_id: int | None = None


class ReviewRead(ORMModel):
    id: int
    verdict: str
    findings: str
    project_id: int
    reviewer_agent_id: int
    task_id: int | None


class ProjectProgress(BaseModel):
    project_id: int
    total_tasks: int
    pending: int
    in_progress: int
    completed: int
    blocked: int
    completion_percent: float
