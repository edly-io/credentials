"""
Edly's Custom permissions classes for use with DRF.
"""
import logging

from rest_framework import permissions

from credentials.apps.edx_credentials_extensions.edly_credentials_app.utils import user_has_edx_organization_access

logger = logging.getLogger(__name__)


class CanAccessCurrentSite(permissions.BasePermission):
    """
    Permission to check if the current site is allowed for the user.
    """

    def has_permission(self, request, view):
        """
        Checks for user's permission for current site.
        """
        if user_has_edx_organization_access(request):
            return True

        return False
