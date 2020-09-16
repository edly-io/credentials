"""
Unit tests for edly credentials app middlewares.
"""
from testfixtures import LogCapture
from django.conf import settings
from django.contrib import auth
from django.test.client import Client
from django.test import RequestFactory, TestCase
from django.urls import reverse

from credentials.apps.core.models import SiteConfiguration
from credentials.apps.core.tests.factories import UserFactory, SiteFactory
from credentials.apps.edx_credentials_extensions.edly_credentials_app.middleware import logger
from credentials.apps.edx_credentials_extensions.edly_credentials_app.tests.factories import EdlySiteConfigurationFactory


class SettingsOverrideMiddlewareTests(TestCase):
    """
    Tests settings override middleware for sites.
    """
    def setUp(self):
        """
        Create environment for settings override middleware tests.
        """
        super(SettingsOverrideMiddlewareTests, self).setUp()
        self.user = UserFactory(is_superuser=True)
        self.request = RequestFactory().get('/')
        self.request.user = self.user
        self.request.site = SiteFactory()
        self.client = Client(SERVER_NAME=self.request.site.domain)
        self.client.login(username=self.user.username, password='test')
        self.program_records_url = reverse('records:index')
        self.default_settings = {}

    def _assert_settings_values(self, expected_settings_values):
        """
        Checks if current settings values match expected settings values.
        """
        for config_key, expected_config_value in expected_settings_values.items():
            assert expected_config_value == getattr(settings, config_key, None)

    def test_settings_override_middleware_logs_warning_for_empty_override(self):
        """
        Tests "SettingsOverrideMiddleware" logs warning if site configuration has no django settings override values.
        """
        with LogCapture(logger.name) as logs:
            EdlySiteConfigurationFactory(site=self.request.site)
            self.client.get(self.program_records_url)
            logs.check(
                (
                    logger.name,
                    'WARNING',
                    'Site configuration for site ({site}) has no django settings overrides.'.format(site=self.request.site)
                )
            )

    def test_settings_override_middleware_overrides_settings_correctly(self):
        """
        Tests "SettingsOverrideMiddleware" correctly overrides django settings.
        """
        django_override_settings = {
            'SOCIAL_AUTH_EDX_OIDC_SECRET': 'fake-secret',
            'SOCIAL_AUTH_EDX_OIDC_ID_TOKEN_DECRYPTION_KEY': 'fake-key',
            'SOCIAL_AUTH_EDX_OIDC_URL_ROOT': 'fake-url',
            'SOCIAL_AUTH_EDX_OIDC_LOGOUT_URL': 'fake-url',
            'SOCIAL_AUTH_EDX_OIDC_KEY': 'fake-key',
        }
        SiteConfiguration.objects.all().delete()
        EdlySiteConfigurationFactory(
            site=self.request.site,
            edly_client_branding_and_django_settings={
                'DJANGO_SETTINGS_OVERRIDE': django_override_settings
            }
        )
        self._assert_settings_values(self.default_settings)
        self.client.get(self.program_records_url)
        for key in django_override_settings.keys():
            if isinstance(django_override_settings.get(key), (list, tuple)):
                django_override_settings.get(key).extend(getattr(settings, key, None))
        self._assert_settings_values(django_override_settings)

    def test_settings_override_middleware_overrides_settings_correctly_if_list_tuple(self):
        """
        Tests "SettingsOverrideMiddleware" correctly overrides tuple/list django settings.

        Tests if a value being overriden through the middleware is a tuple/list value,
        the value is being extended not replaced.
        """
        django_override_settings = {
            'SOME_TUPLE': (
                'fake-tuple-item',
                'fake-tuple-item',
            ),
            'SOCIAL_AUTH_EDX_OIDC_SECRET': 'fake-secret',
            'SOCIAL_AUTH_EDX_OIDC_ID_TOKEN_DECRYPTION_KEY': 'fake-key',
            'SOCIAL_AUTH_EDX_OIDC_URL_ROOT': 'fake-url',
            'SOCIAL_AUTH_EDX_OIDC_LOGOUT_URL': 'fake-url',
            'SOCIAL_AUTH_EDX_OIDC_KEY': 'fake-key',
        }
        SiteConfiguration.objects.all().delete()
        EdlySiteConfigurationFactory(
            site=self.request.site,
            edly_client_branding_and_django_settings={
                'DJANGO_SETTINGS_OVERRIDE': django_override_settings
            }
        )
        self._assert_settings_values(self.default_settings)
        self.client.get('/', follow=True)
        default_settings = self.default_settings.copy()
        default_settings.get('SOME_TUPLE', []).extend(
            django_override_settings.get('SOME_TUPLE', [])
        )
        self._assert_settings_values(default_settings)
