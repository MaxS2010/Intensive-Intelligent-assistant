import edge_tts, pygame, asyncio, time, threading, os

pygame.init()

VOICE = 'uk-UA-OstapNeural' # uk-UA-PolinaNeural 

async def create_voice(text: str,  file_name: str):
    ready_voice = edge_tts.Communicate(text= text, voice= VOICE)
    await ready_voice.save(audio_fname= file_name)

def voice_text(text: str):
    file_name = f'voice_temp_{str(time.time())[-5:]}.mp3'

    voice_event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(voice_event_loop)

    voice_event_loop.run_until_complete(create_voice(text= text, file_name= file_name))
    voice_event_loop.close()

    if os.path.exists(file_name):
        pygame.mixer.music.load(filename= file_name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        os.remove(file_name)    

def run_voice(text: str):
    voicing_thread= threading.Thread(target= voice_text, args= (text,), daemon= True)
    voicing_thread.start()
