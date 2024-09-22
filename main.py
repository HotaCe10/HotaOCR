import sys
import os
import json
import io
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QMenu, QTextEdit, QToolTip, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QDragEnterEvent, QDropEvent, QIcon, QFont
from PyQt5.QtCore import Qt, QBuffer, QIODevice, pyqtSignal, QSize, QTimer
from paddleocr import PaddleOCR
from PIL import Image
import pyperclip
import numpy as np
import locale

class DropZone(QLabel):
    image_dropped = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 20px;
                background-color: #f0f0f0;
            }
        """)
        self.setMinimumHeight(200)  # Increased height of drop zone

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasImage() or event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasImage():
            self.image_dropped.emit(event.mimeData().imageData())
        elif event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.image_dropped.emit(file_path)
        event.acceptProposedAction()

class OCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_languages()
        self.initUI()
        self.ocr = PaddleOCR(use_angle_cls=True, lang=self.get_language())
        self.image = None

    def load_languages(self):
        with open('languages.json', 'r', encoding='utf-8') as f:
            self.languages = json.load(f)
        self.current_language = self.get_language()

    def get_language(self):
        system_locale = locale.getdefaultlocale()[0]
        lang_map = {
            'en': 'en', 'es': 'es', 'fr': 'fr', 'it': 'it', 'de': 'de', 'pt': 'pt', 'nl': 'nl',
            'pl': 'pl', 'sv': 'sv', 'ru': 'ru', 'ja': 'japan', 'ko': 'korean', 'zh': 'ch',
            'ar': 'ar', 'el': 'el', 'hu': 'hu', 'tr': 'tr', 'hi': 'hi', 'he': 'he', 'fi': 'fi',
            'da': 'da', 'no': 'no', 'hr': 'hr', 'th': 'th', 'bg': 'bg', 'vi': 'vi', 'ms': 'ms',
            'uk': 'uk', 'is': 'is', 'fa': 'fa', 'ps': 'ps', 'mn': 'mn', 'sw': 'sw', 'am': 'am',
            'ha': 'ha', 'yo': 'yo'
        }
        for lang_code, paddle_code in lang_map.items():
            if system_locale.startswith(lang_code):
                return paddle_code
        return 'en'

    def initUI(self):
        self.setWindowTitle('HotaOCR') 
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.open_button = self.create_square_button('assets/folder.png', self.openImage)
        button_layout.addWidget(self.open_button)

        self.paste_button = self.create_square_button('assets/paste.png', self.pasteFromClipboard)
        button_layout.addWidget(self.paste_button)

        self.language_button = self.create_square_button('assets/language.png', self.showLanguageMenu)
        button_layout.addWidget(self.language_button)

        self.recognize_button = self.create_square_button('assets/play-button.png', self.recognizeText)
        button_layout.addWidget(self.recognize_button)

        self.info_button = self.create_square_button('assets/info.png', self.showInfo)
        button_layout.addWidget(self.info_button)

        button_layout.addStretch(1)  # This pushes the buttons to the left
        main_layout.addLayout(button_layout)

        # Drop zone and image display
        self.drop_zone = DropZone(self)
        self.drop_zone.image_dropped.connect(self.handle_dropped_image)
        main_layout.addWidget(self.drop_zone)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.image_label)

        # Text display
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.text_edit.customContextMenuRequested.connect(self.showTextContextMenu)
        self.text_edit.setFont(QFont("Arial", 10))  # Reduced font size
        main_layout.addWidget(self.text_edit)

        # Set stretch factors to make image larger and text smaller
        main_layout.setStretchFactor(self.image_label, 3)
        main_layout.setStretchFactor(self.text_edit, 1)

        self.updateLanguage()

    def create_square_button(self, icon_path, connection):
        button = QPushButton(self)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(32, 32))
        button.setFixedSize(QSize(50, 50))
        button.clicked.connect(connection)
        return button

    def updateLanguage(self):
        lang = self.languages[self.current_language]
        self.drop_zone.setText(lang['drag_drop'])
        self.open_button.setToolTip(lang['open_image'])
        self.paste_button.setToolTip(lang['paste_clipboard'])
        self.language_button.setToolTip(lang['change_language'])
        self.recognize_button.setToolTip(lang['recognize_text'])
        self.info_button.setToolTip(lang['show_info'])

    def showLanguageMenu(self):
        menu = QMenu(self)
        lang_names = {
            'en': 'English', 'es': 'Español', 'fr': 'Français', 'it': 'Italiano', 'de': 'Deutsch',
            'pt': 'Português', 'nl': 'Nederlands', 'pl': 'Polski', 'sv': 'Svenska', 'ru': 'Русский',
            'ja': '日本語', 'ko': '한국어', 'zh': '中文', 'ar': 'العربية', 'el': 'Ελληνικά',
            'hu': 'Magyar', 'tr': 'Türkçe', 'hi': 'हिन्दी', 'he': 'עברית', 'fi': 'Suomi',
            'da': 'Dansk', 'no': 'Norsk', 'hr': 'Hrvatski', 'th': 'ไทย', 'bg': 'Български',
            'vi': 'Tiếng Việt', 'ms': 'Bahasa Melayu', 'uk': 'Українська', 'is': 'Íslenska',
            'fa': 'فارسی', 'ps': 'پښتو', 'mn': 'Монгол', 'sw': 'Kiswahili', 'am': 'አማርኛ',
            'ha': 'Hausa', 'yo': 'Yorùbá'
        }
        for lang_code, lang_name in lang_names.items():
            action = menu.addAction(lang_name)
            action.triggered.connect(lambda checked, lc=lang_code: self.changeLanguage(lc))
        menu.exec_(self.language_button.mapToGlobal(self.language_button.rect().bottomLeft()))

    def changeLanguage(self, lang_code):
        self.current_language = lang_code
        self.updateLanguage()
        paddle_lang = self.get_language()
        self.ocr = PaddleOCR(use_angle_cls=True, lang=paddle_lang)

    def handle_dropped_image(self, data):
        if isinstance(data, str):
            self.loadImage(data)
        else:
            self.loadImageFromQImage(data)
        self.recognizeText()  # Automatically recognize text when image is dropped

    def openImage(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.loadImage(file_path)
            self.recognizeText()  # Automatically recognize text when image is opened

    def pasteFromClipboard(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasImage():
            self.loadImageFromQImage(mime_data.imageData())
            self.recognizeText()  # Automatically recognize text when image is pasted
        elif mime_data.hasUrls():
            file_path = mime_data.urls()[0].toLocalFile()
            self.loadImage(file_path)
            self.recognizeText()  # Automatically recognize text when image is pasted

    def loadImage(self, file_path):
        self.image = Image.open(file_path)
        self.displayImage()

    def loadImageFromQImage(self, q_image):
        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        q_image.save(buffer, "PNG")
        pil_im = Image.open(io.BytesIO(buffer.data()))
        self.image = pil_im.convert("RGB")
        self.displayImage()

    def displayImage(self):
        if self.image:
            q_image = QImage(self.image.tobytes(), self.image.width, self.image.height, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def recognizeText(self):
        if self.image:
            result = self.ocr.ocr(np.array(self.image))
            text = '\n'.join([line[1][0] for line in result[0]])
            self.text_edit.setText(text)

    def showTextContextMenu(self, pos):
        menu = QMenu(self)
        copy_action = menu.addAction(self.languages[self.current_language]['copy_text'])
        action = menu.exec_(self.text_edit.mapToGlobal(pos))
        if action == copy_action:
            self.copyTextToClipboard()

    def copyTextToClipboard(self):
        cursor = self.text_edit.textCursor()
        text = cursor.selectedText() if cursor.hasSelection() else self.text_edit.toPlainText()
        pyperclip.copy(text)
        self.showCopyPopup()

    def showCopyPopup(self):
        QToolTip.showText(self.text_edit.mapToGlobal(self.text_edit.rect().center()), 
                          self.languages[self.current_language]['text_copied'], 
                          self.text_edit)
        QTimer.singleShot(2000, QToolTip.hideText)

    def showInfo(self):
        info_text = self.languages[self.current_language]['dependencies_info'] + "\n\n"
        info_text += self.languages[self.current_language]['icons_attribution'] + "\n\n"
        info_text += "Icon Attribution Links:\n"
        info_text += '<a href="https://www.flaticon.com/free-icons/open-folder" title="open folder icons">Open folder icons created by Freepik - Flaticon</a>\n'
        info_text += '<a href="https://www.flaticon.com/free-icons/clipboard" title="clipboard icons">Clipboard icons created by Freepik - Flaticon</a>\n'
        info_text += '<a href="https://www.flaticon.com/free-icons/language" title="language icons">Language icons created by Freepik - Flaticon</a>\n'
        info_text += '<a href="https://www.flaticon.com/free-icons/about" title="about icons">About icons created by Tempo_doloe - Flaticon</a>\n'
        info_text += '<a href="https://www.flaticon.com/free-icons/play-button" title="play button icons">Play button icons created by Those Icons -Flaticon</a>'

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.languages[self.current_language]['info_title'])
        msg_box.setText(info_text)
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setTextInteractionFlags(Qt.TextBrowserInteraction)

        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OCRApp()
    ex.show()
    sys.exit(app.exec_())