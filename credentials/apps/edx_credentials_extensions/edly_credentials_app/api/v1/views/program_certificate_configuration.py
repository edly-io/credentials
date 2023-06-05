"""
Views for Edly Program Certificate Configuration API.
"""
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from credentials.apps.credentials.models import ProgramCertificate
from credentials.apps.edx_credentials_extensions.edly_credentials_app.api.permissions import CanAccessCurrentSite
from credentials.apps.edx_credentials_extensions.edly_credentials_app.api.serializers import (
    ProgramCertificateConfigurationSerializer,
)


class ProgramCertificateConfigurationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Program Certificate Configuration.
    """
    lookup_field = 'program_uuid'
    lookup_value_regex = '[0-9a-f-]+'
    permission_classes = (IsAuthenticated, CanAccessCurrentSite)
    serializer_class = ProgramCertificateConfigurationSerializer
    queryset = ProgramCertificate.objects.all()

    def update(self, request, *args, **kwargs):
        """
        Update existing Program Certificate Configuration.
        """
        data = request.data.copy()

        signatory_ids = []
        for signatory in data.get('signatories', []):
            signatory_ids.append(signatory.get('id'))

        context = {
            'request': request,
            'signatory_ids': signatory_ids
        }

        instance = ProgramCertificate.objects.get(program_uuid=kwargs.get('program_uuid'))

        serializer = ProgramCertificateConfigurationSerializer(instance, data=data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
