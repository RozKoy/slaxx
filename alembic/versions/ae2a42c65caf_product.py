"""product

Revision ID: ae2a42c65caf
Revises: 
Create Date: 2023-12-17 19:01:48.657091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae2a42c65caf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "product",
        sa.Column(
            "id", sa.Integer, autoincrement=True, nullable=False, primary_key=True
        ),
        sa.Column("price", sa.Integer, nullable=False),
        sa.Column("stock", sa.Integer, nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("image", sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("product")