"""empty message

Revision ID: 8affd56e5249
Revises: 89af496bf812
Create Date: 2023-12-05 17:24:28.217025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8affd56e5249'
down_revision = '89af496bf812'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('image_file',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.LargeBinary(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('image_file',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(length=20),
               nullable=False)

    # ### end Alembic commands ###
