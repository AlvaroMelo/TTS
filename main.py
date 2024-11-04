import os

from azure.cognitiveservices.speech import SpeechConfig, AudioConfig
from azure.cognitiveservices.speech import SpeechSynthesizer
from azure.cognitiveservices.speech import SynthesisVoiceGender
from azure.cognitiveservices.speech import SpeechSynthesisOutputFormat

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('AZURE_API_KEY')
### For this to work, we need to install:
# azure-functions
# azure-cognitiveservices-vision-customvision
# azure-cognitiveservices-speech


CREDENTIALS = {
    "speech_endpoint": "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issuetoken",
    "speech_key": api_key,
}

m_speech_config = SpeechConfig(
    endpoint=CREDENTIALS["speech_endpoint"], subscription=CREDENTIALS["speech_key"]
)


def get_voices(speech_synthesizer):
    voices = speech_synthesizer.get_voices_async().get().voices
    return voices


def choose_voices(voices, language="pt-BR", gender="male"):
    gender = (
        SynthesisVoiceGender.Male
        if gender.lower() == "male"
        else SynthesisVoiceGender.Female
    )
    language_gender_voices = [
        voice
        for voice in voices
        if voice.locale.startswith(language) and voice.gender == gender
    ]
    return language_gender_voices


def generate_voice(speech_config, voice, text="Isso é uma amostra da minha voz.", file_name=None):
    speech_config.speech_synthesis_voice_name = voice.name
    speech_config.set_speech_synthesis_output_format(
        SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
    )
    gender = "male" if voice.gender == SynthesisVoiceGender.Male else "female"
    if file_name is None:
        file_name = f"./mnt/data/{gender}/sample_voice{voice.short_name}.wav"
    else:
        file_name = f"./mnt/data/{gender}/{file_name}.wav"
    print("Saving to", file_name)
    audio_output = AudioConfig(filename=file_name)
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_output
    )
    result = synthesizer.speak_text_async(text).get()

    if result.reason == result.reason.SynthesizingAudioCompleted:
        print(f"Generated voice sample for {voice.short_name} ({voice.locale}).")
        return file_name
    else:
        print(
            f"Failed to generate voice sample for {voice.short_name} ({voice.locale})."
        )
        return None


###########################
###########################
###########################

def generate(voice, text, gender="male"):
    m_speech_config = SpeechConfig(
        endpoint=CREDENTIALS["speech_endpoint"], subscription=CREDENTIALS["speech_key"]
    )
    file_name = f"./mnt/data/{gender}/Audio.wav"
    file_config = AudioConfig(filename=file_name)

    speech_synthesizer = SpeechSynthesizer(
        speech_config=m_speech_config, audio_config=file_config
    )
    voices = get_voices(speech_synthesizer)
    all_voices = choose_voices(voices, gender="male") if gender == "male" else choose_voices(voices, gender="female")

    my_voice = None
    for v in all_voices:
        if voice in v.short_name:
            my_voice = v
            break
    generate_voice(m_speech_config, my_voice, text=text, file_name="Audio")
    return file_name  # Return the path to the generated file
