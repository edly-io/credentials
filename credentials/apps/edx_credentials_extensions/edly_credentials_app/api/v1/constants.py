"""
Constants for Edly Credentials API.
"""
from django.utils.translation import ugettext as _

ERROR_MESSAGES = {
    'CLIENT_SITES_SETUP_SUCCESS': _('Client sites setup successful.'),
    'CLIENT_SITES_SETUP_FAILURE': _('Client sites setup failed.'),
}

CLIENT_SITE_SETUP_FIELDS = [
    'lms_site',
    'credentials_site',
    'wordpress_site',
    'edly_slug',
    'platform_name',
    'discovery_site',
    'theme_dir_name',
    'oauth_clients'
]

EDLY_PANEL_WORKER_USER = 'edly_panel_worker'
