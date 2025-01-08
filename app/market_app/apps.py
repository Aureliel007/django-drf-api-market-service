from django.apps import AppConfig


class MarketAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'market_app'

    def ready(self):
        import market_app.signals
