from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.permissions import IsStaff, IsAuthenticated
from rest_framework.response import Response
from credentials.apps.open_badges.models import OpenBadge, OpenBadgeTemplate
from credentials.apps.open_badges.permissions import IsCourseCreator
from credentials.apps.open_badges.serializers import OpenBadgeSerializer, OpenBadgeTemplateSerializer
from credentials.apps.badges.utils import get_badging_event_types, get_event_type_keypaths

class OpenBadgeTemplateViewSet(ModelViewSet):
    
    authentication_classes = []
    permission_classes = []
    serializer_class = OpenBadgeTemplateSerializer
    queryset = OpenBadgeTemplate.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(site=self.request.site, is_active=True)
    
class OpenBadgeViewSet(ModelViewSet):
    authentication_classes = (
        JwtAuthentication,
        SessionAuthentication,
    )
    permission_classes = [IsCourseCreator]
    serializer_class = OpenBadgeSerializer
    queryset = OpenBadge.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_staff:
            queryset = queryset.filter(username=user.username)
        return queryset

class EventTypesView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def get(self, request):
        events = self.get_events_data()
        return Response(events)
    
    def get_events_data(self):
        events = dict()
        events_list = []
        
        badging_events = get_badging_event_types()
        for event in badging_events:
            event_choices = dict()
            event_choices["event"] = event
            event_choices["choices"] = get_event_type_keypaths(event)
            events_list.append(event_choices)
        
        events["events"] = events_list
        return events
