import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random

pontos = 0
duration = 5  # segundos de gravação
sample_rate = 44100

words_by_level = {
    "fácil": ["gato", "cachorro", "maçã", "leite", "sol"],
    "médio": ["casa", "escola", "amigo", "janela", "amarelo"],
    "difícil": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação"]
}
pergunta_dificuldade = int(input("Qual nível de dificuldade você quer? " +
"(1-fácil, 2-médio, 3-difícil): "))

if pergunta_dificuldade == 1:
    dificuldade = "fácil"

if pergunta_dificuldade == 2:
    dificuldade = "médio"
if pergunta_dificuldade == 3:
    dificuldade = "difícil"
for i in range(5):
    palavra = random.choice(words_by_level[dificuldade])
    print("fale a palavra:", palavra, "em inglês")
    print("Fale agora...")
    recording = sd.rec(
    int(duration * sample_rate), 
    samplerate=sample_rate,      
    channels=1,                  
    dtype="int16")               
    sd.wait()  

    wav.write("output.wav", sample_rate, recording)
    print("Gravação concluída, estou reconhecendo...")

    recognizer = sr.Recognizer()
    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="en")
        print("Você disse:", text)
        translator = Translator()
        translated = translator.translate(palavra, src='pt', dest='en')  # O 'en' aqui é um código para inglês
        print('palavra original:', palavra)
        print('tradução', translated.text)
        print("🌍 Tradução para o inglês:", translated.text)
        if text.lower() == translated.text.lower() or (palavra == "cachorro" and text.lower() in ["dog", "puppy"]) or (palavra == "maçã" and text.lower() in ["litter", "apple"]):
            print("Você acertou e ganhou 1 ponto! ✅")
            pontos += 1
            print('')
            print('')
        else:
            pontos -= 1
            print("Você errou e perdeu um ponto. ❌")
            print('')
            print('')
    except sr.UnknownValueError:             # - se o Google não conseguiu entender a fala devido a ruídos ou silêncio
        print("A fala não pôde ser reconhecida.")
    except sr.RequestError as e:             # - se não houver conexão com a Internet ou a API estiver indisponível
        print(f"Service error: {e}")


print('----------------------------------------------')
print('Sua quantidade total de pontos foi:', pontos)