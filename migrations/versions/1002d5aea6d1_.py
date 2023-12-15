"""empty message

Revision ID: 1002d5aea6d1
Revises: d9de2be72a65
Create Date: 2023-12-12 21:45:15.904273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1002d5aea6d1'
down_revision = 'd9de2be72a65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game__room__messages', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'user', ['member_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('game__room__messages', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###