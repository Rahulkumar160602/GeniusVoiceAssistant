import openai
import pyttsx3
import speech_recognition as sr
import time

# Set API key
openai.api_key = "write your api key"

# Initialize text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    """Transcribe audio file to text"""
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

def generate_response(prompt):
    """Generate response using OpenAI"""
    response = openai.Completion.create(
        engine="text_davinci_002",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response["choices"][0]["text"]

def speak_text(text):
    """Speak text using text-to-speech engine"""
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("Say 'Genius' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "genius":
                    filename = "input.wav"
                    print("Say your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())

                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        response = generate_response(text)
                        print(f"GPT-3 says: {response}")

                        speak_text(response)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()