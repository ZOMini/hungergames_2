"""Initial migration.6

Revision ID: bc847decb549
Revises: 4ab9a04427a9
Create Date: 2023-07-07 21:39:44.036962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc847decb549'
down_revision = '4ab9a04427a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('link_id', sa.UUID(), nullable=True))
        batch_op.drop_constraint('event_url_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'links', ['link_id'], ['id'])
        batch_op.drop_column('url_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url_id', sa.UUID(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('event_url_id_fkey', 'links', ['url_id'], ['id'])
        batch_op.drop_column('link_id')

    # ### end Alembic commands ###