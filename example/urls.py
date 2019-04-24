from .local_settings import ADMIN_URL
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(f'{ADMIN_URL}/', admin.site.urls),
    path('webmention/', include('mentions.urls')),
    path('', include('my_app.urls')),
]
