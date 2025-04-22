# produccion_inventario/apps.py
from django.apps import AppConfig

class ProduccionInventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'produccion_inventario'

    def ready(self):
        import produccion_inventario.signals  # Importa las señales