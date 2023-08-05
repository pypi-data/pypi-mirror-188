"""empty message

Revision ID: 5b0fcbb94f24
Revises: 772a5e43f05b
Create Date: 2019-03-14 00:53:39.326495

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5b0fcbb94f24"
down_revision = "772a5e43f05b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "notification",
        "comment_id",
        existing_type=postgresql.UUID(),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "notification",
        "comment_id",
        existing_type=postgresql.UUID(),
        nullable=False,
    )
    # ### end Alembic commands ###
