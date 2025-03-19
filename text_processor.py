# text_processor.py
import re

def extraer_instrucciones(texto):
    """
    Procesa el texto transcrito y extrae instrucciones utilizando heurísticas refinadas.
    
    El método divide el texto en oraciones y asigna una "puntuación" a cada una en función de la
    presencia de palabras clave o verbos de acción (por ejemplo, "debe", "crear", "iniciar", etc.).
    Se consideran instrucciones aquellas oraciones que contengan al menos una coincidencia o que
    sean lo suficientemente largas y empiecen con un prefijo que sugiera acción.
    
    Parámetros:
        texto (str): Texto transcrito.
    
    Retorna:
        list: Lista de instrucciones extraídas.
    """
    palabras_clave = [
        # Expresiones auxiliares para instrucciones
        "debe", "debería", "deberás", "deberán", "debes", "tenía que", "tiene que", "tendría que", "tendrá que", 
        "hay que", "habrá que", "es necesario", "requiere", "requiere que", "requirió", "requerirá", "requeriría",

        # Verbos principales con sus formas conjugadas
        "realizar", "realiza", "realizaste", "realizó", "realizará", "realizaría", "realices",
        "ejecutar", "ejecuta", "ejecutaste", "ejecutó", "ejecutará", "ejecutaría", "ejecutes",
        "iniciar", "inicia", "iniciaste", "inició", "iniciará", "iniciaría", "inicies",
        "completar", "completa", "completaste", "completó", "completará", "completaría", "completes",
        "finalizar", "finaliza", "finalizaste", "finalizó", "finalizará", "finalizaría", "finalices",
        "culminar", "culmina", "culminaste", "culminó", "culminará", "culminaría", "culmines",
        "presentar", "presenta", "presentaste", "presentó", "presentará", "presentaría", "presentes",
        "detener", "detiene", "detuviste", "detuvo", "detendrá", "detendría", "detengas",
        "acreditar", "acredita", "acreditaste", "acreditó", "acreditará", "acreditaría", "acredites",
        "programar", "programa", "programaste", "programó", "programará", "programaría", "programes",
        "organizar", "organiza", "organizaste", "organizó", "organizará", "organizaría", "organices",
        "coordinar", "coordina", "coordinaste", "coordinó", "coordinará", "coordinaría", "coordines",
        "crear", "crea", "creaste", "creó", "creará", "crearía", "crees",
        "modificar", "modifica", "modificaste", "modificó", "modificará", "modificaría", "modifiques",
        "revisar", "revisa", "revisaste", "revisó", "revisará", "revisaría", "revises",
        "analizar", "analiza", "analizaste", "analizó", "analizará", "analizaría", "analices",
        "confirmar", "confirma", "confirmaste", "confirmó", "confirmará", "confirmaría", "confirmes",
        "implementar", "implementa", "implementaste", "implementó", "implementará", "implementaría", "implementes",
        "configurar", "configura", "configuraste", "configuró", "configurará", "configuraría", "configures",
        "generar", "genera", "generaste", "generó", "generará", "generaría", "generes",
        "actualizar", "actualiza", "actualizaste", "actualizó", "actualizará", "actualizaría", "actualices",
        "validar", "valida", "validaste", "validó", "validará", "validaría", "valides",
        "desplegar", "despliega", "desplegaste", "desplegó", "desplegará", "desplegaría", "despliegues",
        "instalar", "instala", "instalaste", "instaló", "instalará", "instalaría", "instales",
        "habilitar", "habilita", "habilitaste", "habilitó", "habilitará", "habilitaría", "habilites",
        "deshabilitar", "deshabilita", "deshabilitaste", "deshabilitó", "deshabilitará", "deshabilitaría", "deshabilites",
        "verificar", "verifica", "verificaste", "verificó", "verificará", "verificaría", "verifiques",
        "comprobar", "comprueba", "comprobaste", "comprobó", "comprobará", "comprobaría", "compruebes",
        "resolver", "resuelve", "resolviste", "resolvió", "resolverá", "resolvería", "resuelvas",
        "registrar", "registra", "registraste", "registró", "registrará", "registraría", "registres",
        "transmitir", "transmite", "transmitiste", "transmitió", "transmitirá", "transmitiría", "transmitas",
        "almacenar", "almacena", "almacenaste", "almacenó", "almacenará", "almacenaría", "almacenes",
        "exportar", "exporta", "exportaste", "exportó", "exportará", "exportaría", "exportes",
        "importar", "importa", "importaste", "importó", "importará", "importaría", "importes",
        "integrar", "integra", "integraste", "integró", "integrará", "integraría", "integres",
        "comparar", "compara", "comparaste", "comparó", "comparará", "compararía", "compares",
        "filtrar", "filtra", "filtraste", "filtró", "filtrará", "filtraría", "filtres",
        "seleccionar", "selecciona", "seleccionaste", "seleccionó", "seleccionará", "seleccionaría", "selecciones",
        "notificar", "notifica", "notificaste", "notificó", "notificará", "notificaría", "notifiques",
        "priorizar", "prioriza", "priorizaste", "priorizó", "priorizará", "priorizaría", "priorices",

        # Frases comunes de instrucciones
        "generar reporte", "establecer conexión", "reiniciar", "cerrar sesión",
        "abrir sesión", "activar modo", "desactivar modo", "enfocar", "escanear", "sincronizar datos",

        # Versiones dirigidas a la persona
        "realices", "ejecutes", "inicies", "completes", "finalices", "culmines", "presentes", "detengas", 
        "acredites", "programes", "organices", "coordines", "crees", "modifiques", "revises", "analices", 
        "confirmes", "implementes", "configures", "generes", "actualices", "valides", "despliegues", "instales", 
        "habilites", "deshabilites", "verifiques", "compruebes", "resuelvas", "registres", "transmitas", 
        "almacenes", "exportes", "importes", "integres", "compares", "filtres", "selecciones", "notifiques", "priorices"
    ]


    
    # Compilamos un patrón de regex que busque cualquiera de las palabras clave (ignora mayúsculas/minúsculas)
    patron = re.compile(r'\b(?:' + '|'.join(map(re.escape, palabras_clave)) + r')\b', re.IGNORECASE)
    
    # Dividir el texto en oraciones usando delimitadores típicos de final de oración (. ! ?)
    oraciones = re.split(r'(?<=[.!?])\s+', texto.strip())
    
    instrucciones = []
    for oracion in oraciones:
        oracion = oracion.strip()
        if not oracion:
            continue
        
        # Buscar todas las coincidencias de palabras clave en la oración
        coincidencias = patron.findall(oracion)
        score = len(coincidencias)
        
        # Si la oración tiene al menos una coincidencia o,
        # si es larga y comienza con un prefijo que sugiere acción,
        # se considera una instrucción.
        if score > 0 or (len(oracion) > 40 and any(
            oracion.lower().startswith(prefijo)
            for prefijo in ("paso", "realiza", "inicia", "ejecuta", "crea", "modifica", "revisa", "analiza", "confirma", "implementa", "configura", "genera", "actualiza", "valida", "despliega")
        )):
            instrucciones.append(oracion)
    
    # Si no se detectaron instrucciones específicas, se retornan todas las oraciones no vacías.
    if not instrucciones:
        instrucciones = [oracion for oracion in oraciones if oracion]
    
    return instrucciones

def formatear_instrucciones(instrucciones):
    """
    Formatea la lista de instrucciones en un texto numerado, ideal para un plan de trabajo.
    
    Parámetros:
        instrucciones (list): Lista de instrucciones.
    
    Retorna:
        str: Texto formateado, donde cada instrucción es precedida por "Paso X:".
    """
    return "\n".join(f"Paso {i+1}: {instr}" for i, instr in enumerate(instrucciones))
