import PyPDF2
import pyttsx3
import threading
import re
import requests
import io
import importlib

alphabets = "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\\s|She\\s|It\\s|They\\s|Their\\s|Our\\s|We\\s|But\\s|However\\s|That\\s|This\\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

def speaker_init ():
    importlib.reload(pyttsx3) # Workaround to be avoid pyttsx3 being stuck
    speaker = pyttsx3.init()
    return speaker

class Speaking(threading.Thread):
    def __init__(self, list_of_sentences, **kw):
        super().__init__(**kw)
        self.sentences = list_of_sentences
        self.paused = False


    def run(self):
        self.running = True
        while self.sentences and self.running:
            if not self.paused:
                sentence = self.sentences.pop(0)
                self.speaker = speaker_init()
                self.speaker.setProperty('rate', 160)
                self.voices = self.speaker.getProperty('voices')
                self.speaker.setProperty('voice', self.voices[0].id)
                print(sentence)
                self.speaker.say(sentence)
                self.speaker.runAndWait()
        print("finished")
        self.running = False

    def stop(self):
        self.running = False

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False


speak = None


def read():
    global speak
    if speak is None or not speak.running:
        speak = Speaking(book, daemon=True)
        speak.start()

def stop():
    global speak
    if speak:
        speak.stop()
        speak = None

def pause():
    if speak:
        speak.pause()

def unpause():
    if speak:
        speak.resume()


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    if "..." in text: text = text.replace("...", "<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    if "e.g." in text: text = text.replace("e.g.", "e<prd>g<prd>")
    if "i.e." in text: text = text.replace("i.e.", "i<prd>e<prd>")
    text = re.sub("\\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" "+suffixes+"[.] "+starters, " \\1<stop> \\2", text)
    text = re.sub(" "+suffixes+"[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

book = None
num_of_pages = 0

def read_book(path, page_num):
    global book, num_of_pages
    url = path
    response = requests.get(url)
    with io.BytesIO(response.content) as open_pdf_file:
        pdfReader = PyPDF2.PdfFileReader(open_pdf_file)
        num_of_pages = pdfReader.numPages

        file = ""
        page = page_num
        for count in range(page, num_of_pages):
            pageObj = pdfReader.getPage(count)
            file += pageObj.extractText()

        book = split_into_sentences(file)
        







