from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
import speech_recognition as sr
import soundfile as sf 

recognizer = sr.Recognizer()
def get_voice(update: Update, context: CallbackContext) -> None:
    new_file = context.bot.get_file(update.message.voice.file_id)
    new_file.download("./data/message.ogg")
    data, samplerate = sf.read('./data/message.ogg')
    sf.write('./data/message.wav', data, samplerate)
    update.message.reply_text('Recognition started...')
    file = sr.AudioFile("./data/message.wav")
    with file as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)
        result = recognizer.recognize_google(audio, language='ru')
    update.message.reply_text(result)


updater = Updater("<TOKEN>")

updater.dispatcher.add_handler(MessageHandler(Filters.voice , get_voice))

updater.start_polling()
updater.idle()


