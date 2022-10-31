"""create user table

Revision ID: 29728760e826
Revises: 
Create Date: 2022-10-31 13:27:54.311376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29728760e826'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
    sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
    sa.Column("email", sa.String(), nullable=False, unique=True),
    sa.Column("password", sa.String(), nullable=False),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()"))
    )


def downgrade():
    op.drop_table("users")

