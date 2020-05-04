import speech_recognition as sr  # Importing SpeechRecognition Package and assigning alias.
import webbrowser as wb          # Importing access to a web browser and assigning an alias.


g1 = sr.Recognizer()
g2 = sr.Recognizer()  # Using Recognizer class to create instances to recognize speech.
g3 = sr.Recognizer()

with sr.Microphone() as source:  # Specifying where the input is coming from.
    print('[say "Google" to activate web and search queries or say "Youtube" to search for videos.]')
    print('Talk now.')
    sound = g3.listen(source)    # Assigning variable to listen method, taking input from source.

if 'Google' in g2.recognize_google(sound):  # Activates when 'Google' is heard, 'recognize_google' uses Google Chrome.
    g2 = sr.Recognizer()
    url = 'https://google.com/search?q='  # Passing url
    with sr.Microphone() as source:
        print('search your query')
        sound = g2.listen(source)

        try:
            get = g2.recognize_google(sound)  # Recognizes the second input query
            print(get)
            wb.get().open_new(url+get)  # Opening specified url
        except sr.UnknownValueError:
            print('I do not comprehend.')
        except sr.RequestError as e:
            print('failed to produce results'.format(e))

if 'YouTube' in g1.recognize_google(sound):  # Activates when 'Youtube' is heard.
    g1 = sr.Recognizer()
    url = 'https://www.youtube.com/results?search_query='  # Passing url
    with sr.Microphone() as source:
        print('search your query')
        sound = g1.listen(source)

        try:
            get = g1.recognize_google(sound)
            print(get)
            wb.get().open_new(url+get)
        except sr.UnknownValueError:
            print('I do not comprehend.')
        except sr.RequestError as e:
            print('failed to produce results'.format(e))
