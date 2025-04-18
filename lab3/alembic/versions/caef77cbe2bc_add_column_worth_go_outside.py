"""add column worth_go_outside

Revision ID: caef77cbe2bc
Revises: 348a1ee9c940
Create Date: 2025-04-16 18:36:44.678866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'caef77cbe2bc'
down_revision: Union[str, None] = '348a1ee9c940'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('air_quality', sa.Column('worth_go_outside', sa.Boolean(), server_default=sa.false(), nullable=False))
    # ### end Alembic commands ###

    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT id, air_quality_us_epa_index, air_quality_gb_defra_index FROM air_quality"))

    for row in result:
        if row.air_quality_us_epa_index <= 2 and row.air_quality_gb_defra_index <= 6:
            conn.execute(sa.text("UPDATE air_quality SET worth_go_outside = :bool WHERE id=:id"),
                         {"id" : row.id, "bool" : True})


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('air_quality', 'worth_go_outside')
    # ### end Alembic commands ###
