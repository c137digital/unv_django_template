from django.contrib import admin

from .models import BusinessModel, ClientModel

# class AuthorAdmin(admin.ModelAdmin):
#     pass

admin.site.register(BusinessModel)
admin.site.register(ClientModel)
