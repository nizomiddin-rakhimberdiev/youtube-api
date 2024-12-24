from django.contrib import admin
from .models import Subscription, Channel, CustomUser, Video

# Register your models here.
admin.site.register(Subscription)

admin.site.register(Channel)

admin.site.register(CustomUser)

admin.site.register(Video)