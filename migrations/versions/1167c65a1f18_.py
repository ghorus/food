"""empty message

Revision ID: 1167c65a1f18
Revises: e4865bdce05c
Create Date: 2023-12-16 11:43:24.863527

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1167c65a1f18'
down_revision = 'e4865bdce05c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('adlib__post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('authors', sa.String(length=30), nullable=False),
    sa.Column('content', sa.String(length=2000), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game__room',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('room_link', sa.String(length=4), nullable=False),
    sa.Column('turn', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('game__room__members',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.String(length=4), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('game__room__messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('member_message', sa.String(length=50), nullable=False),
    sa.Column('room_id', sa.String(length=4), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('content', sa.String(length=2000), nullable=False),
    sa.Column('city', sa.String(length=200), nullable=False),
    sa.Column('datePosted', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profile__pic__upload',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=50), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_adlib_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('adlib_post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['adlib_post_id'], ['adlib__post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('food__post__upload',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=50), nullable=True),
    sa.Column('data', sa.LargeBinary(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('adlib_post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('adlib_post',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    sa.Column('authors', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('content', sa.VARCHAR(length=2000), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='adlib_post_pkey')
    )
    op.drop_table('user_post')
    op.drop_table('food__post__upload')
    op.drop_table('user_adlib_post')
    op.drop_table('profile__pic__upload')
    op.drop_table('post')
    op.drop_table('game__room__messages')
    op.drop_table('game__room__members')
    op.drop_table('user')
    op.drop_table('game__room')
    op.drop_table('adlib__post')
    # ### end Alembic commands ###
