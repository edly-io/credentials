from django.conf.urls import include, url

urlpatterns = [
    url(r'^v1/', include('credentials.apps.edx_credentials_extensions.edly_credentials_app.api.v1.urls')),
]
