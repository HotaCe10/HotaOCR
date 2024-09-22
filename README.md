# HotaOCR
OCR App es una aplicación de escritorio multiplataforma para el reconocimiento óptico de caracteres (OCR) en imágenes. Utiliza PaddleOCR para el reconocimiento de texto y PyQt5 para la interfaz gráfica de usuario.
## Características

- Interfaz gráfica de usuario intuitiva
- Soporte para arrastrar y soltar imágenes
- Capacidad para abrir imágenes desde archivos
- Opción para pegar imágenes desde el portapapeles
- Reconocimiento automático de texto al cargar una imagen
- Soporte para múltiples idiomas
- Copiar texto reconocido al portapapeles
- Interfaz multilingüe

## Requisitos previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clona este repositorio:
```

git clone [https://github.com/tu-usuario/ocr-app.git](https://github.com/tu-usuario/ocr-app.git)
```

2. Crea un entorno virtual (opcional, pero recomendado):
```
python -m venv venv

source venv/bin/activate  # En Windows usa venv\Scripts\activate
```

3. Instala las dependencias:
```
pip install -r requirements.txt
```

## Uso

Para ejecutar la aplicación:



1. La aplicación se abrirá con una interfaz gráfica.
2. Puedes cargar una imagen de tres formas:
   - Arrastrando y soltando una imagen en la zona designada
   - Haciendo clic en el botón de abrir imagen y seleccionando un archivo
   - Copiando una imagen al portapapeles y haciendo clic en el botón de pegar
3. Una vez cargada la imagen, el texto se reconocerá automáticamente.
4. Puedes copiar el texto reconocido haciendo clic derecho en el área de texto y seleccionando "Copiar".
5. Para cambiar el idioma de la interfaz o del reconocimiento, utiliza el botón de idioma.

## Estructura del proyecto

- `main.py`: El script principal que ejecuta la aplicación
- `requirements.txt`: Lista de dependencias del proyecto
- `languages.json`: Archivo de traducciones para la interfaz multilingüe
- `assets/`: Directorio que contiene los iconos utilizados en la interfaz

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de crear un pull request. Al contribuir a este proyecto, aceptas que tus contribuciones se licenciarán bajo la misma licencia GPLv3.

## Licencia

Este proyecto está licenciado bajo la GNU General Public License v3.0 (GPLv3). Esto significa que puedes usar, modificar y distribuir este software libremente, pero cualquier trabajo derivado debe distribuirse bajo la misma licencia GPLv3.

Para más detalles, consulta el archivo `LICENSE` en este repositorio o visita [https://www.gnu.org/licenses/gpl-3.0.en.html](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Atribuciones

Esta aplicación utiliza los siguientes recursos de terceros:

- PaddleOCR: [https://github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- PyQt5: [https://www.riverbankcomputing.com/software/pyqt/](https://www.riverbankcomputing.com/software/pyqt/)
- Iconos:
  - Open folder icons created by Freepik - Flaticon
  - Clipboard icons created by Freepik - Flaticon
  - Language icons created by Freepik - Flaticon
  - About icons created by Tempo_doloe - Flaticon
  - Play button icons created by Those Icons - Flaticon
