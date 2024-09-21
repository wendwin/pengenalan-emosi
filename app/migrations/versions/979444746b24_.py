"""empty message

Revision ID: 979444746b24
Revises: 
Create Date: 2024-09-20 21:24:57.341497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '979444746b24'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('materi', schema=None) as batch_op:
        batch_op.add_column(sa.Column('jenis_emosi', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'jenis_emosi', ['jenis_emosi'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('materi', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('jenis_emosi')

    # ### end Alembic commands ###
