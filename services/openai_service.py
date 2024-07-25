import os
import openai

def procesar_mensaje_texto(mensaje, user_phone):
    """Procesa un mensaje de texto del usuario y genera una respuesta adecuada."""

    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Lógica para identificar la intención del usuario (puedes usar OpenAI para esto)
    if mensaje.lower().startswith("registrar comida"):
        return "Por favor, envía una foto de tu comida para que pueda analizarla."
    elif mensaje.lower().startswith("registrar ejercicio"):
        return "¿Qué tipo de ejercicio realizaste y cuánto tiempo duró?"
    elif mensaje.lower().startswith("registrar agua"):
        return "¿Cuántos mililitros de agua bebiste?"
    elif mensaje.lower().startswith("registrar medicamento"):
        return "Por favor, dime el nombre, la dosis y la frecuencia de tu medicamento."
    elif mensaje.lower().startswith("resumen"):
        return "¿Qué tipo de resumen deseas? (diario, semanal, mensual)"
    else:
        # Utilizar OpenAI para generar una respuesta más general
        prompt = f"El usuario dijo: '{mensaje}'. Responde de manera amigable y útil, como un asistente de salud y bienestar."
        response = openai.Completion.create(
            engine="gpt-4o-mini",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()

def obtener_resumen_comida(alimentos, usuario_id):
    """Genera un resumen nutricional de una lista de alimentos."""

    prompt = f"Los alimentos identificados en la imagen son: {', '.join(alimentos)}. Proporciona un resumen nutricional de estos alimentos para el usuario {usuario_id}, incluyendo calorías, proteínas, carbohidratos y grasas totales. Si es posible, incluye fibra y recomendaciones personalizadas basadas en los objetivos del usuario."

    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return response.choices[0].text.strip()
