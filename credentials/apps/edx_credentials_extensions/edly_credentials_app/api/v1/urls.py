from rest_framework import routers

from credentials.apps.edx_credentials_extensions.edly_credentials_app.api.v1.views.program_certificate_configuration import ProgramCertificateConfigurationViewSet


router = routers.SimpleRouter()
router.register(r'program-certificate-configuration', ProgramCertificateConfigurationViewSet, base_name='program-certificate-configuration')

urlpatterns = router.urls
