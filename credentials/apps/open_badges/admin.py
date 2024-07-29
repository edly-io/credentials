from django.contrib import admin
from django.http import HttpRequest
from credentials.apps.open_badges.models import OpenBadge, OpenBadgeTemplate
from credentials.apps.badges.models import BadgeProgress, BadgePenalty, BadgeRequirement
from credentials.apps.badges.admin import (
BadgeRequirementAdmin, 
BadgeProgressAdmin,
BadgePenaltyAdmin,
CredlyBadgeTemplateAdmin
)
from credentials.apps.open_badges.toggles import is_open_badges_enabled

class OpenBadgeTemplateAdmin(CredlyBadgeTemplateAdmin):
    
    list_display = (
        "name",
        "uuid",
        "is_active",
        "image",
    )
    list_filter = (
        "is_active",
    )
    readonly_fields = [
        "origin",
        "dashboard_link",
        "image"
    ]
    fieldsets = (
        (
            "Generic",
            {
                "fields": (
                    "site",
                    "is_active",
                ),
                "description": (
                    """
                    WARNING: avoid configuration updates on activated badges.
                    Active badge templates are continuously processed and learners may already have progress on them.
                    Any changes in badge template requirements (including data rules) will affect learners' experience!
                    """
                ),
            },
        ),
        (
            "Badge template",
            {
                "fields": (
                    "uuid",
                    "name",
                    "description",
                    "image",
                    "origin",
                )
            },
        ),
    )

class OpenBadgeAdmin(admin.ModelAdmin):
    
    list_display = (
        "uuid",
        "username",
        "credential",
        "status",
    )
    list_filter = (
        "status",
    )
    search_fields = (
        "username",
    )
    readonly_fields = (
        "credential_id",
        "credential_content_type",
        "username",
        "download_url",
        "uuid",
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

if is_open_badges_enabled():
    admin.site.register(BadgeProgress, BadgeProgressAdmin)
    admin.site.register(BadgePenalty, BadgePenaltyAdmin)
    admin.site.register(BadgeRequirement, BadgeRequirementAdmin)
    admin.site.register(OpenBadge, OpenBadgeAdmin)
    admin.site.register(OpenBadgeTemplate, OpenBadgeTemplateAdmin)
