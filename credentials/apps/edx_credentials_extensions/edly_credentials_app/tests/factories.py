import factory

from credentials.apps.core.tests.factories import SiteConfigurationFactory


class EdlySiteConfigurationFactory(SiteConfigurationFactory):

    @factory.lazy_attribute
    def edly_client_branding_and_django_settings(self):
        return {}
