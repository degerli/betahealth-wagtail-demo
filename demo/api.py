from django.core.urlresolvers import reverse

from rest_framework import serializers

from wagtail.api.v2.endpoints import PagesAPIEndpoint as WagtailPagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.wagtailimages.api.v2.endpoints import ImagesAPIEndpoint as WagtailImagesAPIEndpoint
from wagtail.wagtailimages.api.v2.serializers import ImageSerializer as WagtailImageSerializer
from wagtail.wagtailimages.utils import generate_signature
from wagtail.wagtaildocs.api.v2.endpoints import DocumentsAPIEndpoint

api_router = WagtailAPIRouter('wagtailapi')


class PagesAPIEndpoint(WagtailPagesAPIEndpoint):
    meta_fields = WagtailPagesAPIEndpoint.meta_fields + [
        'url_path'
    ]

    listing_default_fields = WagtailPagesAPIEndpoint.listing_default_fields + [
        'url_path'
    ]


def generate_image_url(image, filter_spec):
    signature = generate_signature(image.id, filter_spec)
    url = reverse('wagtailimages_serve', args=(signature, image.id, filter_spec))

    # Append image's original filename to the URL (optional)
    url += image.file.name[len('original_images/'):]

    return url


class ImageSerializer(WagtailImageSerializer):
    def _get_url_x(self, obj, width):
        return generate_image_url(obj, 'width-{}'.format(width))

    def get_url_400(self, obj):
        return self._get_url_x(obj, 400)

    def get_url_640(self, obj):
        return self._get_url_x(obj, 640)

    def get_url_800(self, obj):
        return self._get_url_x(obj, 800)

    def get_url_1280(self, obj):
        return self._get_url_x(obj, 1280)

    url_400 = serializers.SerializerMethodField()
    url_640 = serializers.SerializerMethodField()
    url_800 = serializers.SerializerMethodField()
    url_1280 = serializers.SerializerMethodField()


class ImagesAPIEndpoint(WagtailImagesAPIEndpoint):
    base_serializer_class = ImageSerializer
    meta_fields = WagtailImagesAPIEndpoint.meta_fields + [
        'url_400', 'url_640', 'url_800', 'url_1280'
    ]


api_router.register_endpoint('pages', PagesAPIEndpoint)
api_router.register_endpoint('images', ImagesAPIEndpoint)
api_router.register_endpoint('documents', DocumentsAPIEndpoint)
