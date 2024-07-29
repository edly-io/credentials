from credentials.apps.badges.issuers import BadgeTemplateIssuer
from credentials.apps.open_badges.models import OpenBadgeTemplate, OpenBadge

class OpenBadgeTemplateIssuer(BadgeTemplateIssuer):
    
    issued_credential_type = OpenBadgeTemplate
    issued_user_credential_type = OpenBadge
