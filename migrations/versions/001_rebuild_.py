"""empty message

Revision ID: 001_rebuild
Revises: 
Create Date: 2021-03-13 02:28:38.285883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_rebuild'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('association')
    op.add_column('restaurants', sa.Column('deliveroo_url', sa.String(), nullable=True))
    op.add_column('restaurants', sa.Column('justeat_url', sa.String(), nullable=True))
    op.add_column('restaurants', sa.Column('latitude', sa.Float(), nullable=False))
    op.add_column('restaurants', sa.Column('longitude', sa.Float(), nullable=False))
    op.add_column('restaurants', sa.Column('profile_image_url', sa.String(), nullable=True))
    op.add_column('restaurants', sa.Column('ubereats_url', sa.String(), nullable=True))
    op.create_index(op.f('ix_restaurants_name'), 'restaurants', ['name'], unique=False)
    op.add_column('tags', sa.Column('icon', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tags', 'icon')
    op.drop_index(op.f('ix_restaurants_name'), table_name='restaurants')
    op.drop_column('restaurants', 'ubereats_url')
    op.drop_column('restaurants', 'profile_image_url')
    op.drop_column('restaurants', 'longitude')
    op.drop_column('restaurants', 'latitude')
    op.drop_column('restaurants', 'justeat_url')
    op.drop_column('restaurants', 'deliveroo_url')
    op.create_table('association',
    sa.Column('restaurant_id', sa.INTEGER(), nullable=False),
    sa.Column('tag_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], name='fk_association_restaurant_id_restaurants'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name='fk_association_tag_id_tags'),
    sa.PrimaryKeyConstraint('restaurant_id', 'tag_id', name='pk_association')
    )
    # ### end Alembic commands ###
