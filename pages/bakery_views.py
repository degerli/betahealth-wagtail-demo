from exporter.views import BakeryView
from .models import SimplePage


class SimplePageStatic(BakeryView):
    bakery_model = SimplePage
