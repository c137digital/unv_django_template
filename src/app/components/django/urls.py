from django.urls import path, include

from .admin import admin


urlpatterns = [
    path('admin/', admin.urls),

    # include app urls
    # path('', include('app.components.business.urls')),
]
