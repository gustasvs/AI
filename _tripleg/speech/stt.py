import speech_recognition as sr

r = sr.Recognizer()
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"Microphone - \"{name}\" index={index})`")

with sr.Microphone() as f:
    print('Retrieving input...')
    audio = r.listen(f)
    try:
        # text = r.recognize_google(audio, language='lv')
        text = r.recognize_google(audio, language='en-US')
        print(f'Retrieved input - {text}')
    # except:
    #     text = r.recognize_google(audio, language='en-US')
    #     print(f'Retrieved input - {text}')
    except:
        pass