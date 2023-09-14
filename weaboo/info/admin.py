from django.contrib import admin
from .models import CustomUser, ListType, UserShowList

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ListType)
admin.site.register(UserShowList)
