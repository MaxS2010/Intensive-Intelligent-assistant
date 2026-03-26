from django.core.management.base import BaseCommand
import speech_recognition, platform, os, psutil, subprocess

from utils.voice_answers import run_voice
from utils.close_programs import get_open_programs, close_unwanted_programs
from core.models import AppComand, VoiceAnswer
from utils.find_path import find_path

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Assistent started... "))
        recognizer = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()
        with microphone as source:
            self.stdout.write("Wait for tune your voice...")
            recognizer.adjust_for_ambient_noise(source= source)
            self.stdout.write(self.style.SUCCESS("Ready to talk..."))
            while True:
                try:
                    audio = recognizer.listen(source= source, phrase_time_limit= 5)
                    text_command = recognizer.recognize_google(audio, language= "uk-UA") # type: ignore
                    self.stdout.write(f"You say: {text_command}")
                    self.run_commands(text_command= text_command)
                except speech_recognition.UnknownValueError:
                    continue
                except Exception as error:
                    self.stdout.write(self.style.WARNING(f"Error: {error}"))

    def run_commands(self, text_command: str):
        if "відкрий" in text_command.lower():
            all_commands = AppComand.objects.all()
            user_app = None

            for command in all_commands:
                    if command.keyword.lower() in text_command.lower():
                        user_app = command
                        break

            if user_app:
                if user_app.path:
                    run_voice(f"Відкриваю {user_app.name}")
                    self.open_app(path_app= user_app.path)
                else:
                    run_voice(f"Шукаю шлях до {user_app.name}")
                    path= find_path(filename= user_app.name)
                    if path:
                        run_voice(f"Шлях знайдено")
                        self.open_app(path_app= path)
                        user_app.path = path
                        user_app.save()
                    else:
                        run_voice("Шлях до цієї програми не знайдено")
            else:
                run_voice("Такої програми не знайдено")
        if "help" in text_command.lower() or "команди" in text_command.lower():
            self.command_help()

        if "stop" in text_command.lower() or "стоп" in text_command.lower():
            self.stop_assistant()
        
        
        else:
            answers = VoiceAnswer.objects.all()

            for answer in answers:
                if answer.request.lower() in text_command.lower():
                    user_app = text_command
                    break


            
    def open_app(self, path_app: str):
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(filepath= path_app)
            elif system == "Darwin":
                subprocess.Popen(["open", path_app])
            else:
                subprocess.Popen(path_app)
        except Exception as error:
            self.stdout.write(self.style.WARNING(f"Error: {error}"))

    def stop_assistant(self):
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'].lower() == 'python.exe' and proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline']).lower()
                    if 'run_assistant' in cmdline:
                        proc.kill()
                        print(f"Ассистент зупинен (PID: {proc.info['pid']})")
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
        
    def command_help(self):
        run_voice("Ось команди які я можу виконувати: Додати команду, Відкрий 'Назва додатку', Відкриті програми, Зачинити програми, Стоп")

        self.stdout.write("Список можливих дій: \n - Додати команду \n - Відкрий 'Назва додатку' \n Зачинити програми \n Стоп")
        for app_command in AppComand.objects.all():
            self.stdout.write(f"Ключове слово - {app_command.keyword}, Назва додатку - {app_command.name}")
            self.stdout.write("\nГолосові запити: ")
        for voice_answer in VoiceAnswer.objects.all():
            self.stdout.write(f' {voice_answer.request}')











    """
    if "програми" in text_command.lower():
                    open_progs = get_open_programs()
                    print(f"Відчинені додатки: {open_progs}")
                    run_voice("Відчинені додатки")
    if "зачинити" in text_command.lower() or "close" in text_command.lower():
        open_progs = get_open_programs()
        allowed = ['widgets.exe', 'sppsvc.exe', 'gamebarftserver.exe', 'chrome.exe', 'widgetservice.exe', 'gamebar.exe']
        close_unwanted_programs(allowed, open_progs)
        run_voice("Додатки закриті")
                
    """