"""empty message

Revision ID: 01e845cf240d
Revises: 5ebde834c7a6
Create Date: 2021-02-12 03:35:55.150307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01e845cf240d'
down_revision = '5ebde834c7a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_user_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_admin_user_model'))
    )
    op.create_index(op.f('ix_admin_user_model_username'), 'admin_user_model', ['username'], unique=True)
    op.drop_index('ix_admin_user_username', table_name='admin_user')
    op.drop_table('admin_user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin_user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_admin_user')
    )
    op.create_index('ix_admin_user_username', 'admin_user', ['username'], unique=True)
    op.drop_index(op.f('ix_admin_user_model_username'), table_name='admin_user_model')
    op.drop_table('admin_user_model')
    # ### end Alembic commands ###
