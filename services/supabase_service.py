import os
from supabase import create_client, Client
from datetime import datetime, timedelta

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def existe_usuario(celular):
    """Verifica si un usuario existe en la base de datos."""
    try:
        response = supabase.table("usuarios").select("celular").eq("celular", celular).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Error al verificar existencia del usuario: {e}")
        return False

def verificar_suscripcion(usuario_id):
    """Verifica si un usuario tiene una suscripción activa."""
    try:
        response = supabase.table("suscripciones").select("*").eq("usuario_id", usuario_id).execute()
        for suscripcion in response.data:
            if suscripcion["estado"] == "activa" and suscripcion["fecha_vencimiento"] >= datetime.now().date():
                return True
        return False
    except Exception as e:
        print(f"Error al verificar suscripción: {e}")
        return False

def registrar_alimento(nombre, calorias, proteinas, carbohidratos, grasas):
    """Registra un nuevo alimento en la base de datos."""
    try:
        data = supabase.table("alimentos").insert({
            "nombre": nombre,
            "calorias_por_100g": calorias,
            "proteinas_por_100g": proteinas,
            "carbohidratos_por_100g": carbohidratos,
            "grasas_por_100g": grasas
        }).execute()
        return data.data[0]["id"]
    except Exception as e:
        print(f"Error al registrar alimento: {e}")
        return None

def registrar_comida(usuario_id, alimento_id, cantidad):
    """Registra una comida en la base de datos."""
    try:
        data = supabase.table("comidas").insert({
            "usuario_id": usuario_id,
            "alimento_id": alimento_id,
            "cantidad": cantidad
        }).execute()
        return data.data[0]["id"]
    except Exception as e:
        print(f"Error al registrar comida: {e}")
        return None

def obtener_resumen_diario(usuario_id, fecha):
    """Obtiene el resumen diario de comidas, actividades y agua para un usuario."""
    try:
        # Obtener comidas
        comidas = supabase.table("comidas").select("*, alimentos (nombre, calorias_por_100g, proteinas_por_100g, carbohidratos_por_100g, grasas_por_100g)") \
            .eq("usuario_id", usuario_id).eq("fecha_hora::date", fecha).execute().data

        # Obtener actividades
        actividades = supabase.table("actividades").select("*, ejercicios (nombre)") \
            .eq("usuario_id", usuario_id).eq("fecha_hora::date", fecha).execute().data

        # Obtener consumo de agua
        agua = supabase.table("agua").select("*") \
            .eq("usuario_id", usuario_id).eq("fecha_hora::date", fecha).execute().data

        # Calcular totales y formatear respuesta
        resumen = {
            "comidas": [],
            "total_calorias": 0,
            "total_proteinas": 0,
            "total_carbohidratos": 0,
            "total_grasas": 0,
            "agua_consumida": 0,
            "actividades": []
        }

        for comida in comidas:
            resumen["comidas"].append({
                "nombre": comida["alimentos"]["nombre"],
                "cantidad": comida["cantidad"],
                "calorias": comida["alimentos"]["calorias_por_100g"] * comida["cantidad"] / 100,
                "proteinas": comida["alimentos"]["proteinas_por_100g"] * comida["cantidad"] / 100,
                "carbohidratos": comida["alimentos"]["carbohidratos_por_100g"] * comida["cantidad"] / 100,
                "grasas": comida["alimentos"]["grasas_por_100g"] * comida["cantidad"] / 100
            })
            resumen["total_calorias"] += comida["alimentos"]["calorias_por_100g"] * comida["cantidad"] / 100
            resumen["total_proteinas"] += comida["alimentos"]["proteinas_por_100g"] * comida["cantidad"] / 100
            resumen["total_carbohidratos"] += comida["alimentos"]["carbohidratos_por_100g"] * comida["cantidad"] / 100
            resumen["total_grasas"] += comida["alimentos"]["grasas_por_100g"] * comida["cantidad"] / 100

        for actividad in actividades:
            resumen["actividades"].append({
                "nombre": actividad["ejercicios"]["nombre"],
                "duracion": str(actividad["duracion"]),
                "calorias_quemadas": actividad["calorias_quemadas"]
            })

        if agua:
            resumen["agua_consumida"] = agua[0]["cantidad_ml"]

        return resumen

    except Exception as e:
        print(f"Error al obtener resumen diario: {e}")
        return None
# ... (otras importaciones y funciones existentes)

# Funciones para Ejercicios
def registrar_ejercicio(nombre, calorias_por_minuto=None, musculos_trabajados=None):
    """Registra un nuevo ejercicio en la base de datos."""
    try:
        data = supabase.table("ejercicios").insert({
            "nombre": nombre,
            "calorias_por_minuto": calorias_por_minuto,
            "musculos_trabajados": musculos_trabajados
        }).execute()
        return data.data[0]["id"]
    except Exception as e:
        print(f"Error al registrar ejercicio: {e}")
        return None

def obtener_ejercicios():
    """Obtiene todos los ejercicios de la base de datos."""
    try:
        response = supabase.table("ejercicios").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener ejercicios: {e}")
        return None

# Funciones para Rutinas
def registrar_rutina(usuario_id, nombre, descripcion=None, fecha_inicio=None, fecha_fin=None, objetivo=None):
    """Registra una nueva rutina en la base de datos."""
    try:
        data = supabase.table("rutinas").insert({
            "usuario_id": usuario_id,
            "nombre": nombre,
            "descripcion": descripcion,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "objetivo": objetivo
        }).execute()
        return data.data[0]["id"]
    except Exception as e:
        print(f"Error al registrar rutina: {e}")
        return None

def obtener_rutinas(usuario_id):
    """Obtiene todas las rutinas de un usuario."""
    try:
        response = supabase.table("rutinas").select("*").eq("usuario_id", usuario_id).execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener rutinas: {e}")
        return None

# Funciones para Metas de Agua
def registrar_meta_agua(usuario_id, cantidad_ml, fecha_inicio, fecha_fin=None):
    """Registra una nueva meta de agua en la base de datos."""
    try:
        data = supabase.table("metas_agua").insert({
            "usuario_id": usuario_id,
            "cantidad_ml": cantidad_ml,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin
        }).execute()
        return data.data[0]["id"]
    except Exception as e:
        print(f"Error al registrar meta de agua: {e}")
        return None

def obtener_meta_agua_actual(usuario_id):
    """Obtiene la meta de agua actual del usuario."""
    try:
        response = supabase.table("metas_agua").select("*").eq("usuario_id", usuario_id) \
            .gte("fecha_inicio", datetime.now().date()) \
            .lte("fecha_fin", datetime.now().date()).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error al obtener meta de agua actual: {e}")
        return None

def actualizar_medicamento(medicamento_id, nombre=None, dosis=None, frecuencia=None, horario=None):
    """Actualiza los datos de un medicamento existente."""
    try:
        updates = {}
        if nombre:
            updates["nombre"] = nombre
        if dosis:
            updates["dosis"] = dosis
        if frecuencia:
            updates["frecuencia"] = frecuencia
        if horario:
            updates["horario"] = horario

        data = supabase.table("medicamentos").update(updates).eq("id", medicamento_id).execute()
        return data.data[0] if data.data else None
    except Exception as e:
        print(f"Error al actualizar medicamento: {e}")
        return None

def eliminar_medicamento(medicamento_id):
    """Elimina un medicamento de la base de datos."""
    try:
        supabase.table("medicamentos").delete().eq("id", medicamento_id).execute()
        return True  # Éxito
    except Exception as e:
        print(f"Error al eliminar medicamento: {e}")
        return False  # Error

# Funciones para Recordatorios (Actualizar y Eliminar)
def actualizar_recordatorio(recordatorio_id, fecha_hora):
    """Actualiza la fecha y hora de un recordatorio."""
    try:
        data = supabase.table("recordatorios").update({"fecha_hora": fecha_hora}).eq("id", recordatorio_id).execute()
        return data.data[0] if data.data else None
    except Exception as e:
        print(f"Error al actualizar recordatorio: {e}")
        return None

def eliminar_recordatorio(recordatorio_id):
    """Elimina un recordatorio de la base de datos."""
    try:
        supabase.table("recordatorios").delete().eq("id", recordatorio_id).execute()
        return True
    except Exception as e:
        print(f"Error al eliminar recordatorio: {e}")
        return False

# Funciones para Suscripciones (Actualizar y Eliminar)
def actualizar_suscripcion(suscripcion_id, tipo_suscripcion=None, fecha_vencimiento=None, estado=None):
    """Actualiza los datos de una suscripción existente."""
    try:
        updates = {}
        if tipo_suscripcion:
            updates["tipo_suscripcion"] = tipo_suscripcion
        if fecha_vencimiento:
            updates["fecha_vencimiento"] = fecha_vencimiento
        if estado:
            updates["estado"] = estado

        data = supabase.table("suscripciones").update(updates).eq("id", suscripcion_id).execute()
        return data.data[0] if data.data else None
    except Exception as e:
        print(f"Error al actualizar suscripción: {e}")
        return None

def eliminar_suscripcion(suscripcion_id):
    """Elimina una suscripción de la base de datos."""
    try:
        supabase.table("suscripciones").delete().eq("id", suscripcion_id).execute()
        return True
    except Exception as e:
        print(f"Error al eliminar suscripción: {e}")
        return False
