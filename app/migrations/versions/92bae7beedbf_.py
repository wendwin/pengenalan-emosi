"""empty message

Revision ID: 92bae7beedbf
Revises: 
Create Date: 2024-09-23 12:29:57.879459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92bae7beedbf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jenis_emosi',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jenis', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('laporan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.String(length=50), nullable=True),
    sa.Column('jenis_emosi', sa.String(length=50), nullable=True),
    sa.Column('nama_emosi', sa.String(length=50), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rombel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('materi',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama_emosi', sa.String(length=50), nullable=True),
    sa.Column('jenis_emosi', sa.Integer(), nullable=False),
    sa.Column('gambar_satu', sa.String(length=50), nullable=True),
    sa.Column('gambar_dua', sa.String(length=50), nullable=True),
    sa.Column('vidio', sa.String(length=50), nullable=True),
    sa.Column('emoji', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['jenis_emosi'], ['jenis_emosi.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(length=50), nullable=True),
    sa.Column('rombel_id', sa.Integer(), nullable=False),
    sa.Column('gambar', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['rombel_id'], ['rombel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('materi')
    op.drop_table('rombel')
    op.drop_table('laporan')
    op.drop_table('jenis_emosi')
    # ### end Alembic commands ###
