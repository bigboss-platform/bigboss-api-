from app.shared.base_schema import BigBossBaseSchema, BigBossReadSchema


class TenantThemeReadSchema(BigBossReadSchema):
    tenant_id: str
    primary_color: str
    primary_color_hover: str
    secondary_color: str
    background_color: str
    surface_color: str
    text_primary_color: str
    text_secondary_color: str
    font_family_url: str
    font_family_name: str
    logo_url: str
    favicon_url: str
    primary_button_text_color: str
    loading_screen_background_color: str


class TenantThemeUpdateSchema(BigBossBaseSchema):
    primary_color: str = ""
    primary_color_hover: str = ""
    secondary_color: str = ""
    background_color: str = ""
    surface_color: str = ""
    text_primary_color: str = ""
    text_secondary_color: str = ""
    font_family_url: str = ""
    font_family_name: str = ""
    logo_url: str = ""
    favicon_url: str = ""
    primary_button_text_color: str = ""
    loading_screen_background_color: str = ""


class TenantSettingsReadSchema(BigBossReadSchema):
    tenant_id: str
    business_name: str
    business_address: str
    business_lat: float
    business_lng: float
    whatsapp_number: str
    whatsapp_message_template: str
    max_delivery_radius_km: float
    instagram_url: str
    facebook_url: str
    tiktok_url: str
    twitter_url: str
    payment_instructions: str


class TenantSettingsUpdateSchema(BigBossBaseSchema):
    business_name: str = ""
    business_address: str = ""
    business_lat: float = 0.0
    business_lng: float = 0.0
    whatsapp_number: str = ""
    whatsapp_message_template: str = ""
    max_delivery_radius_km: float = 5.0
    instagram_url: str = ""
    facebook_url: str = ""
    tiktok_url: str = ""
    twitter_url: str = ""
    payment_instructions: str = ""
