#anadir una interfaz grafica al codigo de python y mejor su interactividad.

import speech_recognition as sr
import openai
import pyttsx3
import typer

# ApiKey OpenAI
openai.api_key = "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"

# Configuración de texto a voz
engine = pyttsx3.init()

# Función de texto a voz
def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

# Función  transcribir audio
def escuchar_audio():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        hablar("ciao, dimmi che posso aiutarti oggi")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio, language="it-IT")
            hablar(f"ho sentito questo: {text}")
            return text
        except:
            hablar("Scusa, non sono riuscito a capire quello che hai detto. Potresti riprovare?")
            return ""

# Función generar respuesta
def generar_respuesta(prompt):

    prompt = f"{prompt.strip()}"

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text
    message = message.strip()
    print(f"codegenius: {message}")
    hablar(f"codegenius dice: {message}")

    return message

# Bucle de salida
while True:
    texto_entrada = escuchar_audio()
    if texto_entrada.lower() == "arrivederci":
        salir = typer.confirm("Sei sicuro di voler uscire?")
        if salir:
            print("Arrivederci! cod3genius al tuo servizio!")
            break
        else:
            continue
    respuesta = generar_respuesta(texto_entrada)
