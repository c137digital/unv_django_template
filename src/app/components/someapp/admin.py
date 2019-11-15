from django.contrib import admin

from .models import BusinessModel, ClientModel

admin.site.register(BusinessModel)
admin.site.register(ClientModel)
