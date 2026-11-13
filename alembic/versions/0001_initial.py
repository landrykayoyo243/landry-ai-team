"""Initial schema and default agents.

Revision ID: 0001_initial
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(320), nullable=False), sa.Column("full_name", sa.String(160), nullable=False), sa.Column("hashed_password", sa.String(255), nullable=False), sa.Column("role", sa.String(32), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("agents", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(80), nullable=False, unique=True), sa.Column("role", sa.String(32), nullable=False, unique=True), sa.Column("description", sa.Text(), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_table("projects", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(160), nullable=False), sa.Column("description", sa.Text(), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_projects_owner_id", "projects", ["owner_id"])
    op.create_table("conversations", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(200), nullable=False), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("agent_id", sa.Integer(), sa.ForeignKey("agents.id", ondelete="RESTRICT"), nullable=False), sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_conversations_user_id", "conversations", ["user_id"])
    op.create_table("messages", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False), sa.Column("sender_type", sa.String(16), nullable=False), sa.Column("content", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_messages_conversation_id", "messages", ["conversation_id"])
    op.create_table("tasks", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(200), nullable=False), sa.Column("description", sa.Text(), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False), sa.Column("assignee_id", sa.Integer(), sa.ForeignKey("agents.id", ondelete="SET NULL"), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_tasks_project_id", "tasks", ["project_id"])
    op.create_table("reviews", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("verdict", sa.String(16), nullable=False), sa.Column("findings", sa.Text(), nullable=False), sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False), sa.Column("reviewer_agent_id", sa.Integer(), sa.ForeignKey("agents.id", ondelete="RESTRICT"), nullable=False), sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_reviews_project_id", "reviews", ["project_id"])
    op.bulk_insert(sa.table("agents", sa.column("name", sa.String), sa.column("role", sa.String), sa.column("description", sa.Text), sa.column("is_active", sa.Boolean), sa.column("created_at", sa.DateTime), sa.column("updated_at", sa.DateTime)), [
        {"name": "LANDRY MANAGER", "role": "manager", "description": "Chef de projet : analyse et coordination.", "is_active": True, "created_at": sa.func.now(), "updated_at": sa.func.now()},
        {"name": "LANDRY CODER", "role": "coder", "description": "Développeur : implémentation et tests.", "is_active": True, "created_at": sa.func.now(), "updated_at": sa.func.now()},
        {"name": "LANDRY REVIEWER", "role": "reviewer", "description": "Auditeur : contrôle qualité et sécurité.", "is_active": True, "created_at": sa.func.now(), "updated_at": sa.func.now()},
    ])


def downgrade() -> None:
    for table in ("reviews", "tasks", "messages", "conversations", "projects", "agents", "users"):
        op.drop_table(table)
