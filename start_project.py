import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Voice_Assistant.settings")

django.setup()

call_command("rus_assistant")