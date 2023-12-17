"""order

Revision ID: fddf61fab894
Revises: e530b4660113
Create Date: 2023-12-17 23:03:22.109047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fddf61fab894'
down_revision: Union[str, None] = 'e530b4660113'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "order",
        sa.Column(
            "id", sa.Integer, autoincrement=True, nullable=False, primary_key=True
        ),
        sa.Column("status", sa.String(255), nullable=False),
        sa.Column("item_count", sa.Integer, nullable=False),
        sa.Column("price_count", sa.Integer, nullable=False),
        sa.Column("create_at", sa.String(255), nullable=False),
        sa.Column(
            "customerId",
            sa.Integer,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["customerId"],
            ["user.id"],
            name="fk_customerId",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )


def downgrade() -> None:
    op.drop_table("order")
