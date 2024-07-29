from django.http import Http404
from rest_framework import permissions

class IsCourseCreator(permissions.DjangoModelPermissions):
    
    def has_permission(self, request, view):
        import pdb; pdb.set_trace()
        return super().has_permission(request, view)
