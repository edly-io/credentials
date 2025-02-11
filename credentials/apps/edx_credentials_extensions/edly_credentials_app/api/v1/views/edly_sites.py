"""
Views for Edly Site Creation API.
"""
import logging

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from credentials.apps.core.models import SiteConfiguration
from credentials.apps.catalog.models import Course, CourseRun, Organization, Pathway, Program
from credentials.apps.edx_credentials_extensions.edly_credentials_app.api.permissions import CanAccessSiteCreation
from credentials.apps.edx_credentials_extensions.edly_credentials_app.api.v1.constants import ERROR_MESSAGES
from credentials.apps.edx_credentials_extensions.edly_credentials_app.helpers import (
    get_credentials_site_configuration,
    validate_site_configurations,
)

logger = logging.getLogger(__name__)
User = get_user_model()

class EdlySiteViewSet(APIView):
    """
    Creates credentials site and it's site configuration.
    """
    permission_classes = [IsAuthenticated, CanAccessSiteCreation]

    def post(self, request):
        """
        POST /api/edly_api/v1/edly_sites.
        """
        validations_messages = validate_site_configurations(request.data)
        if len(validations_messages) > 0:
            return Response(validations_messages, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.process_client_sites_setup()
            return Response(
                {'success': ERROR_MESSAGES.get('CLIENT_SITES_SETUP_SUCCESS')},
                status=status.HTTP_200_OK
            )
        except TypeError:
            return Response(
                {'error': ERROR_MESSAGES.get('CLIENT_SITES_SETUP_FAILURE')},
                status=status.HTTP_400_BAD_REQUEST
            )

    def process_client_sites_setup(self):
        """
        Process client sites setup and update configurations.
        """
        edly_slug = self.request.data.get('edly_slug', '')
        credentials_base = self.request.data.get('credentials_site', '')
        old_credentials_base = self.request.data.get('old_domain_values', {}).get('credentials_site', None)
        theme_dir_name = self.request.data.get('theme_dir_name', 'openedx')
        lms_url_root = '{protocol}://{lms_url_root}'.format(
            protocol=self.request.data.get('protocol', 'https'),
            lms_url_root=self.request.data.get('lms_site', '')
        )
        catalog_api_url = '{protocol}://{discovery_site}/api/v1/'.format(
            protocol=self.request.data.get('protocol', 'https'),
            discovery_site=self.request.data.get('discovery_site', '')
        )
        wordpress_site = '{protocol}://{wordpress_site}'.format(
            protocol=self.request.data.get('protocol', 'https'),
            wordpress_site=self.request.data.get('wordpress_site', '')
        )
        credentials_site, __ = Site.objects.update_or_create(
            domain=old_credentials_base,
            defaults={'domain': credentials_base, 'name': credentials_base[:50]},
        )
        credentials_site_config, __ = SiteConfiguration.objects.update_or_create(
            site=credentials_site,
            defaults=dict(
                edx_org_short_name=edly_slug,
                platform_name=self.request.data.get('platform_name', ''),
                company_name=self.request.data.get('platform_name', ''),
                theme_name=theme_dir_name,
                lms_url_root=lms_url_root,
                catalog_api_url=catalog_api_url,
                tos_url='{lms_url_root}/tos'.format(lms_url_root=lms_url_root),
                privacy_policy_url='{lms_url_root}/privacy'.format(lms_url_root=lms_url_root),
                homepage_url=wordpress_site,
                certificate_help_url='{wordpress_site}/contact-us'.format(wordpress_site=wordpress_site),
                edly_client_branding_and_django_settings=get_credentials_site_configuration(self.request.data),
            )
        )


class EdlySiteDeletionViewSet(APIView):
    """
    Delete credentials site and it's site configuration.
    """
    permission_classes = [IsAuthenticated, CanAccessSiteCreation]

    def delete_users(self, request):
        """Delete all the sync user for a given site."""
        user_emails = request.data.get('emails')
        user_names = request.data.get('usernames')
        if not all([len(user_emails), len(user_names)]):
            logger.info(f"No user deleted for given site : {(str(request.site))}")
            return 

        users = User.objects.filter(
            email__in=user_emails,
            username__in=user_names
        )
        users.delete()

    def delete_site(self, request):
        """Process site deletion."""
        SiteConfiguration.objects.get(site=request.site).delete()
        request.site.delete()
    
    def process_client_sites_deletion(self, request):
        """
        Process deletion of site and it's configurations, data in a transaction.
        """
        with transaction.atomic():
            self.delete_users(request)
            self.delete_site(request)

    def post(self, request):
        """
        POST /api/edly_api/v1/delete_site
        """
        try:
            self.process_client_sites_deletion(request)
            return Response(
                {'success': 'Successfully deleted site and its configurations.'},
                status=status.HTTP_200_OK
            )
        except TypeError:
            return Response(
                {'error': 'Failed to delete site and its configurations.'},
                status=status.HTTP_400_BAD_REQUEST
            )