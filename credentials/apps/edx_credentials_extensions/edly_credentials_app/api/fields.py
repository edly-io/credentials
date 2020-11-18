import base64

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """
    Custom serializer field to ingest base64 encoded image.
    """

    def to_internal_value(self, data):
        """
        Save base 64 encoded images.

        SOURCE: http://matthewdaly.co.uk/blog/2015/07/04/handling-images-as-base64-strings-with-django-rest-framework/
        """
        if not data:
            return None

        if isinstance(data, str) and data.startswith('data:image'):
            file_format, image_string = data.split(';base64,')  # format ~= data:image/X;base64,/xxxyyyzzz/
            file_extension = file_format.split('/')[-1]
            data = ContentFile(base64.b64decode(image_string), name='tmp.' + file_extension)

        return super(Base64ImageField, self).to_internal_value(data)
