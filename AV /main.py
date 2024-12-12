import webbrowser
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import os

# Inicializa o motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Velocidade da fala
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.monica')  # Voz

# Configurações da API GEMINI IA
genai.configure(api_key="AIzaSyASwHi8y-HV20lbKtxcuDLotD3WksBsv8k")
model = genai.GenerativeModel('gemini-1.5-pro')
chat = model.start_chat(history=[])

def speak(text):
    """Faz o assistente falar"""
    engine.say(text)
    engine.runAndWait()

def ouvir_comando():
    """Escuta o comando do usuário usando o microfone"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            comando = recognizer.recognize_google(audio, language="pt-BR")
            return comando.lower()
        except sr.UnknownValueError:
            speak("Não consegui entender. Pode repetir, por favor?")
            return ""
        except sr.RequestError:
            speak("Houve um problema com a conexão ao serviço de reconhecimento de voz.")
            return ""
        except sr.WaitTimeoutError:
            speak("Não detectei nenhum som. Pode tentar novamente?")
            return ""

def pesquisar_google(query):
    """Realiza uma pesquisa no Google"""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("Aqui está o que encontrei no Google para sua pesquisa.")

def pesquisar_youtube(query):
    """Realiza uma pesquisa no YouTube"""
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    speak("Aqui estão os resultados no YouTube para sua pesquisa.")

def responder_pergunta(query):
    """Usa o modelo generativo para responder perguntas de forma natural"""
    try:
        response = chat.send_message(query)
        speak(response)
        print("Gemini:", response.text, "\n")
    except openai.error.OpenAIError as e:
        speak("Desculpe, houve um problema ao processar sua pergunta.")
        print(f"Erro com a API OpenAI: {e}")
    except Exception as e:
        speak("Houve um erro inesperado. Tente novamente mais tarde.")
        print(f"Erro geral: {e}")

def registrar_comando_invalido(comando):
    """Registra comandos não reconhecidos em um arquivo de log"""
    with open("comandos_nao_reconhecidos.log", "a") as log_file:
        log_file.write(f"Comando não reconhecido: {comando}\n")

# Fluxo principal do assistente
speak("Olá! Eu sou seu assistente virtual. Como posso ajudar?")

while True:
    comando = ouvir_comando()

    if "google" in comando:
        speak("O que você quer pesquisar no Google?")
        pesquisa = ouvir_comando()
        if pesquisa:
            pesquisar_google(pesquisa)

    elif "youtube" in comando:
        speak("O que você quer pesquisar no YouTube?")
        pesquisa = ouvir_comando()
        if pesquisa:
            pesquisar_youtube(pesquisa)

    elif "pergunta" in comando:
        speak("Qual é a sua pergunta?")
        pergunta = ouvir_comando()
        if pergunta:
            responder_pergunta(pergunta)

    elif "sair" in comando or "fechar" in comando:
        speak("Até logo! Se precisar de mim, é só chamar.")
        break

    elif comando:
        print(f"Comando não reconhecido: {comando}")
        registrar_comando_invalido(comando)
        speak("Desculpe, não entendi. Você pode repetir?")

