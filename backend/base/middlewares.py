from django.contrib.auth import get_user_model
from base.models import Config

class CreateAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
    
        User = get_user_model()

        username = "admin"
        password = "admin"

        try:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email="", password=password)
                print("Superuser created.")
        except:
            pass
                
        return self.get_response(request)
    
    
class ConfigsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        configs_defaults = {
            "max_slides_per_run": 10,
            "max_points_per_slide_run": 10,
            "amount_slide_alternatives": 4,
            "difficulty_1_bonus": 1,
            "difficulty_2_bonus": 1,
            "difficulty_3_bonus": 2,
            "difficulty_4_bonus": 3,
            "difficulty_5_bonus": 4,
        }
        
        for config_name, default in configs_defaults.items():
            config = Config.objects.filter(name=config_name).first()
            if not config:
                Config.objects.create(name=config_name, value=default)
            
        
        return self.get_response(request)