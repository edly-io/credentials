"""
Tests for edly_api Views.
"""
import json

from django.urls import reverse

from rest_framework.test import APITestCase

from credentials.apps.catalog.tests.factories import ProgramFactory
from credentials.apps.core.tests.factories import UserFactory
from credentials.apps.core.tests.mixins import SiteMixin
from credentials.apps.credentials.tests.factories import ProgramCertificateFactory

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
