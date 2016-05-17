"""empty message

Revision ID: 3c590cabb190
Revises: 76e55d3e06eb
Create Date: 2016-05-15 16:40:03.180723

"""

# revision identifiers, used by Alembic.
revision = '3c590cabb190'
down_revision = '76e55d3e06eb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('urole', sa.String(length=80), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'urole')
    ### end Alembic commands ###