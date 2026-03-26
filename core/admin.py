from django.contrib import admin
from .models import VoiceAnswer, AppComand
# Register your models here.

admin.site.register([VoiceAnswer, AppComand])