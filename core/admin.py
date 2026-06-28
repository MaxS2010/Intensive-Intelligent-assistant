from django.contrib import admin
from .models import VoiceAnswer, AppComand, AppGroup, WebSite
# Register your models here.

admin.site.register([VoiceAnswer, AppComand, AppGroup, WebSite])