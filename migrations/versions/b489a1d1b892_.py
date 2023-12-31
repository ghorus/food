"""empty message

Revision ID: b489a1d1b892
Revises: 2973381ae903
Create Date: 2023-12-05 13:15:03.981229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b489a1d1b892'
down_revision = '2973381ae903'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('upload',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=50), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('upload')
    # ### end Alembic commands ###
