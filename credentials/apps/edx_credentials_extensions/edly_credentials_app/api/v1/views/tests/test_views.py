"""
Tests for edly_api Views.
"""
import json

from django.contrib.sites.models import Site
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from credentials.apps.catalog.tests.factories import ProgramFactory
from credentials.apps.core.models import SiteConfiguration
from credentials.apps.core.tests.factories import UserFactory
from credentials.apps.core.tests.mixins import SiteMixin
from credentials.apps.credentials.tests.factories import ProgramCertificateFactory
from credentials.apps.edx_credentials_extensions.edly_credentials_app.api.v1.constants import (
    CLIENT_SITE_SETUP_FIELDS,
    EDLY_PANEL_WORKER_USER,
)

JSON_CONTENT_TYPE = 'application/json'


def get_test_image_as_base_64_encoded_string():
    base64_header = 'data:image/png;base64,'
    base64_data = (
        'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY'
        '42YAAAAASUVORK5CYII='
    )
    base64_full = base64_header + base64_data
    return base64_full


class ProgramCertificateConfigurationTests(SiteMixin, APITestCase):
    """
    Test for Program Certificate Configuration Viewset.
    """

    def setUp(self):
        super(ProgramCertificateConfigurationTests, self).setUp()
        self.list_url = reverse('edly_api:program-certificate-configuration-list')

        self.user = UserFactory(is_staff=True, is_superuser=True)

        program = ProgramFactory(site=self.site)
        self.test_data = {
            'site': self.site.domain,
            'is_active': True,
            'signatories': [
                {
                    'name': 'Jhon Doe',
                    'title': 'Test Certificate',
                    'image': get_test_image_as_base_64_encoded_string()
                }
            ],
            'program_uuid': str(program.uuid),
            'use_org_name': True,
            'include_hours_of_effort': True,
            'language': 'en'
        }

    def test_create_program_certificate_configuration(self):
        """
        Verify program certificate configuration creation.
        """
        response = self.client.post(self.list_url, data=json.dumps(self.test_data), content_type=JSON_CONTENT_TYPE)
        assert response.status_code == 401

        self.client.login(username=self.user.username, password='password')
        response = self.client.post(self.list_url, data=json.dumps(self.test_data), content_type=JSON_CONTENT_TYPE)
        assert response.status_code == 201

    def test_update_program_certificate_configuration(self):
        """
        Verify program certificate configuration update.
        """
        program_certificate_configuration = ProgramCertificateFactory()

        self.detail_url = reverse('edly_api:program-certificate-configuration-detail',
                                  kwargs={'program_uuid': str(program_certificate_configuration.program_uuid)})
        test_data = self.test_data
        test_data['signatories'] = []
        test_data['is_active'] = False

        response = self.client.patch(self.detail_url, data=json.dumps(test_data), content_type=JSON_CONTENT_TYPE)
        assert response.status_code == 401

        self.client.login(username=self.user.username, password='password')
        response = self.client.patch(self.detail_url, data=json.dumps(test_data), content_type=JSON_CONTENT_TYPE)
        assert response.status_code == 200

    def test_list_program_certificate_configuration(self):
        """
        Verify list program certificate configuration.
        """
        program_certificate_configuration = ProgramCertificateFactory()

        response = self.client.get(self.list_url)
        assert response.status_code == 401

        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.list_url)
        assert response.status_code == 200

        actual_data = response.json()
        actual_data = actual_data.get('results')[0]
        assert str(program_certificate_configuration.program_uuid) == actual_data.get('program_uuid')


class EdlySiteViewSet(APITestCase):
    """
    Unit tests for EdlySiteViewSet viewset.
    """

    def setUp(self):
        """
        Prepare environment for tests.
        """
        super(EdlySiteViewSet, self).setUp()
        self.admin_user = UserFactory(is_staff=True, username=EDLY_PANEL_WORKER_USER)
        self.edly_sites_url = reverse('edly_api:edly_sites')
        self.client.force_authenticate(self.admin_user)
        self.request_data = dict(
            lms_site='example.lms',
            credentials_site='example.credentials',
            wordpress_site='example.wordpress',
            edly_slug='edx',
            platform_name='Edly',
            discovery_site='example.discovery',
            theme_dir_name='openedx',
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

    def test_without_authentication(self):
        """
        Verify authentication is required when accessing the endpoint.
        """
        self.client.logout()
        response = self.client.post(self.edly_sites_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_without_permission(self):
        """
        Verify panel permission is required when accessing the endpoint.
        """
        user = UserFactory()
        self.client.logout()
        self.client.force_authenticate(user)
        response = self.client.post(self.edly_sites_url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_request_data_validation(self):
        """
        Verify validation messages in response for missing required data.
        """
        response = self.client.post(self.edly_sites_url, data={})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert set(response.json().keys()) == set(CLIENT_SITE_SETUP_FIELDS)

    def test_client_setup(self):
        """
        Verify successful client setup with correct data.
        """
        response = self.client.post(self.edly_sites_url, data=self.request_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        credentials_site = Site.objects.get(domain=self.request_data.get('credentials_site', ''))
        assert credentials_site.siteconfiguration
        assert credentials_site.siteconfiguration.edly_client_branding_and_django_settings

    def test_client_setup_idempotent(self):
        """
        Test that the values are only update not created on multiple API calls.
        """
        response = self.client.post(self.edly_sites_url, data=self.request_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        credentials_site = Site.objects.get(domain=self.request_data.get('credentials_site', ''))
        assert credentials_site.siteconfiguration

        sites_count = Site.objects.all().count()
        site_configurations_count = SiteConfiguration.objects.all().count()
        response = self.client.post(self.edly_sites_url, data=self.request_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert Site.objects.all().count() == sites_count
        assert SiteConfiguration.objects.all().count() == site_configurations_count
