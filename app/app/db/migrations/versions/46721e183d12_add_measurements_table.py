"""Add measurements table

Revision ID: 46721e183d12
Revises: 
Create Date: 2021-08-15 20:34:40.981780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = "46721e183d12"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "measurements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("device_id", sa.String(length=6), nullable=True),
        sa.Column("co2", sa.Integer(), nullable=True),
        sa.Column("temperature", sa.Numeric(precision=4, scale=2), nullable=True),
        sa.Column("pm2_5", sa.Integer(), nullable=True),
        sa.Column("humidity", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_measurements_device_id"), "measurements", ["device_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_measurements_device_id"), table_name="measurements")
    op.drop_table("measurements")
    # ### end Alembic commands ###
