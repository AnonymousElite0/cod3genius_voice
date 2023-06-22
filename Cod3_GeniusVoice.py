import wx
import speech_recognition as sr
import openai
import pyttsx3

# ApiKey OpenAI
openai.api_key = "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"

# Configuración de texto a voz
engine = pyttsx3.init()

# Función de texto a voz
def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

# Función transcribir audio
def escuchar_audio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        hablar("dimmi che posso aiutarti")
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

# Clase para la ventana principal
class VentanaPrincipal(wx.Frame):
    def __init__(self, parent, title):
        super(VentanaPrincipal, self).__init__(parent, title=title, size=(400, 300))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        texto_entrada = wx.StaticText(panel, label="Ingrese su mensaje de voz:")
        vbox.Add(texto_entrada, flag=wx.LEFT | wx.TOP, border=10)

        self.campo_entrada = wx.TextCtrl(panel)
        vbox.Add(self.campo_entrada, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        boton_enviar = wx.Button(panel, label="Enviar")
        boton_enviar.Bind(wx.EVT_BUTTON, self.enviar_mensaje)
        vbox.Add(boton_enviar, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def enviar_mensaje(self, event):
        texto_entrada = self.campo_entrada.GetValue()
        respuesta = generar_respuesta(texto_entrada)
        wx.MessageBox(respuesta, "Respuesta", wx.OK | wx.ICON_INFORMATION)

# Iniciar la aplicación
if __name__ == "__main__":
    app = wx.App()
    ventana_principal = VentanaPrincipal(None, title="CodeGenius")
    ventana_principal.Show()
    app.MainLoop()