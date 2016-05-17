"""empty message

Revision ID: 9f1f85ca8a70
Revises: cbf3cfdfded3
Create Date: 2016-05-12 00:06:11.151697

"""

# revision identifiers, used by Alembic.
revision = '9f1f85ca8a70'
down_revision = 'cbf3cfdfded3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hit', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.add_column('rating', sa.Column('timestamp', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rating', 'timestamp')
    op.drop_column('hit', 'timestamp')
    ### end Alembic commands ###