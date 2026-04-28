# FastRetail - Clasificación de imágenes

Proyecto de Programación de Inteligencia Artificial para clasificar automáticamente imágenes de productos de una tienda online usando Amazon Rekognition.

## Descripción

La aplicación permite subir una imagen de un producto, almacenarla en Amazon S3, analizarla con Amazon Rekognition y guardar el resultado en Amazon DynamoDB.

El objetivo es ayudar a FastRetail a automatizar la clasificación de productos como ropa, calzado, accesorios, bolsos y mochilas.

## Tecnologías utilizadas

- Python
- FastAPI
- Amazon Rekognition
- Amazon S3
- Amazon DynamoDB
- Boto3
- HTML
- CSS

## Funcionalidades

- Subida de imágenes desde una interfaz web.
- Almacenamiento de imágenes en Amazon S3.
- Análisis automático con Amazon Rekognition.
- Asignación de categorías de negocio.
- Guardado de resultados en DynamoDB.
- Consulta del histórico de clasificaciones.
- Documentación automática de la API con Swagger.

## Estructura del proyecto

```text
app/
├── main.py
├── aws_services.py
├── config.py
├── category_mapper.py
├── evaluation.py
├── templates/
│   ├── index.html
│   ├── results.html
│   └── history.html
└── static/
    └── style.css
```

## Instalación

Crear y activar un entorno virtual:
```text
python -m venv venv
```

En Windows:
```text
venv\Scripts\activate
```

En Linux/Mac:
```text
source venv/bin/activate
```

Instalar dependencias:
```text
pip install -r requirements.txt
```

## Configuración

Crear un archivo .env tomando como referencia .env.example:
```text
AWS_REGION=us-east-1
S3_BUCKET_NAME=fastretail-product-images-tu-nombre
DYNAMODB_TABLE_NAME=FastRetailImageClassifications
MIN_CONFIDENCE=75

AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_SESSION_TOKEN=your_session_token_here
```

Por seguridad, el archivo .env no se incluye en el repositorio.

## Ejecución

Ejecutar la aplicación con:
```text
uvicorn app.main:app --reload
```

Después abrir en el navegador:
```text
http://127.0.0.1:8000
```

Rutas principales:
/                 Página principal para subir imágenes
/classify         Procesamiento de imagen
/history          Histórico de clasificaciones
/api/history      Histórico en formato JSON
/docs             Documentación automática de la API

Categorías utilizadas
Ropa superior
Ropa inferior
Calzado
Bolsos y mochilas
Accesorios
Seguridad

Las credenciales de AWS no se suben al repositorio.
El archivo .env.example solo contiene valores de ejemplo.

## Autor
Gema Sánchez Navarro
