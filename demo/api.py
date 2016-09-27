from django.conf.urls import url

from wagtail.api.v2.endpoints import PagesAPIEndpoint as WagtailPagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.wagtailimages.api.v2.endpoints import ImagesAPIEndpoint
from wagtail.wagtaildocs.api.v2.endpoints import DocumentsAPIEndpoint

api_router = WagtailAPIRouter('wagtailapi')


class PagesAPIEndpoint(WagtailPagesAPIEndpoint):
    lookup_field = 'slug'
    lookup_url_kwarg = 'pk'

    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """
        return [
            url(r'^$', cls.as_view({'get': 'listing_view'}), name='listing'),
            url(r'^(?P<pk>[\w-]+)/$', cls.as_view({'get': 'detail_view'}), name='detail'),
        ]


api_router.register_endpoint('pages', PagesAPIEndpoint)
api_router.register_endpoint('images', ImagesAPIEndpoint)
api_router.register_endpoint('documents', DocumentsAPIEndpoint)
