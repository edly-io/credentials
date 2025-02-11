from django.conf.urls import url
from rest_framework import routers

from credentials.apps.edx_credentials_extensions.edly_credentials_app.api.v1.views.edly_sites import (
    EdlySiteViewSet, EdlySiteDeletionViewSet
)
from credentials.apps.edx_credentials_extensions.edly_credentials_app.api.v1.views.program_certificate_configuration import (
    ProgramCertificateConfigurationViewSet
) 


router = routers.SimpleRouter()
router.register(r'program-certificate-configuration', ProgramCertificateConfigurationViewSet, basename='program-certificate-configuration')

urlpatterns = [
    url(r'^edly_sites/', EdlySiteViewSet.as_view(), name='edly_sites'),
    url(r'^delete_site/', EdlySiteDeletionViewSet.as_view(), name='delete_site')
]

urlpatterns += router.urls
