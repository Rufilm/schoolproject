import speech_recognition
import wave
import os
import pyttsx3
import webbrowser
import googletrans
import random
import pyautogui
import wikipediaapi
import command

################### КЛАССЫ ###################
class VoiceAssistant:
    name = ""
    sex = ""
    speech_language = ""
    recognition_language = ""

class PersonInfo:
    name = ""
    location = ""


##################### END #####################

################### ФУНКЦИИ ###################

def setup_assistant_voice():

    voices = ttsEngine.getProperty("voices")

    if assistant.speech_language == "en":
        assistant.recognition_language = "en-US"
        ttsEngine.setProperty("voice", voices[2].id)
    else:
        assistant.recognition_language = "ru-RU"
        # Microsoft Irina Desktop - Russian
        ttsEngine.setProperty("voice", voices[0].id)

def play_voice_assistant_speech(text_to_speech):

    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()

def record_and_recognize_audio(*args: tuple):

    with microphone:
        recognized_data = ""

        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Прослушивание...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            return

        try:
            print("Обработка...")
            recognized_data = recognizer.recognize_google(audio, language="ru").lower()

        except speech_recognition.UnknownValueError:
            pass

        return recognized_data

def open_browser(*args: tuple):

    if not args[0]: return

    url = "http://127.0.0.1:{0}"
    webbrowser.open_new(url)

    play_voice_assistant_speech('Открываю')

def search_on_browser(*args: tuple):

    if not args[0]: return

    search_term = " ".join(args[0])
    url = "https://google.com/search?q=" + search_term
    webbrowser.get().open(url)

    play_voice_assistant_speech('Вот что я нашёл по данному запросу')
def he_said_hello(*args: tuple):

    he_said_hello = [
        ("Привет, {}! Как настроение?").format(person.name),
        ("Приветсвую {}! Чем займёмся?").format(person.name),
        ("Здравствуйте {}!").format(person.name)
    ]
    play_voice_assistant_speech(he_said_hello[random.randint(0, len(he_said_hello) - 1)])

def search_on_wikipedia(*args: tuple):

    if not args[0]: return

    search_term = " ".join(args[0])

    wiki = wikipediaapi.Wikipedia(assistant.speech_language)

    wiki_page = wiki.page(search_term)
    try:
        if wiki_page.exists():
            play_voice_assistant_speech(("Вот что было найдено по запросу: {} на Википедий").format(search_term))
            webbrowser.get().open(wiki_page.fullurl)

            play_voice_assistant_speech(wiki_page.summary.split(".")[:2])
        else:
            play_voice_assistant_speech("Не могу найти ваш запрос: {} на вики. Но вот что я нашла в гугле").format(search_term)
            url = "https://google.com/search?q=" + search_term
            webbrowser.get().open(url)

    except:
        print('DEBUG: Error (122 line)')
        traceback.print_exc()
        return
def toss_coin(*args: tuple):

    flips_count, heads, tails = 3, 0, 0

    for flip in range(flips_count):
        if random.randint(0, 1) == 0:
            heads += 1

    tails = flips_count - heads
    winner = "Решка" if tails > heads else "Орёл"
    play_voice_assistant_speech('winner') + " " + ("won")
def minimized(*args: tuple):

    if not args[0]: return

    pyautogui.hotkey('win', 'm')
    play_voice_assistant_speech('Сворачиваю окна')
def exit_programm(*args: tuple):

    exit_phrase = [
        ("Прощайте, {}! Надеюсь мы увдимся вновь!").format(person.name),
        ("Счастливого дня, {}!").format(person.name)
    ]
    play_voice_assistant_speech(exit_phrase[random.randint(0, len(exit_phrase) - 1)])
    ttsEngine.stop()
    quit()

def execute_command_with_name(command_name: str, *args: list):

    for key in commands.keys():
        if command_name in key:
            commands[key](*args)
        else:
            pass

##################### END #####################


commands = {
    ("приветик", "здорова", "приветствую", "привет"): he_said_hello,
    ("пока", "отключайся", "выключись", "прощай", "пока"): exit_programm,
    ("открой" + "браузер"): open_browser,
    ("найди", "поищи"): search_on_browser,
    ("сверни" + "окна"): minimized,
    ("монета", "подбрось", "монетка"): toss_coin,
    ("определение", "википедий", "википедия"): search_on_wikipedia,
}

if __name__ == "__main__":

    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    ttsEngine = pyttsx3.init()
    person = PersonInfo()
    person.name = "Станислав"
    person.location = "Обнинск"

    assistant = VoiceAssistant()
    assistant.name = "Jarvis"
    assistant.sex = "Male"

    setup_assistant_voice()

    while True:
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")
        print(voice_input)

        voice_input = voice_input.split(" ")
        command = voice_input[0]
        command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
        execute_command_with_name(command, command_options)
