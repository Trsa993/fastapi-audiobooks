"""add books table

Revision ID: 453c890e2704
Revises: 29728760e826
Create Date: 2022-10-31 14:09:44.226039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '453c890e2704'
down_revision = '29728760e826'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('img', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###
