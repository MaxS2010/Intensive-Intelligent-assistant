from django.core.management.base import BaseCommand
import speech_recognition, platform, os, psutil, subprocess

from utils.voice_answers import run_voice
from utils.close_programs import get_open_programs, close_unwanted_programs
from core.models import AppComand, AppGroup, VoiceAnswer, WebSite
from utils.find_path import find_path
from utils.add_command import add_command
from utils.run_sites import open_folder, open_site_in_profile

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Асистент запущений..."))

        recognizer = speech_recognition.Recognizer()
        microphone = speech_recognition.Microphone()

        self.run = True

        with microphone as source:
            self.stdout.write("Почекайте, налаштовую фоновий шум...")
            recognizer.adjust_for_ambient_noise(source= source)
            self.stdout.write(self.style.SUCCESS("Слухаю вас..."))

            while self.run:
                try:
                    audio = recognizer.listen(source= source, phrase_time_limit= 5)
                    text_command = recognizer.recognize_google(audio, language= "uk-UA") # type: ignore
                    self.run_commands(text_command= text_command, source= source)
                    self.stdout.write(f"Ви сказали: {text_command}")
                except speech_recognition.UnknownValueError:
                    continue
                except Exception as error:
                    self.stdout.write(self.style.WARNING(f"Error: {error}"))

    def run_commands(self, text_command: str, source):                    
        if "відкрити сайт" in text_command.lower():
            sites = []
            for site in WebSite.objects.all():
                if site.name.lower() in text_command.lower():
                    sites.append(site)
            
            if not sites:
                run_voice('Сайт не знайдено')
            elif len(sites) == 1:
                run_voice(f'Відкриваю сайт {sites[0].name}')
                print(sites[0].profile)
                open_site_in_profile(sites[0].profile, sites[0].url)
            else:
                run_voice('Відкриваю всі сайти')
                for site in sites:
                    open_site_in_profile(site.profile, site.url)

        if "відкрити" in text_command.lower() or "закрити" in text_command.lower():
            all_commands = AppComand.objects.all()
            list_apps = []

            for command in all_commands:
                    if command.keyword.lower() in text_command.lower():
                        list_apps.append(command)
            
            if "групу" in text_command.lower():
                for group in AppGroup.objects.all():
                    if group.name.lower() in text_command.lower():
                        list_apps.extend(group.apps.all())

            if list_apps:
                if len(list_apps) > 1:
                    if "відкрити" in text_command.lower():
                        run_voice(f"Відкриваю додатки")
                    if "закрити" in text_command.lower():
                        run_voice(f"Закриваю додатки")

                for user_app in list_apps:
                    if user_app.path:
                        if "відкрити" in text_command.lower():
                            if len(list_apps) == 1: run_voice(f"Відкриваю {user_app.name}")
                            self.open_app(path_app= user_app.path)
                        elif "закрити" in text_command.lower():
                            if len(list_apps) == 1: run_voice(f"Зачиняю {user_app.name}")
                            self.close_app(name_app= os.path.basename(user_app.path))
                    else:
                        if len(list_apps) == 1: run_voice(f"Шукаю шлях до {user_app.name}")
                        path= find_path(filename= user_app.name)
                        if path:
                            if len(list_apps) == 1: run_voice(f"Шлях знайдено")
                            if "відкрити" in text_command.lower():
                                self.open_app(path_app= path)
                            elif "закрити" in text_command.lower():
                                self.close_app(user_app.name)
                            user_app.path = path
                            user_app.save()
                        else:
                            if len(list_apps) == 1: run_voice("Шлях до цієї програми не знайдено")
        
        if "help" in text_command.lower() or "команди" in text_command.lower():
            self.command_help()

        if "stop" in text_command.lower() or "стоп" in text_command.lower():
            self.run = False

        if "додати команду" in text_command.lower():
            add_command(source= source)

        if "список програм" in text_command.lower():
                open_progs = get_open_programs()
                print(f"Відчинені додатки: {open_progs}")
                run_voice("Відчинені додатки")

        if "закрити програми" in text_command.lower() or "close" in text_command.lower():
            open_progs = get_open_programs()
            allowed = ['gamebar.exe', 'zoom.exe', 'crossdeviceresume.exe', 'nvidia overlay.exe']
            close_unwanted_programs(allowed, open_progs)
            run_voice("Додатки закриті")

        if "шаблон математика" in text_command.lower():
            open_folder(folder_name= "Математика")

        if "шаблон програмування" in text_command.lower():
            open_folder(folder_name= "Програмування")

        if "профіль перший" in text_command.lower():
            open_site_in_profile(url_name= "https://")

        if "профіль третій" in text_command.lower():
            open_site_in_profile("Profile 3", url_name= "https://")
        
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

    def close_app(self, name_app: str):
        try:
            if platform.system() == "Windows":
                if not ".exe" in name_app:
                    name_app += ".exe"
                subprocess.run(['taskkill', '/F', '/IM', name_app], 
                            check=False, 
                            stdout= subprocess.DEVNULL, stderr= subprocess.DEVNULL
                        )
            else:
                subprocess.run(args= ["pkill", name_app])
        except Exception as error:
            self.stdout.write(self.style.WARNING(f"Error: {error}"))
        
    def command_help(self):
        self.stdout.write("Список можливих дій: \n\n • Додати команду \n • Закрий 'Назва додатку'\n • Відкрий 'Назва додатку'\n • Відкрий сайт 'Назва сайту'\n • Зупинись \n\nСписок додатків: ")
        for app_command in AppComand.objects.all():
            self.stdout.write(f" • Ключове слово - {app_command.keyword}, Назва додатку - {app_command.name}")
        self.stdout.write("\nГолосові запити:")
        for voice_answer in VoiceAnswer.objects.all():
            self.stdout.write(f' • {voice_answer.request}')
        self.stdout.write("\nСписок сайтів:")
        for site in WebSite.objects.all():
            self.stdout.write(f' • {site.name}, url - {site.url}')