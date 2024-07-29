
from django.urls import path, include
from rest_framework import routers

from credentials.apps.open_badges.views import OpenBadgeTemplateViewSet, OpenBadgeViewSet, EventTypesView


router = routers.DefaultRouter()
router.register(r'openbadges', OpenBadgeViewSet)
router.register(r'openbadgetemplates', OpenBadgeTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('event-types', EventTypesView.as_view())
]
