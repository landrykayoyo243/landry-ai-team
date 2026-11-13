from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.schemas import AgentRead, ConversationCreate, ConversationRead, MessageCreate, MessageRead, ProjectCreate, ProjectProgress, ProjectRead, ProjectUpdate, ReviewCreate, ReviewRead, TaskCreate, TaskRead, TaskUpdate, Token, UserCreate, UserRead
from app.database.models import Agent, Conversation, Message, Project, Review, Task, User
from app.database.session import get_db
from app.services.security import create_access_token, ensure_project_access, get_current_user, hash_password, require_admin, verify_password

api_router = APIRouter()

AGENT_SEEDS = [
    ("LANDRY MANAGER", "manager", "Chef de projet : analyse et coordination."),
    ("LANDRY CODER", "coder", "Développeur : implémentation et tests."),
    ("LANDRY REVIEWER", "reviewer", "Auditeur : contrôle qualité et sécurité."),
]


def seed_agents(db: Session) -> None:
    for name, role, description in AGENT_SEEDS:
        if db.scalar(select(Agent).where(Agent.role == role)) is None:
            db.add(Agent(name=name, role=role, description=description))
    db.commit()


@api_router.post("/auth/register", response_model=UserRead, status_code=201, tags=["auth"])
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.scalar(select(User.id).where(User.email == payload.email)):
        raise HTTPException(status_code=409, detail="Cette adresse e-mail est déjà enregistrée")
    user = User(email=payload.email, full_name=payload.full_name, hashed_password=hash_password(payload.password), role="member")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@api_router.post("/auth/login", response_model=Token, tags=["auth"])
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == form.username))
    if user is None or not user.is_active or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides", headers={"WWW-Authenticate": "Bearer"})
    return Token(access_token=create_access_token(user))


@api_router.get("/auth/me", response_model=UserRead, tags=["auth"])
def who_am_i(user: User = Depends(get_current_user)):
    return user


@api_router.get("/agents", response_model=list[AgentRead], tags=["agents"])
def list_agents(db: Session = Depends(get_db), _user: User = Depends(get_current_user)):
    seed_agents(db)
    return db.scalars(select(Agent).order_by(Agent.id)).all()


@api_router.post("/projects", response_model=ProjectRead, status_code=201, tags=["projects"])
def create_project(payload: ProjectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = Project(name=payload.name, description=payload.description, owner_id=user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@api_router.get("/projects", response_model=list[ProjectRead], tags=["projects"])
def list_projects(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = select(Project).order_by(Project.created_at.desc())
    if user.role != "admin":
        query = query.where(Project.owner_id == user.id)
    return db.scalars(query).all()


@api_router.get("/projects/{project_id}", response_model=ProjectRead, tags=["projects"])
def get_project(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return ensure_project_access(project_id, user, db)


@api_router.patch("/projects/{project_id}", response_model=ProjectRead, tags=["projects"])
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = ensure_project_access(project_id, user, db)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project


@api_router.delete("/projects/{project_id}", status_code=204, tags=["projects"])
def delete_project(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = ensure_project_access(project_id, user, db)
    db.delete(project)
    db.commit()


def _get_conversation(conversation_id: int, user: User, db: Session) -> Conversation:
    conversation = db.get(Conversation, conversation_id)
    if conversation is None:
        raise HTTPException(404, "Conversation introuvable")
    if conversation.user_id != user.id and user.role != "admin":
        raise HTTPException(403, "Accès refusé à cette conversation")
    return conversation


@api_router.post("/conversations", response_model=ConversationRead, status_code=201, tags=["conversations"])
def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if payload.project_id is not None:
        ensure_project_access(payload.project_id, user, db)
    agent = db.get(Agent, payload.agent_id)
    if agent is None or not agent.is_active:
        raise HTTPException(404, "Agent introuvable ou inactif")
    conversation = Conversation(title=payload.title, user_id=user.id, agent_id=agent.id, project_id=payload.project_id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


@api_router.get("/conversations", response_model=list[ConversationRead], tags=["conversations"])
def list_conversations(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = select(Conversation).order_by(Conversation.created_at.desc())
    if user.role != "admin":
        query = query.where(Conversation.user_id == user.id)
    return db.scalars(query).all()


@api_router.post("/conversations/{conversation_id}/messages", response_model=MessageRead, status_code=201, tags=["messages"])
def create_message(conversation_id: int, payload: MessageCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    conversation = _get_conversation(conversation_id, user, db)
    message = Message(conversation_id=conversation.id, sender_type="user", content=payload.content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@api_router.get("/conversations/{conversation_id}/messages", response_model=list[MessageRead], tags=["messages"])
def list_messages(conversation_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    _get_conversation(conversation_id, user, db)
    return db.scalars(select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at, Message.id)).all()


@api_router.post("/projects/{project_id}/tasks", response_model=TaskRead, status_code=201, tags=["tasks"])
def create_task(project_id: int, payload: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ensure_project_access(project_id, user, db)
    if payload.assignee_id is not None and db.get(Agent, payload.assignee_id) is None:
        raise HTTPException(404, "Agent introuvable")
    task = Task(project_id=project_id, title=payload.title, description=payload.description, assignee_id=payload.assignee_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@api_router.get("/projects/{project_id}/tasks", response_model=list[TaskRead], tags=["tasks"])
def list_tasks(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ensure_project_access(project_id, user, db)
    return db.scalars(select(Task).where(Task.project_id == project_id).order_by(Task.created_at.desc())).all()


@api_router.patch("/tasks/{task_id}", response_model=TaskRead, tags=["tasks"])
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(404, "Tâche introuvable")
    ensure_project_access(task.project_id, user, db)
    updates = payload.model_dump(exclude_unset=True)
    if "assignee_id" in updates and updates["assignee_id"] is not None and db.get(Agent, updates["assignee_id"]) is None:
        raise HTTPException(404, "Agent introuvable")
    for key, value in updates.items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


@api_router.post("/projects/{project_id}/reviews", response_model=ReviewRead, status_code=201, tags=["reviews"])
def create_review(project_id: int, payload: ReviewCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ensure_project_access(project_id, user, db)
    reviewer = db.scalar(select(Agent).where(Agent.role == "reviewer", Agent.is_active.is_(True)))
    if reviewer is None:
        raise HTTPException(503, "Agent Reviewer non initialisé")
    if payload.task_id is not None:
        task = db.get(Task, payload.task_id)
        if task is None or task.project_id != project_id:
            raise HTTPException(404, "Tâche introuvable dans ce projet")
    review = Review(project_id=project_id, reviewer_agent_id=reviewer.id, task_id=payload.task_id, verdict=payload.verdict, findings=payload.findings)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@api_router.get("/projects/{project_id}/reviews", response_model=list[ReviewRead], tags=["reviews"])
def list_reviews(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ensure_project_access(project_id, user, db)
    return db.scalars(select(Review).where(Review.project_id == project_id).order_by(Review.created_at.desc())).all()


@api_router.get("/projects/{project_id}/progress", response_model=ProjectProgress, tags=["projects"])
def project_progress(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    ensure_project_access(project_id, user, db)
    counts = dict(db.execute(select(Task.status, func.count(Task.id)).where(Task.project_id == project_id).group_by(Task.status)).all())
    total = sum(counts.values())
    completed = counts.get("completed", 0)
    return ProjectProgress(project_id=project_id, total_tasks=total, pending=counts.get("pending", 0), in_progress=counts.get("in_progress", 0), completed=completed, blocked=counts.get("blocked", 0), completion_percent=(completed * 100 / total if total else 0))
