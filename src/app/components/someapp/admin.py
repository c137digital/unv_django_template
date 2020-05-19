from ..django.admin import admin

from .models import BusinessModel, ClientModel


admin.register(BusinessModel)
admin.register(ClientModel)
