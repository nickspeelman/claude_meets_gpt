from text_to_speech import text_to_speech
from io import BytesIO
from pydub import AudioSegment

def process_audio_if_enabled(response, voice_id, generate_voice):
    """
    Generates audio if the voice generation is enabled.
    """
    if generate_voice:
        audio_data = text_to_speech(response, voice_id)
        final_audio = AudioSegment.from_file(BytesIO(audio_data), format="mp3")
        return final_audio
