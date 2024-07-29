from rest_framework import serializers
from datetime import date
from credentials.apps.badges.models import BadgeRequirement, DataRule
from credentials.apps.open_badges.models import OpenBadge, OpenBadgeTemplate
        

class DataRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRule
        fields = ("data_path", "operator", "value")
        
class BadgeRequirementSerializer(serializers.ModelSerializer):
    rules = DataRuleSerializer(many=True)
    class Meta:
        model = BadgeRequirement
        fields = (
            "event_type",
            "description",
            "blend",
            "rules",
        )
    def create(self, validated_data):
        data_rule_data = validated_data.pop('rules')
        requirement = BadgeRequirement.objects.create(**validated_data)
        for data_rule in data_rule_data:
            DataRule.objects.create(requirement=requirement, **data_rule)
        return requirement
    
class OpenBadgeTemplateSerializer(serializers.ModelSerializer):
    requirements = BadgeRequirementSerializer(many=True)
    class Meta:
        model = OpenBadgeTemplate
        fields = (
            "name",
            "description",
            "icon",
            "requirements",
        )
        read_only_fields = ("state",)
        
    def create(self, validated_data):
        requirement_data = validated_data.pop('requirements')
        template = OpenBadgeTemplate.objects.create(**validated_data)
        for requirement in requirement_data:
            requirement_serializer = BadgeRequirementSerializer(data=requirement)
            if not requirement_serializer.is_valid():
                serializers.ValidationError("Please enter the correct data!")
            requirement_serializer.save(template=template)
        return template
        
class OpenBadgeSerializer(serializers.ModelSerializer):
    credential = OpenBadgeTemplateSerializer(many=False)
    class Meta:
        model = OpenBadge
        fields = (
            "credential_id",
            "credential",
            "username",
            "status",
            "expires_at"
        )
    
    def create(self, validated_data):
        credential_data = validated_data.pop('credential')
        credential = OpenBadgeTemplate.objects.create(**credential)
        requirement = OpenBadge.objects.create(credential=credential, **validated_data)
        return requirement
    
    def validate_expires_at(self, value):
        """
        Check that the expiration_date is set in the future.
        """
        if value <= date.today():
            raise serializers.ValidationError("Expiration date must be in the future.")
        return value
