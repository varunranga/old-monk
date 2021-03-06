import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:              # use "test.wav" as the audio source
    audio = r.record(source)                        # extract audio data from the file

try:
    print("You said " + r.recognize_google(audio))         # recognize speech using Google Speech Recognition
except IndexError:                                  # the API key didn't work
    print("No internet connection")
except KeyError:                                    # the API key didn't work
    print("Invalid API key or quota maxed out")
except LookupError:                                 # speech is unintelligible
    print("Could not understand audio")