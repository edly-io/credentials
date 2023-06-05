"""
Serializers for edly_api.
"""
from django.contrib.sites.models import Site
from rest_framework import serializers

from credentials.apps.credentials.models import ProgramCertificate, Signatory
from credentials.apps.edx_credentials_extensions.edly_credentials_app.api.fields import Base64ImageField


class SignatorySerializer(serializers.ModelSerializer):
    """
    Serializer for Signatory.
    """
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Signatory
        fields = ['id', 'name', 'title', 'image']


class ProgramCertificateConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer for Program Certificate Configuration.
    """
    site = serializers.SlugRelatedField(slug_field='domain', queryset=Site.objects.all())
    signatories = SignatorySerializer(many=True)

    class Meta:
        model = ProgramCertificate
        fields = [
            'site', 'is_active', 'signatories', 'program_uuid', 'use_org_name',
            'include_hours_of_effort', 'language',
        ]

    def create(self, validated_data):
        signatories = []
        for signatory in validated_data.pop('signatories', []):
            signatories.append(Signatory.objects.create(**signatory))

        program_certificate_configuration = ProgramCertificate(**validated_data)
        program_certificate_configuration.save()
        program_certificate_configuration.signatories.set(signatories)
        return program_certificate_configuration

    def update(self, instance, validated_data):
        signatory_ids = self.context.get('signatory_ids', [])

        signatories = []
        for signatory_index, signatory in enumerate(validated_data.pop('signatories', [])):
            signatory_obj, _ = Signatory.objects.update_or_create(
                pk=signatory_ids[signatory_index],
                defaults=signatory
            )
            signatories.append(signatory_obj)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        instance.signatories.set(signatories)
        return instance
