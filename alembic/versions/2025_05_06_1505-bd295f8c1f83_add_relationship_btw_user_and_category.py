"""Add relationship btw user and category

Revision ID: bd295f8c1f83
Revises: 1e0c8776f623
Create Date: 2025-05-06 15:05:13.745624

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bd295f8c1f83"
down_revision: Union[str, None] = "1e0c8776f623"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("categories") as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=False))
        batch_op.create_foreign_key("user_id", "categories", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("categories") as batch_op:
        batch_op.drop_constraint("user_id", type_="foreignkey")
        batch_op.drop_column("user_id")
    # ### end Alembic commands ###
