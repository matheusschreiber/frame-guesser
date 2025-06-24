from django.contrib.auth import get_user_model

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