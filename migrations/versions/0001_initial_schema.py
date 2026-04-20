"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-16 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tenants",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("product", sa.String(50), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )
    op.create_index("ix_tenants_slug", "tenants", ["slug"], unique=True, schema="public")

    op.create_table(
        "tenant_themes",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("tenant_id", sa.String(), nullable=False),
        sa.Column("primary_color", sa.String(7), server_default="#000000"),
        sa.Column("primary_color_hover", sa.String(7), server_default="#333333"),
        sa.Column("secondary_color", sa.String(7), server_default="#ffffff"),
        sa.Column("background_color", sa.String(7), server_default="#ffffff"),
        sa.Column("surface_color", sa.String(7), server_default="#f5f5f5"),
        sa.Column("text_primary_color", sa.String(7), server_default="#212121"),
        sa.Column("text_secondary_color", sa.String(7), server_default="#757575"),
        sa.Column("font_family_url", sa.Text(), server_default=""),
        sa.Column("font_family_name", sa.String(100), server_default="system-ui"),
        sa.Column("logo_url", sa.Text(), server_default=""),
        sa.Column("favicon_url", sa.Text(), server_default=""),
        sa.Column("primary_button_text_color", sa.String(7), server_default="#ffffff"),
        sa.Column(
            "loading_screen_background_color", sa.String(7), server_default="#000000"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )
    op.create_index(
        "ix_tenant_themes_tenant_id", "tenant_themes", ["tenant_id"], schema="public"
    )

    op.create_table(
        "tenant_settings",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("tenant_id", sa.String(), nullable=False),
        sa.Column("business_name", sa.String(200), server_default=""),
        sa.Column("business_address", sa.Text(), server_default=""),
        sa.Column("business_lat", sa.Numeric(10, 7), server_default="0"),
        sa.Column("business_lng", sa.Numeric(10, 7), server_default="0"),
        sa.Column("whatsapp_number", sa.String(20), server_default=""),
        sa.Column("whatsapp_message_template", sa.Text(), server_default=""),
        sa.Column("max_delivery_radius_km", sa.Numeric(5, 2), server_default="5"),
        sa.Column("instagram_url", sa.Text(), server_default=""),
        sa.Column("facebook_url", sa.Text(), server_default=""),
        sa.Column("tiktok_url", sa.Text(), server_default=""),
        sa.Column("twitter_url", sa.Text(), server_default=""),
        sa.Column(
            "payment_instructions",
            sa.Text(),
            server_default="El staff coordinará el pago.",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )
    op.create_index(
        "ix_tenant_settings_tenant_id",
        "tenant_settings",
        ["tenant_id"],
        unique=True,
        schema="public",
    )

    op.create_table(
        "tenant_admins",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("tenant_id", sa.String(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(
            ["tenant_id"],
            ["public.tenants.id"],
            name="fk_tenant_admins_tenant_id",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="public",
    )
    op.create_index(
        "ix_tenant_admins_tenant_id", "tenant_admins", ["tenant_id"], schema="public"
    )
    op.create_index(
        "ix_tenant_admins_email",
        "tenant_admins",
        ["email"],
        unique=True,
        schema="public",
    )

    op.create_table(
        "otp_verifications",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(20), nullable=False),
        sa.Column("code_hash", sa.String(64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_used", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_otp_verifications_phone_number", "otp_verifications", ["phone_number"]
    )

    op.create_table(
        "end_users",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("phone_number", sa.String(20), nullable=False),
        sa.Column("name", sa.String(200), server_default=""),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("consent_accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_end_users_phone_number", "end_users", ["phone_number"])

    op.create_table(
        "menus",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("tenant_id", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_menus_tenant_id", "menus", ["tenant_id"])

    op.create_table(
        "menu_sections",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("menu_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="0"),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true()),
        sa.ForeignKeyConstraint(
            ["menu_id"], ["menus.id"], name="fk_menu_sections_menu_id"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "menu_items",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("section_id", sa.String(), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), server_default=""),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("photo_url", sa.Text(), server_default=""),
        sa.Column("sort_order", sa.Integer(), server_default="0"),
        sa.Column("is_available", sa.Boolean(), server_default=sa.true()),
        sa.ForeignKeyConstraint(
            ["section_id"], ["menu_sections.id"], name="fk_menu_items_section_id"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("end_user_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending"),
        sa.Column("delivery_type", sa.String(20), nullable=False),
        sa.Column("delivery_address", sa.Text(), server_default=""),
        sa.Column("delivery_lat", sa.Numeric(10, 7), server_default="0"),
        sa.Column("delivery_lng", sa.Numeric(10, 7), server_default="0"),
        sa.Column("delivery_cost", sa.Numeric(10, 2), server_default="0"),
        sa.Column("subtotal", sa.Numeric(10, 2), nullable=False),
        sa.Column("total", sa.Numeric(10, 2), nullable=False),
        sa.Column("notes", sa.Text(), server_default=""),
        sa.Column(
            "payment_status", sa.String(50), nullable=False, server_default="pending"
        ),
        sa.Column("payment_method", sa.String(200), server_default=""),
        sa.Column("payment_amount_received", sa.Numeric(10, 2), server_default="0"),
        sa.Column("payment_reference", sa.String(200), server_default=""),
        sa.Column("payment_notes", sa.Text(), server_default=""),
        sa.Column("payment_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("payment_updated_by", sa.String(), server_default=""),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_orders_end_user_id", "orders", ["end_user_id"])

    op.create_table(
        "order_items",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("order_id", sa.String(), nullable=False),
        sa.Column("menu_item_id", sa.String(), nullable=False),
        sa.Column("menu_item_name", sa.String(200), nullable=False),
        sa.Column("menu_item_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("note", sa.Text(), server_default=""),
        sa.ForeignKeyConstraint(
            ["order_id"], ["orders.id"], name="fk_order_items_order_id"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("order_items")
    op.drop_index("ix_orders_end_user_id", table_name="orders")
    op.drop_table("orders")
    op.drop_table("menu_items")
    op.drop_table("menu_sections")
    op.drop_index("ix_menus_tenant_id", table_name="menus")
    op.drop_table("menus")
    op.drop_index("ix_end_users_phone_number", table_name="end_users")
    op.drop_table("end_users")
    op.drop_index(
        "ix_otp_verifications_phone_number", table_name="otp_verifications"
    )
    op.drop_table("otp_verifications")
    op.drop_index(
        "ix_tenant_admins_email", table_name="tenant_admins", schema="public"
    )
    op.drop_index(
        "ix_tenant_admins_tenant_id", table_name="tenant_admins", schema="public"
    )
    op.drop_table("tenant_admins", schema="public")
    op.drop_index(
        "ix_tenant_settings_tenant_id", table_name="tenant_settings", schema="public"
    )
    op.drop_table("tenant_settings", schema="public")
    op.drop_index(
        "ix_tenant_themes_tenant_id", table_name="tenant_themes", schema="public"
    )
    op.drop_table("tenant_themes", schema="public")
    op.drop_index("ix_tenants_slug", table_name="tenants", schema="public")
    op.drop_table("tenants", schema="public")
