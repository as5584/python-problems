"""Initial schema for books and issues

Revision ID: 001
Revises:
Create Date: 2026-07-08

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("id", sa.String(length=10), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=False),
        sa.Column("isbn", sa.String(length=20), nullable=False),
        sa.Column("total_copies", sa.Integer(), nullable=False),
        sa.Column("available_copies", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("isbn"),
    )
    op.create_table(
        "issues",
        sa.Column("issue_id", sa.String(length=10), nullable=False),
        sa.Column("book_id", sa.String(length=10), nullable=False),
        sa.Column("book_title", sa.String(length=255), nullable=False),
        sa.Column("borrower_name", sa.String(length=255), nullable=False),
        sa.Column("borrower_id", sa.String(length=50), nullable=False),
        sa.Column("issue_date", sa.Date(), nullable=False),
        sa.Column("return_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(["book_id"], ["books.id"]),
        sa.PrimaryKeyConstraint("issue_id"),
        sa.UniqueConstraint("issue_id", name="uq_issues_issue_id"),
    )


def downgrade() -> None:
    op.drop_table("issues")
    op.drop_table("books")