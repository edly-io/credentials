from credentials.apps.edx_credentials_extensions.edly_credentials_app.api.v1.constants import CLIENT_SITE_SETUP_FIELDS


def validate_site_configurations(request_data):
    """
    Identify missing required fields for client's site setup.

    Arguments:
        request_data (dict): Request data passed for site setup

    Returns:
        validation_messages (dict): Missing fields information
    """

    validation_messages = {}

    for field in CLIENT_SITE_SETUP_FIELDS:
        if not request_data.get(field, None):
            validation_messages[field] = '{0} is Missing'.format(field.replace('_', ' ').title())

    return validation_messages


def get_credentials_site_configuration(request_data):
    """
    Prepare Credentials Site Configurations for Client based on Request Data.

    Arguments:
        request_data (dict): Request data passed for site setup

    Returns:
        (dict): Credentials Site Configuration
    """
    protocol = request_data.get('protocol', 'https')
    lms_site = request_data.get('lms_site', '')
    lms_site_with_protocol = '{protocol}://{lms_root_domain}'.format(
        protocol=protocol,
        lms_root_domain=lms_site,
    )
    oauth2_clients = request_data.get('oauth2_clients', {})
    credentials_sso_values = oauth2_clients.get('credentials-sso', {})
    credentials_backend_values = oauth2_clients.get('credentials-backend', {})

    return {
        'DJANGO_SETTINGS_OVERRIDE': {
            'SOCIAL_AUTH_EDX_OAUTH2_KEY': credentials_sso_values.get('id', ''),
            'SOCIAL_AUTH_EDX_OAUTH2_SECRET': credentials_sso_values.get('secret', ''),
            'SOCIAL_AUTH_EDX_OAUTH2_ISSUER': lms_site_with_protocol,
            'SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT': lms_site_with_protocol,
            'SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT': lms_site_with_protocol,
            'SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL': '{lms_site_with_protocol}/logout'.format(
                lms_site_with_protocol=lms_site_with_protocol
            ),
            'BACKEND_SERVICE_EDX_OAUTH2_KEY': credentials_backend_values.get('id', ''),
            'BACKEND_SERVICE_EDX_OAUTH2_SECRET': credentials_backend_values.get('secret', ''),
            'BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL': '{lms_site_with_protocol}/oauth2'.format(
                lms_site_with_protocol=lms_site_with_protocol
            ),
            'LANGUAGE_CODE': request_data.get('language_code', 'en'),
        }
    }
