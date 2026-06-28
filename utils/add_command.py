from .voice_answers import run_voice
import speech_recognition, time

from core.models import AppComand

recognizer = speech_recognition.Recognizer()

def get_voice(source) -> str | None:
    try:
        audio = recognizer.listen(source, phrase_time_limit= 5)
        text = recognizer.recognize_google(audio, language="uk-UA").strip() # type: ignore
        print(f"Асистент почув: {text}")
        return text
    except:
        return None

def add_command(source):
    run_voice('Щоб додати команду скажіть ключове слово')
    
    keyword = get_voice(source)

    if keyword:
        run_voice(f'Ваше слово: {keyword}. Підтвердити?')

        accept = get_voice(source)

        if 'підтвердити' in accept.lower() or 'так' in accept.lower(): # type: ignore
            run_voice("Скажіть назву файлу додатка")

            app_name = get_voice(source)
            
            if app_name:
                run_voice(f"Назва додатку {app_name}. Підтвердити?")

                name_accept = get_voice(source)

                if 'підтвердити' in name_accept.lower() or 'так' in name_accept.lower(): # type: ignore
                    AppComand.objects.create(name= app_name, keyword= keyword)
                    run_voice("Команду успішно додано")

                else:
                    run_voice("Невдалося підтвердити")
                    add_command(source)
            else:
                run_voice("Назву не розпізнано")
                add_command(source)
        else:
            run_voice("Невдалося підтвердити, спробуйте ще раз")
    else: 
        run_voice('Слово не розпізнано, спробуйте ще раз')