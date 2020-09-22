"""
Unit tests for edly credentials app context_processor
"""
from django.test.client import Client
from django.test import RequestFactory, TestCase

from credentials.apps.core.tests.factories import SiteFactory
from credentials.apps.edx_credentials_extensions.edly_credentials_app.context_processor import edly_app_context
from credentials.apps.edx_credentials_extensions.edly_credentials_app.tests.factories import EdlySiteConfigurationFactory


class EdlyAppContextProcessorTests(TestCase):
    """
    Unit tests for Edly Context processor.
    """

    def setUp(self):
        """
        Create environment for context processor tests.
        """
        super(EdlyAppContextProcessorTests, self).setUp()
        self.request = RequestFactory().get('/')
        self.request.site = SiteFactory()
        self.site_configuration = EdlySiteConfigurationFactory(site=self.request.site)
        self.client = Client(SERVER_NAME=self.request.site.domain)

    def test_default_edly_app_context(self):
        """
        Verify default context values applies correctly.
        """
        expected_context_values = {
            'services_notifications_url': '',
            'session_cookie_domain': '',
            'services_notifications_cookie_expiry': 180,
        }
        actual_context_values = edly_app_context(self.request)
        assert expected_context_values == actual_context_values


    def test_custom_edly_app_context(self):
        """
        Verify custom context values applies correctly.
        """
        test_context_values = {
            'SESSION_COOKIE_DOMAIN': self.request.site.domain,
            'PANEL_NOTIFICATIONS_BASE_URL': 'http://panel.backend.dev.edly.com:9998',
            'SERVICES_NOTIFICATIONS_COOKIE_EXPIRY': 360,
        }

        site_configuration = self.request.site.siteconfiguration
        site_configuration.edly_client_branding_and_django_settings = test_context_values
        site_configuration.save()

        expected_panel_services_notifications_url = '{base_url}/api/v1/all_services_notifications/'.format(
            base_url=test_context_values['PANEL_NOTIFICATIONS_BASE_URL']
        )
        expected_context_values = {
            'session_cookie_domain': test_context_values['SESSION_COOKIE_DOMAIN'],
            'services_notifications_url': expected_panel_services_notifications_url,
            'services_notifications_cookie_expiry': test_context_values['SERVICES_NOTIFICATIONS_COOKIE_EXPIRY'],
        }
        actual_context_values = edly_app_context(self.request)
        assert expected_context_values == actual_context_values
