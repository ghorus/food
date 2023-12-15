"""empty message

Revision ID: ccc4a7252fa0
Revises: 56dd7e96b563
Create Date: 2023-12-14 17:57:26.609916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccc4a7252fa0'
down_revision = '56dd7e96b563'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game__room', schema=None) as batch_op:
        batch_op.add_column(sa.Column('turn', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game__room', schema=None) as batch_op:
        batch_op.drop_column('turn')

    # ### end Alembic commands ###