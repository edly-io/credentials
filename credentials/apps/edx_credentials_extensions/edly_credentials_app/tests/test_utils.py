"""
Tests for Edly Utils Functions.
"""
from unittest import TestCase

import jwt
import mock
import pytest
from django.conf import settings
from django.test.client import RequestFactory
from mock import MagicMock

from credentials.apps.core.tests.factories import SiteFactory, UserFactory
from credentials.apps.edx_credentials_extensions.edly_credentials_app.tests.factories import (
    EdlySiteConfigurationFactory,
)
from credentials.apps.edx_credentials_extensions.edly_credentials_app.utils import (
    encode_edly_user_info_cookie,
    decode_edly_user_info_cookie,
    get_edx_org_from_cookie,
    user_has_edx_organization_access,
)


@pytest.mark.django_db
class UtilsTests(TestCase):
    """
    Tests for utility methods.
    """

    def setUp(self):
        """
        Setup initial test data
        """
        super(UtilsTests, self).setUp()
        self.user = UserFactory()
        self.admin_user = UserFactory(is_staff=True)
        self.request = RequestFactory().get('/')
        self.request.user = self.user
        self.request.session = self._get_stub_session()
        self.request.site = SiteFactory()
        self.request.site.siteconfiguration = EdlySiteConfigurationFactory(
            site=self.request.site,
            edx_org_short_name='cloudX'
        )

        self.test_edly_user_info_cookie_data = {
            'edly-org': 'edly',
            'edly-sub-org': 'cloud',
            'edx-org': 'cloudX'
        }

    def _get_stub_session(self, expire_at_browser_close=False, max_age=604800):
        return MagicMock(
            get_expire_at_browser_close=lambda: expire_at_browser_close,
            get_expiry_age=lambda: max_age,
        )

    def _copy_cookies_to_request(self, request):
        edly_cookie_string = encode_edly_user_info_cookie((self.test_edly_user_info_cookie_data))
        request.COOKIES = {
            settings.EDLY_USER_INFO_COOKIE_NAME: edly_cookie_string
        }

    def test_encode_edly_user_info_cookie(self):
        """
        Test that "encode_edly_user_info_cookie" method encodes data correctly.
        """
        actual_encoded_string = encode_edly_user_info_cookie(self.test_edly_user_info_cookie_data)
        expected_encoded_string = jwt.encode(
            self.test_edly_user_info_cookie_data, settings.EDLY_COOKIE_SECRET_KEY,
            algorithm=settings.EDLY_JWT_ALGORITHM
        )

        assert actual_encoded_string == expected_encoded_string

    def test_decode_edly_user_info_cookie(self):
        """
        Test that "decode_edly_user_info_cookie" method decodes data correctly.
        """
        encoded_data = jwt.encode(
            self.test_edly_user_info_cookie_data,
            settings.EDLY_COOKIE_SECRET_KEY,
            algorithm=settings.EDLY_JWT_ALGORITHM
        )
        decoded_edly_user_info_cookie_data = decode_edly_user_info_cookie(encoded_data)

        assert self.test_edly_user_info_cookie_data == decoded_edly_user_info_cookie_data

    def test_get_edx_org_from_cookie(self):
        """
        Test that "get_edx_org_from_cookie" method returns edx-org short name correctly.
        """
        edly_user_info_cookie = encode_edly_user_info_cookie(self.test_edly_user_info_cookie_data)

        assert self.request.site.siteconfiguration.edx_org_short_name == get_edx_org_from_cookie(edly_user_info_cookie)

    def test_user_with_edx_organization_access(self):
        """
        Test user has edx organization access of a site.
        """
        with mock.patch('credentials.apps.edx_credentials_extensions.edly_credentials_app.utils.get_current_site') as current_site:
            current_site.return_value = self.request.site
            self._copy_cookies_to_request(self.request)

            assert user_has_edx_organization_access(self.request) is True

    def test_user_without_edx_organization_access(self):
        """
        Test user does not have edx organization access of a site.
        """
        with mock.patch('credentials.apps.edx_credentials_extensions.edly_credentials_app.utils.get_current_site') as current_site:
            current_site.return_value = self.request.site
            self.request.site.siteconfiguration = EdlySiteConfigurationFactory()

            assert user_has_edx_organization_access(self.request) is False
