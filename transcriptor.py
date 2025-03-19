# transcriptor.py
import os
import subprocess

def transcribir_audio(archivo):
    """
    Invoca a Whisper para transcribir el audio y retorna el texto resultante.
    Se asume que Whisper está instalado y accesible desde la línea de comandos.
    
    Parámetros:
        archivo (str): Ruta del archivo de audio a transcribir.
    
    Retorna:
        str: Texto transcrito.
    """
    # Directorio donde se guardará la transcripción
    directorio = os.path.dirname(archivo)
    if not directorio:
        directorio = os.getcwd()
    
    # Construir el comando para invocar Whisper.
    # Asegúrate de que el comando 'whisper' esté en el PATH o proporciona la ruta completa.
    comando = f'whisper "{archivo}" --language Spanish --output_dir "{directorio}" --output_format txt'
    
    # Ejecutar el comando. Esto puede tardar dependiendo de la duración del audio.
    subprocess.run(comando, shell=True, check=True)
    
    # Se asume que Whisper genera un archivo .txt con el mismo nombre que el audio.
    archivo_salida = os.path.splitext(archivo)[0] + ".txt"
    with open(archivo_salida, "r", encoding="utf-8") as f:
        texto = f.read()
    return texto
