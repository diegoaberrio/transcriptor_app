# recorder.py
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

class AudioRecorder:
    def __init__(self, samplerate=44100, channels=2, dtype='int16'):
        self.samplerate = samplerate
        self.channels = channels
        self.dtype = dtype
        self.frames = []
        self.stream = None

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        # Se almacena una copia de los datos capturados
        self.frames.append(indata.copy())

    def start(self):
        """Inicia la grabación limpiando cualquier dato previo y arrancando el stream."""
        self.frames = []
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            dtype=self.dtype,
            callback=self._callback
        )
        self.stream.start()

    def stop(self, archivo_salida):
        """
        Detiene la grabación, guarda los datos acumulados en un archivo WAV y retorna la ruta.
        """
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        # Concatenar todos los bloques grabados en un solo arreglo
        audio = np.concatenate(self.frames, axis=0)
        wav.write(archivo_salida, self.samplerate, audio)
        return archivo_salida
