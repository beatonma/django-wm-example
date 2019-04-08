from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webmention/', include('mentions.urls')),
    path('', include('my_app.urls')),
]
