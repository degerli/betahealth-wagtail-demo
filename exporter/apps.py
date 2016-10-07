from django.apps import AppConfig
from exporter.signal_handlers import register_signal_handlers


class ExporterConfig(AppConfig):
    name = 'exporter'

    def ready(self):
        register_signal_handlers()
