"""Add columns for Person to store fido devices informations

Revision ID: 956659992419
Revises: 42ec83db6a01
Create Date: 2023-01-04 15:20:26.590297

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "956659992419"
down_revision = "42ec83db6a01"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "person", sa.Column("fido_enabled", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "person",
        sa.Column(
            "fido_credentials",
            sa.ARRAY(postgresql.JSONB(astext_type=sa.Text())),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("person", "fido_credentials")
    op.drop_column("person", "fido_enabled")
    # ### end Alembic commands ###
