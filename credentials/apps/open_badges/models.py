### Models for Open Badges
import uuid

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from credentials.apps.credentials.models import AbstractCredential, UserCredential
from openedx_events.learning.data import BadgeData, BadgeTemplateData, UserData, UserPersonalData
from credentials.apps.core.api import get_user_by_username
from credentials.apps.badges.models import BadgeTemplate
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.fields import StatusField



class OpenBadgeTemplate(BadgeTemplate):
    """
    Open Badges Template credential
    """
    
    ORIGIN = "OpenBadge"



class OpenBadge(UserCredential):
    """
    """
    expires_at = models.DateField(null=True)
    
    @property
    def template(self) -> BadgeTemplateData:
        badge_template = self.credential
        template = BadgeTemplateData(
                uuid=str(badge_template.uuid),
                origin=badge_template.origin,
                name=badge_template.name,
                description=badge_template.description,
                image_url=str(badge_template.icon),
            )
        return template
    
    @property
    def user(self) -> UserData:
        user = get_user_by_username(self.username)
        userData = UserData(
                pii=UserPersonalData(
                    username=self.username,
                    email=user.email,
                    name=user.get_full_name(),
                ),
                id=user.lms_user_id,
                is_active=user.is_active,
        )
        return userData
        
    
    def as_badge_data(self) -> BadgeData:
        """
        Represents itself as a BadgeData instance.
        """

        badge_data = BadgeData(
            uuid=str(self.uuid),
            user=self.user,
            template=self.template
        )

        return badge_data
