import sys
from googletrans import Translator
import pytesseract
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Программа для перевода текста")
        self.resize(800, 800)
        self.original_text_area = QTextEdit()
        self.original_text_area.setReadOnly(True)
        self.translated_text_area = QTextEdit()
        self.translated_text_area.setReadOnly(True)
        self.load_image_button = QPushButton("Загрузить изображение")
        self.load_image_button.clicked.connect(self.load_image)
        self.clear_button = QPushButton("Очистить")
        self.clear_button.clicked.connect(self.clear_text)
        layout = QVBoxLayout()
        layout.addWidget(self.original_text_area)
        layout.addWidget(self.translated_text_area)
        layout.addWidget(self.load_image_button)
        layout.addWidget(self.clear_button)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.translator = Translator()

    def load_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить изображение", "",
                                                   "Изображения (*.png *.jpg *.jpeg)", options=options)
        if file_path:
            try:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                translation = self.translate_text(text)
                self.original_text_area.setText(text)
                self.translated_text_area.setText(translation)
            except Exception as e:
                self.clear_text()
                print(f"Ошибка при загрузке и обработке изображения: {str(e)}")

    def translate_text(self, text):
        try:
            translation = self.translator.translate(text, src="en", dest="ru").text
            return translation
        except Exception as e:
            print(f"Ошибка при переводе текста: {str(e)}")
            return ""

    def clear_text(self):
        self.original_text_area.clear()
        self.translated_text_area.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
