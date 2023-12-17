"""orderlist

Revision ID: b38edaaf84e5
Revises: fddf61fab894
Create Date: 2023-12-18 02:49:06.960796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b38edaaf84e5'
down_revision: Union[str, None] = 'fddf61fab894'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "order_list",
        sa.Column(
            "id", sa.Integer, autoincrement=True, nullable=False, primary_key=True
        ),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("price_count", sa.Integer, nullable=False),
        sa.Column("orderId", sa.Integer, nullable=False),
        sa.Column("productId", sa.Integer, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["orderId"],
            ["order.id"],
            name="fk_orderId",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["productId"],
            ["product.id"],
            name="fk_productId",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )


def downgrade() -> None:
    op.drop_table("order_list")
