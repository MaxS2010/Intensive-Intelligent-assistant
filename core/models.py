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
        return f"Activate {self.name} with command {self.keyword}"
