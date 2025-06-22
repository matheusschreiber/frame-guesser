from django.contrib.auth import get_user_model

User = get_user_model()

username = "admin"
password = "admin"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email="", password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")