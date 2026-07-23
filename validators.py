"""validators.py — Validación de entrada (Parte 3, aún sin implementar).
 
Qué hace este módulo (POR AHORA):
  - Stub temporal: ambas funciones siempre devuelven "válido" para no
    bloquear el desarrollo de la Parte 2. logic.py ya las llama en el orden
    correcto (fail-closed), así que cuando se implemente de verdad aquí, NO
    hace falta tocar logic.py.
 
TODO Fase 3 (Parte 3 — Robustez):
  - validar_entrada(pregunta):
      * longitud (config.MAX_INPUT_CHARS)
      * vacío / solo espacios
      * patrones de inyección (config.PATRONES_SOSPECHOSOS)
      * fuera de dominio (config.DOMINIO_KEYWORDS)
      * datos sensibles (salario, bonus, datos de terceros) -> derivar,
        no responder con cifras (ver POLITICAS.md)
  - validar_dia(dia):
      * ya valida rango básico 1-5; ampliar si hace falta con
        config.DIAS_ONBOARDING_VALIDOS
"""
 
import config
import re

#---------------------------------------------------------------------------------------------------------------
# Mensajes de rechazo (Cargados desde config.py)
#---------------------------------------------------------------------------------------------------------------

MSG_VACIO = config.MSG_VACIO

MSG_DEMASIADO_LARGO = (
    "Tu mensaje es demasiado largo para procesarlo (máx. "
    f"{config.MAX_INPUT_CHARS} caracteres). ¿Puedes resumir tu pregunta?"
)

MSG_ENTRADA_SOSPECHOSA = config.MSG_ENTRADA_SOSPECHOSA
MSG_DATO_SENSIBLE = config.MSG_DATO_SENSIBLE
MSG_FUERA_DE_DOMINIO = config.MSG_FUERA_DE_DOMINIO
MSG_DIA_INVALIDO = config.MSG_DIA_INVALIDO


#---------------------------------------------------------------------------------------------------------------
# Patrones de datos sensibles (Cargados desde config.py)
#---------------------------------------------------------------------------------------------------------------

PATRONES_DATOS_SENSIBLES = config.PATRONES_DATOS_SENSIBLES
PATRONES_PROGRAMA_EXTERNO = config.PATRONES_PROGRAMA_EXTERNO

#---------------------------------------------------------------------------------------------------------------
# Funciones
#---------------------------------------------------------------------------------------------------------------


def _contiene_alguno(texto_normalizado: str, patrones: tuple[str, ...]) -> bool:
    """True si alguno de los patrones aparece como substring en el texto."""
    return any(patron in texto_normalizado for patron in patrones)


def validar_entrada(pregunta: str) -> tuple[bool, str | None]:
    """TODO Fase 3."""
    if pregunta is None or pregunta.strip() == "":
        return False, MSG_VACIO
 
    if len(pregunta) > config.MAX_INPUT_CHARS:
        return False, MSG_DEMASIADO_LARGO
 
    texto = pregunta.lower()
 
    if _contiene_alguno(texto, config.PATRONES_SOSPECHOSOS):
        return False, MSG_ENTRADA_SOSPECHOSA
 
    if _contiene_alguno(texto, PATRONES_DATOS_SENSIBLES):
        return False, MSG_DATO_SENSIBLE
 
    if _contiene_alguno(texto, PATRONES_PROGRAMA_EXTERNO):
        return False, MSG_FUERA_DE_DOMINIO
 
    dominio_keywords = getattr(config, "DOMINIO_KEYWORDS", ())
    if dominio_keywords and not _contiene_alguno(texto, dominio_keywords):
        return False, MSG_FUERA_DE_DOMINIO
 
    return True, None
    
 
def validar_dia(dia: int) -> tuple[bool, str | None]:
    """Valida que el día de onboarding esté en rango 1-5.
 
    TODO Fase 3: usar config.DIAS_ONBOARDING_VALIDOS si se añade lógica
    adicional (p. ej. mensajes de error más ricos, distintos por perfil).
    """
    if not isinstance(dia, int) or dia not in range(1, 6):
        return False, f"Día {dia} fuera de rango (debe ser 1-5)."
    return True, None