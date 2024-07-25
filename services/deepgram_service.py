import os
import asyncio
from deepgram import Deepgram

async def transcribir_audio_async(audio_url):
    """Transcribe un audio usando Deepgram (asíncronamente)."""

    deepgram_key = os.getenv("DEEPGRAM_API_KEY")
    dg_client = Deepgram(deepgram_key)
    
    # Opciones para la transcripción (puedes personalizarlas según tus necesidades)
    options = {
        "model": "nova",        # Modelo de transcripción (puedes usar otros modelos)
        "language": "es-MX",    # Idioma español de México
        "punctuate": True,      # Puntuación automática
        "smart_format": True,   # Formato inteligente
        # "diarize": True,      # Identificación de hablantes (opcional)
        # ... (otras opciones)
    }

    try:
        # Realizar la transcripción
        response = await dg_client.transcription.prerecorded_from_url(audio_url, options)
        transcript = ""
        for utterance in response['results']['utterances']:
            transcript += utterance['transcript'] + " "
        return transcript

    except Exception as e:
        print(f"Error en la transcripción de Deepgram: {e}")
        return "Lo siento, hubo un error al procesar tu audio."

def transcribir_audio(audio_url):
    """Envuelve la función asíncrona para ser utilizada de forma síncrona."""
    return asyncio.run(transcribir_audio_async(audio_url))