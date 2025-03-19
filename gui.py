# gui.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit,
    QHBoxLayout, QFileDialog, QMessageBox, QInputDialog, QProgressBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from typing import Callable

# Estilo general inspirado en Apple
GENERAL_STYLE = """
    QWidget {
        background-color: #FFFFFF;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
        font-size: 14px;
    }
    QTextEdit {
        background-color: #F9F9F9;
        border: 1px solid #D1D1D6;
        border-radius: 8px;
        padding: 10px;
    }
    QProgressBar {
        border: 1px solid #D1D1D6;
        border-radius: 8px;
        text-align: center;
        background: #F9F9F9;
    }
    QProgressBar::chunk {
        background-color: #007AFF;
        border-radius: 8px;
    }
"""

def button_style(background_color: str, text_color: str = "#FFFFFF") -> str:
    """Devuelve el estilo para un botón con los colores indicados."""
    return (
        f"background-color: {background_color}; "
        f"color: {text_color}; "
        "border: none; "
        "border-radius: 8px; "
        "padding: 10px 20px;"
    )

class TranscriptorApp(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("AudioFlow Pro")
        self.setGeometry(100, 100, 900, 600)
        self.setWindowIcon(QIcon("app_icon.png"))
        self.setStyleSheet(GENERAL_STYLE)
        self.recorder = None
        self._init_ui()

    def _init_ui(self) -> None:
        """Configura la interfaz de usuario con una distribución moderna."""
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(15)

        # --- Sección superior: Controles de archivo y grabación ---
        top_controls = QHBoxLayout()
        top_controls.setSpacing(15)
        self.btn_seleccionar_archivo = self._create_button(
            "📁 Seleccionar Archivo", self.seleccionar_archivo, button_style("#007AFF")
        )
        top_controls.addWidget(self.btn_seleccionar_archivo)

        self.btn_grabar_audio = self._create_button(
            "🔴 Grabar Audio", self.iniciar_grabacion, button_style("#FF3B30")
        )
        top_controls.addWidget(self.btn_grabar_audio)

        self.btn_detener_grabacion = self._create_button(
            "⏹ Detener Grabación", self.detener_grabacion, button_style("#8E8E93")
        )
        self.btn_detener_grabacion.setEnabled(False)
        top_controls.addWidget(self.btn_detener_grabacion)

        top_controls.addStretch()  # Empuja los botones a la izquierda
        layout_principal.addLayout(top_controls)

        # --- Área de texto para transcripción ---
        self.texto_transcripcion = QTextEdit(self)
        self.texto_transcripcion.setPlaceholderText("Aquí aparecerá la transcripción...")
        self.texto_transcripcion.setReadOnly(True)
        layout_principal.addWidget(self.texto_transcripcion)

        # --- Barra de progreso (inicialmente oculta) ---
        self.progress = QProgressBar(self)
        self.progress.setVisible(False)
        layout_principal.addWidget(self.progress)

        # --- Sección inferior: Controles de procesamiento y exportación ---
        bottom_controls = QHBoxLayout()
        bottom_controls.setSpacing(15)
        self.btn_procesar_texto = self._create_button(
            "📝 Procesar Texto", self.procesar_texto, button_style("#34C759")
        )
        bottom_controls.addWidget(self.btn_procesar_texto)

        self.btn_exportar_txt = self._create_button(
            "📄 Exportar a TXT", self.exportar_txt, button_style("#5856D6")
        )
        bottom_controls.addWidget(self.btn_exportar_txt)

        self.btn_exportar_pdf = self._create_button(
            "📑 Exportar a PDF", self.exportar_pdf, button_style("#FFCC00")
        )
        bottom_controls.addWidget(self.btn_exportar_pdf)

        self.btn_generar_mermaid = self._create_button(
            "📊 Generar Mermaid", self.generar_mermaid, button_style("#5AC8FA")
        )
        bottom_controls.addWidget(self.btn_generar_mermaid)

        self.btn_generar_calendario = self._create_button(
            "📆 Generar Calendario", self.generar_calendario, button_style("#FF2D55")
        )
        bottom_controls.addWidget(self.btn_generar_calendario)

        self.btn_exportar_calendario_excel = self._create_button(
            "📈 Exportar Calendario Excel", self.exportar_calendario_excel, button_style("#4CD964")
        )
        bottom_controls.addWidget(self.btn_exportar_calendario_excel)

        bottom_controls.addStretch()
        layout_principal.addLayout(bottom_controls)

        self.setLayout(layout_principal)

    def _create_button(self, text: str, callback: Callable, style: str) -> QPushButton:
        """Crea un botón con el texto, callback y estilo especificados."""
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        btn.setStyleSheet(style)
        return btn

    def show_progress(self, message: str = "Procesando...") -> None:
        """Muestra la barra de progreso y añade un mensaje al área de texto."""
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Modo indeterminado
        self.texto_transcripcion.append(message)
        QApplication.processEvents()

    def hide_progress(self) -> None:
        """Oculta la barra de progreso."""
        self.progress.setRange(0, 1)
        self.progress.setValue(1)
        self.progress.setVisible(False)

    def seleccionar_archivo(self) -> None:
        """Selecciona un archivo de audio y lo transcribe."""
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar archivo de audio", "",
            "Archivos de audio (*.mp3 *.wav *.ogg *.m4a)"
        )
        if not archivo:
            QMessageBox.warning(self, "Atención", "No seleccionaste ningún archivo.")
            return

        try:
            self.show_progress("Transcribiendo el audio... Esto puede tardar unos momentos.")
            from transcriptor import transcribir_audio  # Importación diferida
            texto = transcribir_audio(archivo)
            self.texto_transcripcion.setPlainText(texto)
            self.hide_progress()
            QMessageBox.information(self, "Éxito", "Transcripción completada.")
        except Exception as e:
            self.hide_progress()
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

    def iniciar_grabacion(self) -> None:
        """Inicia la grabación de audio."""
        try:
            self.texto_transcripcion.setPlainText("Grabando audio...")
            from recorder import AudioRecorder  # Importación diferida
            self.recorder = AudioRecorder()
            self.recorder.start()
            self.btn_grabar_audio.setEnabled(False)
            self.btn_detener_grabacion.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar la grabación: {e}")

    def detener_grabacion(self) -> None:
        """Detiene la grabación, guarda el archivo y lo transcribe."""
        try:
            self.show_progress("Deteniendo grabación y transcribiendo...")
            self.btn_detener_grabacion.setEnabled(False)
            QApplication.processEvents()
            archivo_salida = "grabacion.wav"
            self.recorder.stop(archivo_salida)
            self.btn_grabar_audio.setEnabled(True)
            from transcriptor import transcribir_audio  # Importación diferida
            texto = transcribir_audio(archivo_salida)
            self.texto_transcripcion.setPlainText(texto)
            self.hide_progress()
            QMessageBox.information(self, "Éxito", "Grabación y transcripción completadas.")
        except Exception as e:
            self.hide_progress()
            QMessageBox.critical(self, "Error", f"Error al detener la grabación o transcribir: {e}")

    def procesar_texto(self) -> None:
        """Procesa el texto transcrito para extraer y formatear instrucciones."""
        from text_processor import extraer_instrucciones, formatear_instrucciones  # Importación diferida
        texto_original = self.texto_transcripcion.toPlainText()
        if not texto_original:
            QMessageBox.warning(self, "Advertencia", "No hay texto para procesar.")
            return

        self.show_progress("Procesando texto...")
        instrucciones = extraer_instrucciones(texto_original)
        texto_formateado = formatear_instrucciones(instrucciones)
        self.texto_transcripcion.setPlainText(texto_formateado)
        self.hide_progress()
        QMessageBox.information(self, "Procesado", "El texto se ha procesado en instrucciones.")

    def exportar_txt(self) -> None:
        """Exporta el contenido del área de texto a un archivo TXT."""
        from exporter import exportar_txt  # Importación diferida
        archivo_destino, _ = QFileDialog.getSaveFileName(
            self, "Guardar TXT", "instrucciones.txt", "Archivo de Texto (*.txt)"
        )
        if archivo_destino:
            contenido = self.texto_transcripcion.toPlainText()
            exportar_txt(archivo_destino, contenido)
            QMessageBox.information(self, "Exportado", "Archivo TXT exportado exitosamente.")

    def exportar_pdf(self) -> None:
        """Exporta el contenido del área de texto a un archivo PDF."""
        from exporter import exportar_pdf  # Importación diferida
        archivo_destino, _ = QFileDialog.getSaveFileName(
            self, "Guardar PDF", "instrucciones.pdf", "Archivo PDF (*.pdf)"
        )
        if archivo_destino:
            contenido = self.texto_transcripcion.toPlainText()
            exportar_pdf(archivo_destino, contenido)
            QMessageBox.information(self, "Exportado", "Archivo PDF exportado exitosamente.")

    def generar_mermaid(self) -> None:
        """Genera código Mermaid a partir de las instrucciones y ofrece exportarlo como imagen."""
        from exporter import generar_mermaid, exportar_mermaid_diagrama  # Importación diferida
        instrucciones = [linea.strip() for linea in self.texto_transcripcion.toPlainText().splitlines() if linea.strip()]
        if not instrucciones:
            QMessageBox.warning(self, "Advertencia", "No hay instrucciones para generar Mermaid.")
            return

        self.show_progress("Generando código Mermaid...")
        codigo_mermaid = generar_mermaid(instrucciones)
        self.texto_transcripcion.setPlainText(codigo_mermaid)
        self.hide_progress()
        QMessageBox.information(self, "Mermaid", "Código Mermaid generado y mostrado en el área de texto.")

        respuesta = QMessageBox.question(
            self, "Exportar Diagrama",
            "¿Deseas exportar el diagrama a una imagen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if respuesta == QMessageBox.StandardButton.Yes:
            archivo_imagen, _ = QFileDialog.getSaveFileName(
                self, "Guardar Diagrama", "diagrama.png", "Imágenes (*.png *.jpg *.svg)"
            )
            if archivo_imagen:
                try:
                    exportar_mermaid_diagrama(instrucciones, archivo_imagen)
                    QMessageBox.information(self, "Éxito", f"Diagrama exportado como imagen:\n{archivo_imagen}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo exportar el diagrama:\n{e}")

    def generar_calendario(self) -> None:
        """Genera un documento calendario basado en las instrucciones."""
        from exporter import generar_documento_calendario  # Importación diferida
        instrucciones = [linea.strip() for linea in self.texto_transcripcion.toPlainText().splitlines() if linea.strip()]
        if not instrucciones:
            QMessageBox.warning(self, "Advertencia", "No hay instrucciones para generar el documento calendario.")
            return

        num_sprints, ok = QInputDialog.getInt(self, "Número de Sprints", "Ingrese el número de sprints:", 1, 1)
        if not ok:
            return
        total_days, ok = QInputDialog.getInt(self, "Total de Días", "Ingrese el total de días para realizar el trabajo:", 30, 1)
        if not ok:
            return

        doc_calendario = generar_documento_calendario(instrucciones, num_sprints, total_days)
        self.texto_transcripcion.setPlainText(doc_calendario)
        QMessageBox.information(self, "Calendario", "Documento calendario generado y mostrado en el área de texto.")

    def exportar_calendario_excel(self) -> None:
        """Exporta el calendario generado a un archivo Excel."""
        from exporter import exportar_calendario_excel  # Importación diferida
        instrucciones = [linea.strip() for linea in self.texto_transcripcion.toPlainText().splitlines() if linea.strip()]
        if not instrucciones:
            QMessageBox.warning(self, "Advertencia", "No hay instrucciones para exportar el calendario a Excel.")
            return

        num_sprints, ok = QInputDialog.getInt(self, "Número de Sprints", "Ingrese el número de sprints:", 1, 1)
        if not ok:
            return
        total_days, ok = QInputDialog.getInt(self, "Total de Días", "Ingrese el total de días para realizar el trabajo:", 30, 1)
        if not ok:
            return

        archivo_destino, _ = QFileDialog.getSaveFileName(
            self, "Guardar Calendario Excel", "calendario.xlsx", "Archivos Excel (*.xlsx)"
        )
        if archivo_destino:
            try:
                exportar_calendario_excel(instrucciones, num_sprints, total_days, archivo_destino)
                QMessageBox.information(self, "Exportado", f"Calendario exportado a Excel exitosamente:\n{archivo_destino}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar el calendario a Excel:\n{e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranscriptorApp()
    window.show()
    sys.exit(app.exec())
