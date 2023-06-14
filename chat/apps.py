from django.apps import AppConfig

class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    def ready(self):
        
        # from .models import ChatRooms
        print("runserver")        
        # ChatRooms.objects.all().delete()