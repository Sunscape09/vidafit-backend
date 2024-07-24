import openai
import json
import services.supabase_service as supabase_service

def procesar_mensaje_texto(mensaje, user_phone):
    """Procesa un mensaje de texto del usuario utilizando OpenAI y Supabase."""

    # Configurar OpenAI
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Obtener información del usuario desde Supabase (si es necesario)
    usuario = supabase_service.obtener_usuario(user_phone)

    # Crear un prompt para OpenAI con el mensaje del usuario y el contexto
    prompt = f"""
    Eres un asistente de salud y bienestar. El usuario te envía el siguiente mensaje:
    '{mensaje}'

    El usuario tiene el siguiente perfil en la base de datos:
    {json.dumps(usuario)}

    Responde al usuario de manera amigable y útil, considerando su perfil y el contexto de la conversación. 
    Si el usuario pregunta sobre su información, usa los datos de su perfil.
    Si el usuario quiere registrar una comida, pídele que envíe una foto de la comida.
    Si el usuario quiere registrar una actividad física, pregúntale el tipo de actividad y la duración.
    Si el usuario quiere registrar su consumo de agua, pregúntale la cantidad en mililitros.
    Si el usuario quiere registrar un medicamento, pídele el nombre, dosis y frecuencia.
    Si el usuario quiere ver un resumen, pregúntale qué tipo de resumen desea (diario, semanal o mensual).
    Si el usuario escribe algo que no entiendes, pídele que reformule su pregunta.
    """

    # Generar una respuesta con OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",  # Puedes cambiar el modelo si lo deseas
        prompt=prompt,
        max_tokens=150,  # Ajusta según la longitud deseada de la respuesta
        n=1,
        stop=None,
        temperature=0.7,  # Ajusta para controlar la creatividad de la respuesta
    )

    # Extraer la respuesta generada
    respuesta_texto = response.choices[0].text.strip()

    return respuesta_texto

def obtener_resumen_comida(alimentos, usuario_id):
    """Genera un resumen de la comida usando OpenAI."""

    prompt = f"""
    Los alimentos identificados en la imagen son: {', '.join(alimentos)}.
    
    El usuario tiene el siguiente perfil en la base de datos:
    {json.dumps(supabase_service.obtener_usuario(usuario_id))}

    Proporciona un resumen nutricional de estos alimentos para el usuario, incluyendo:
    - Calorías totales
    - Proteínas totales
    - Carbohidratos totales
    - Grasas totales
    - Fibra total (si es posible)

    Si algún alimento no se encuentra en la base de datos, estima sus valores nutricionales.
    
    Si es posible, incluye recomendaciones personalizadas para el usuario basadas en sus objetivos y datos de perfil.
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,  # Ajusta según la longitud deseada de la respuesta
        n=1,
        stop=None,
        temperature=0.5,  # Ajusta para controlar la creatividad de la respuesta
    )

    return response.choices[0].text.strip()
