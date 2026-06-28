from django.db import models

# Create your models here.
class VoiceAnswer(models.Model):
    request = models.CharField(max_length= 255)
    responce = models.TextField()

    def __str__(self):
        return f"Answer for {self.request}"
    
class AppComand(models.Model):
    name = models.CharField(max_length= 128)
    keyword = models.CharField(max_length= 128)
    path = models.CharField(max_length= 255)

    def __str__(self):
        return f"Activate/Deactivate application {self.name} with command {self.keyword}"

class WebSite(models.Model):
    name = models.CharField(max_length= 128)
    profile = models.CharField(max_length= 128, default= "Default")
    url = models.URLField()


    def __str__(self):
        return f"Website {self.name} with URL {self.url}"
    
class AppGroup(models.Model):
    name = models.CharField(max_length=255)
    apps = models.ManyToManyField(AppComand)
    
    def __str__(self):
        return f"Группа додатків {self.apps.all()}"