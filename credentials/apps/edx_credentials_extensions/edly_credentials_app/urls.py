from django.conf.urls import include, url

urlpatterns = [
    url('', include('credentials.apps.edx_credentials_extensions.edly_credentials_app.api.urls')),
]
