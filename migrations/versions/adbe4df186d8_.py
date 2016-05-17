"""empty message

Revision ID: adbe4df186d8
Revises: fbb9bb2e95ee
Create Date: 2016-05-06 10:26:25.805897

"""

# revision identifiers, used by Alembic.
revision = 'adbe4df186d8'
down_revision = 'fbb9bb2e95ee'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('card_cvv', sa.Integer(), nullable=True),
    sa.Column('card_type', sa.String(length=12), nullable=True),
    sa.Column('expire_month', sa.String(length=10), nullable=True),
    sa.Column('expire_year', sa.Integer(), nullable=True),
    sa.Column('payment_method', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('card_association',
    sa.Column('users_id', sa.Integer(), nullable=True),
    sa.Column('card_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['card_id'], ['card.id'], ),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], )
    )
    op.drop_column(u'payment', 'card_type')
    op.drop_column(u'payment', 'expire_year')
    op.drop_column(u'payment', 'card_cvv')
    op.drop_column(u'payment', 'expire_month')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'payment', sa.Column('expire_month', sa.VARCHAR(length=10), autoincrement=False, nullable=True))
    op.add_column(u'payment', sa.Column('card_cvv', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column(u'payment', sa.Column('expire_year', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column(u'payment', sa.Column('card_type', sa.VARCHAR(length=12), autoincrement=False, nullable=True))
    op.drop_table('card_association')
    op.drop_table('card')
    ### end Alembic commands ###
