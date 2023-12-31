"""empty message

Revision ID: 62a5d10917a9
Revises: 2da66d124ff5
Create Date: 2023-12-15 08:04:46.777986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62a5d10917a9'
down_revision = '2da66d124ff5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('adlib_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=2000), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('adlib_post')
    # ### end Alembic commands ###
