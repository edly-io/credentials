import logging

import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from credentials.apps.core.models import SiteConfiguration


LOGGER = logging.getLogger(__name__)


def user_has_edx_organization_access(request):
    """
    Check if the user can access the requested URL by verifying its linked edx organization.

    This method checks if the "edx_org_short_name" related to the requested URL's site
    matches with the "edx-org" in the "edly_user_info" cookie.

    Arguments:
        request: HTTP request object

    Returns:
        bool: Returns True if user has edX organization access otherwise False.
    """

    if request.user.is_superuser or request.user.is_staff:
        return True

    current_site = get_current_site(request)
    try:
        current_site_configuration = current_site.siteconfiguration
    except SiteConfiguration.DoesNotExist:
        LOGGER.warning('Site (%s) has no related site configuration.', current_site)
        return False

    edly_user_info_cookie = request.COOKIES.get(settings.EDLY_USER_INFO_COOKIE_NAME, None)
    if current_site_configuration.edx_org_short_name == get_edx_org_from_cookie(edly_user_info_cookie):
        return True

    return False


def encode_edly_user_info_cookie(cookie_data):
    """
    Encode edly_user_info cookie data into JWT string.

    Arguments:
        cookie_data (dict): Edly user info cookie dict.

    Returns:
        string
    """
    return jwt.encode(cookie_data, settings.EDLY_COOKIE_SECRET_KEY, algorithm=settings.EDLY_JWT_ALGORITHM)


def decode_edly_user_info_cookie(encoded_cookie_data):
    """
    Decode edly_user_info cookie data from JWT string.

    Arguments:
        encoded_cookie_data (dict): Edly user info cookie JWT encoded string.

    Returns:
        dict
    """
    return jwt.decode(encoded_cookie_data, settings.EDLY_COOKIE_SECRET_KEY, algorithms=[settings.EDLY_JWT_ALGORITHM])


def get_edx_org_from_cookie(encoded_cookie_data):
    """
    Returns edx-org short name from the edly-user-info cookie.

    Arguments:
        encoded_cookie_data (dict): Edly user info cookie JWT encoded string.

    Returns:
        string
    """

    if not encoded_cookie_data:
        return ''

    decoded_cookie_data = decode_edly_user_info_cookie(encoded_cookie_data)
    return decoded_cookie_data['edx-org']
