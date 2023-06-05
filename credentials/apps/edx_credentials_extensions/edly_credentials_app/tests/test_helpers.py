import pytest
from django.test import RequestFactory, TestCase

from credentials.apps.core.tests.factories import SiteFactory
from credentials.apps.edx_credentials_extensions.edly_credentials_app.helpers import (
    get_credentials_site_configuration,
    validate_site_configurations,
)


@pytest.mark.django_db
class EdlyAppHelperMethodsTests(TestCase):
    """
    Unit tests for helper methods.
    """

    def setUp(self):
        super(EdlyAppHelperMethodsTests, self).setUp()
        self.request = RequestFactory().get('/')
        self.request.site = SiteFactory()
        self.request_data = dict(
            lms_site='example.lms',
            credentials_site='example.credentials',
            wordpress_site='example.wordpress',
            edly_slug='edx',
            platform_name='Edly',
            discovery_site='example.discovery',
            theme_dir_name='openedx',
            language_code='en',
            oauth2_clients={
                'credentials-sso': {
                    'id': 'credentials-sso-key',
                    'secret': 'credentials-sso-secret'
                },
                'credentials-backend': {
                    'id': 'credentials-backend-key',
                    'secret': 'credentials-backend-secret'
                }
            },
        )

    def test_validate_site_configurations(self):
        """
        Test that required site creation data is present in request data.
        """
        lms_site = self.request_data.pop('lms_site')
        validation_messages = validate_site_configurations(self.request_data)
        expected_message = 'Lms Site is Missing'
        assert validation_messages.get('lms_site') == expected_message

        self.request_data['lms_site'] = lms_site
        validation_messages = validate_site_configurations(self.request_data)
        assert not validation_messages

    def test_get_credentials_site_configuration(self):
        """
        Test that correct credentials site configuration data is returned using the request data.
        """
        protocol = self.request_data.get('protocol', 'https')
        lms_site = self.request_data.get('lms_site', '')
        lms_site_with_protocol = '{protocol}://{lms_root_domain}'.format(
            protocol=protocol,
            lms_root_domain=lms_site,
        )
        oauth2_clients = self.request_data.get('oauth2_clients', {})
        credentials_sso_values = oauth2_clients.get('credentials-sso', {})
        credentials_backend_values = oauth2_clients.get('credentials-backend', {})
        language_code = self.request_data.get("language_data", 'en')
        expected_site_configuration = {
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
                'LANGUAGE_CODE': language_code,
            }
        }

        credentials_site_configuration = get_credentials_site_configuration(self.request_data)
        for key, value in credentials_site_configuration.items():
            assert expected_site_configuration[key] == value
