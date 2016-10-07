import json
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.http import HttpResponse

from bakery.views import BuildableDetailView

from wagtail.wagtailcore.middleware import SiteMiddleware


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)


class BakeryView(JSONResponseMixin, BuildableDetailView):
    """
    An abstract class that can be inherited to create a buildable view that can be
    added to BAKERY_VIEWS setting. An inheriting class should define a bakery_model
    property pointing to a Wagtail Page model.

    Example:

        # File: app/models.py

        from wagtail.wagtailcore.pages import Page

        class AuthorPage(Page):
            bakery_views = ('app.bakery_views.AuthorPage',)
            ...

        # File: app/bakery_views.py

        from wagtail.wagtailbakery.views import BakeryView
        from . import models

        class AuthorPage(BakeryView):
            bakery_model = models.AuthorPage

        # File: project/settings.py:

        BAKERY_VIEWS = (
            'app.bakery_views.AuthorPage',
            ...
        )

        BUILD_DIR = os.path.join(PROJECT_ROOT, 'baked')

    Build command:

        python manage.py build app.bakery_views.AuthorPage

    """

    bakery_model = None

    def get_queryset(self):
        """
        Defines get_queryset() for BuildableDetailView to return a
        QuerySet containing all live Wagtail Page models
        """
        return self.bakery_model.objects.live()

    def get(self, request):
        """
        Overrides DetailView's get() to return TemplateResponse from serve()
        after passing request through Wagtail SiteMiddleware
        """
        smw = SiteMiddleware()
        smw.process_request(request)
        view_func, view_args, view_kwargs = resolve(request.path)
        return view_func(request, **view_kwargs)

    def get_content(self):
        """
        Overrides BuildableMixin's get_content() to work with
        both TemplateRespose and HttpResponse
        """
        response = self.get(self.request)
        if hasattr(response, 'render'):
            response = response.render()
        return response.content

    def get_url(self, obj):
        """
        Overrides BuildableDetailView's get_url() to return a url from the
        Page model url_path property
        """
        return reverse('wagtailapi:pages:detail', kwargs={'pk': obj.pk})

    def get_build_path(self, obj):
        """
        Used to determine where to build the detail page. Override this if you
        would like your detail page at a different location. By default it
        will be built at get_url() + "index.html"
        """
        import os
        from django.conf import settings

        path = os.path.join(settings.BUILD_DIR, self.get_url(obj)[1:])
        os.path.exists(path) or os.makedirs(path)
        return os.path.join(path, 'manifest.json')

    class Meta:
        abstract = True
