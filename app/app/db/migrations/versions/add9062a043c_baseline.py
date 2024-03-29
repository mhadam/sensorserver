"""baseline

Revision ID: add9062a043c
Revises: 
Create Date: 2021-09-25 20:26:11.699050

"""
import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic

revision = "add9062a043c"
down_revision = None
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "measurements",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
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

    op.create_table(
        "device_block",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("device_id", sa.Text(), nullable=False),
        sa.Column("ip_address", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("device_id", "ip_address"),
    )
    op.create_index(
        op.f("ix_device_block_device_id"), "device_block", ["device_id"], unique=False
    )
    op.create_table(
        "device_request",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("device_id", sa.Text(), nullable=False),
        sa.Column("ip_address", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("device_id", "ip_address"),
    )
    op.create_index(
        op.f("ix_device_request_device_id"),
        "device_request",
        ["device_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_measurements_device_id"), "measurements", ["device_id"], unique=False
    )

    create_updated_at_trigger()
    op.create_table(
        "users",
        sa.Column("id", fastapi_users_db_sqlalchemy.GUID(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=72), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_table(
        "device_auth",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("device_id", sa.Text(), nullable=False),
        sa.Column("user_id", fastapi_users_db_sqlalchemy.GUID(), nullable=False),
        sa.Column("ip_address", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("device_id", "ip_address"),
    )
    op.create_index(
        op.f("ix_device_auth_device_id"), "device_auth", ["device_id"], unique=False
    )
    # ### end Alembic commands ###
    for table in ["device_auth", "device_block", "device_request", "users"]:
        op.execute(
            f"""
            CREATE TRIGGER update_user_modtime
                BEFORE UPDATE
                ON {table}
                FOR EACH ROW
            EXECUTE PROCEDURE update_updated_at_column();
            """
        )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_device_auth_device_id"), table_name="device_auth")
    op.drop_table("device_auth")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_measurements_device_id"), table_name="measurements")
    op.drop_table("measurements")
    op.drop_index(op.f("ix_device_request_device_id"), table_name="device_request")
    op.drop_table("device_request")
    op.drop_index(op.f("ix_device_block_device_id"), table_name="device_block")
    op.drop_table("device_block")
    # ### end Alembic commands ###
