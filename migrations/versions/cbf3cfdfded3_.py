"""empty message

Revision ID: cbf3cfdfded3
Revises: be371e0ba082
Create Date: 2016-05-10 07:04:10.141522

"""

# revision identifiers, used by Alembic.
revision = 'cbf3cfdfded3'
down_revision = 'be371e0ba082'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sessions')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sessions',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('session_id', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.Column('data', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('expiry', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'sessions_pkey'),
    sa.UniqueConstraint('session_id', name=u'sessions_session_id_key')
    )
    ### end Alembic commands ###
