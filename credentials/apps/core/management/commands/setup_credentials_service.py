""" Management command to set up credentials service locally"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from credentials.apps.core.models import SiteConfiguration


class Command(BaseCommand):
    help = 'Set up credentials service locally.'
    domain_name = 'edx.devstack.lms:18150'

    def setup_credentials_service(self):
        site, _ = Site.objects.get_or_create(name=self.domain_name, domain=self.domain_name)
        SiteConfiguration.objects.get_or_create(
            site=site,
            edx_org_short_name='edly',
            platform_name='Edly',
            company_name='Edly',
            lms_url_root='http://edx.devstack.lms:18000/',
            catalog_api_url='http://edx.devstack.lms:18381/api/v1/',
            tos_url='http://edx.devstack.lms:18000/tos',
            privacy_policy_url='http://edx.devstack.lms:18000/privacy-policy',
            homepage_url='http://edx.devstack.lms:18000/',
            certificate_help_url='http://edx.devstack.lms:18000/',

            edly_client_branding_and_django_settings=
            {
                "DJANGO_SETTINGS_OVERRIDE": {
                    "SOCIAL_AUTH_EDX_OAUTH2_KEY": "credentials-sso-key",
                    "SOCIAL_AUTH_EDX_OAUTH2_SECRET": "credentials-sso-secret",
                    "SOCIAL_AUTH_EDX_OAUTH2_ISSUER": "http://edx.devstack.lms:18000",
                    "SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT": "http://edx.devstack.lms:18000",
                    "SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT": "http://edx.devstack.lms:18000",
                    "SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL": "http://edx.devstack.lms:18000/logout",
                    "BACKEND_SERVICE_EDX_OAUTH2_KEY": "credentials-backend-service-key",
                    "BACKEND_SERVICE_EDX_OAUTH2_SECRET": "credentials-backend-service-secret",
                    "BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL": "http://edx.devstack.lms:18000"
                }
            }
        )

    def handle(self, *args, **options):
        """Set up credentials service locally."""
        self.setup_credentials_service()
