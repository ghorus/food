"""empty message

Revision ID: c4142dc028bc
Revises: 2bed72873533
Create Date: 2023-12-12 18:20:49.488146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4142dc028bc'
down_revision = '2bed72873533'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game__room__members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('game__room', schema=None) as batch_op:
        batch_op.add_column(sa.Column('room_link', sa.String(length=4), nullable=False))
        batch_op.drop_column('host_id')
        batch_op.drop_column('messages')
        batch_op.drop_column('members')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game__room', schema=None) as batch_op:
        batch_op.add_column(sa.Column('members', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('messages', sa.VARCHAR(length=200), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('host_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('room_link')

    op.drop_table('game__room__members')
    # ### end Alembic commands ###