# 🍋 Lemon Automation - Sistema de Automatización para Soporte

## 📌 Tabla de Contenidos
- [Características Principales](#-características-principales)
- [Diseño y Decisiones Técnicas](#-diseño-y-decisiones-técnicas)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Ejecución](#-ejecución)
- [Documentación API](#-documentación-api)

## 🚀 Características Principales

| Módulo               | Funcionalidades                                                                 |
|----------------------|---------------------------------------------------------------------------------|
| **Email Processor**  | Clasificación automática, extracción de CVU, generación de resúmenes con NLP    |
| **Intent Classifier**| Modelo de ML para categorizar consultas, sistema de respuestas configurables     |
| **RAG System**       | Base de datos vectorial, búsqueda semántica, generación de respuestas contextuales|
| **API**              | Endpoints para integración                                                        |

## 🛠️ Diseño y Decisiones Técnicas
Se realizo web scrapping (lemon_scraper.py) con selenium al centro de ayuda de lemon (https://help.lemon.me/es/) y se genero un faq.json. Con esta información se creo la base de datos vectorial

### Decisiones Clave

#### Procesamiento de Emails:
- Optamos por un sistema híbrido (reglas + ML) para clasificación
- Clasificamos en diferentes categorias
- Extracción de CVU 
- Generar un resumen de cada email

#### Clasificador de Intenciones:
- Selección de LinearSVC por buen desempeño en texto corto
- Dataset balanceado con 40 ejemplos por categoría
- Sistema de respuestas configurables sin reentrenar

#### Sistema RAG:
- Elección de FAISS por eficiencia con embeddings
- Modelo multilingual para soporte en español

#### API Design:
- Patrón de inyección de dependencias
- Validación estricta de inputs
- Códigos de error HTTP semánticos


## 📁 Estructura del Proyecto
```text
📦 lemon/
├── 📂 api                          # API REST con Flask
│   ├── 📂 utils                    # logging
│   ├── 📄 app.py                   # Crear aplicación Flask
│   ├── 📄 chatbot_handler.py       # 
│   ├── 📄 dependencies.py          # Instanciar RAG y Intent
│   ├── 📄 endpoints.py             # Endpoint consulta API
│   └── 📄 schemas.py               # Validad Estructura de la solicitud
├── 📂 data                         # Datos y recursos
│   ├── 📂 input_emails             # Ejemplos .json/.csv
│   └── 📂 output                   # CSV procesado
├── 📂 email_processor              # Procesamiento de emails
│   ├── 📄 classifier.py            # Clasificación
│   ├── 📄 cvu_extractor.py         # Extracción CVU
│   ├── 📄 procesor.py              # Procesa emails
│   └── 📄 summarizer.py            # Resúmenes NLP
├── 📂 intent_classifier            # Clasificación de intenciones
│   ├── 📂 data                     # Datos y recursos
|   |    ├── 📂 models
|   |    │   └── intent_model.pkl   # Modelo entrenado
|   |    └── intents_dataset.csv    # Dataset de entrenamiento
│   ├── 📄 dataset_generator.py     # Genera el dataset
│   ├── 📄 predictor.py             # Predice
│   └── 📄 trainer.py               # Entrena
├── 📂 rag_system                   # Sistema RAG completo
|   ├── 📂 data                     # Datos y recursos
|   |    ├── 📂 embeddings          # 
│   |    |   ├── index.faiss         
│   |    |   └── metadata.json       
|   |    └──  📂 help_center/         
│   |         └── faq.json          # Informacion de centro ayuda
│   ├── 📄 generator.py             # Genera las respuestas
│   ├── 📄 retriever.py             # Construye indece y busqueda semantica
│   └── 📄 vector_db.py             # Construye base de dato vectorial
├── 📂 tests                        # Pruebas unitarias
├── 📄 config.py                    # Configuracion
└── requirements.txt                # Dependencias
```

## 🔧 Instalación

### Requisitos
- Python 3.8+
- pip 20+

### Pasos
1. Clonar repositorio:

        git clone https://github.com/tu-usuario/lemon.git
        cd lemon
2. Instalar dependencias:

        pip install -r requirements.txt
<!-- 3. Descargar modelos NLP:

        python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')" -->

## 🏃 Ejecución

1. Procesamiento de Emails:

    - Procesar archivo específico:

            python -m email_processor.processor --input data/input_emails/emails.json --output results.csv

    - Procesar todo un directorio:

            python -m email_processor.processor --dir data/input_emails/
2. Clasificador de Intenciones:

    <!-- - Entrenar modelo (requiere dataset) -->
    <!-- - python -m intent_classifier.trainer -->

    - Probar predicción

            python -m intent_classifier.predictor --text "¿Cómo retiro mis criptomonedas?"
3. Sistema RAG:

    - Reconstruir índice vectorial

            python -m rag_system.retriever --rebuild

    - Consulta interactiva

            python -m rag_system.query --question "¿Cómo activo mi tarjeta?"
4. API REST:

    - Iniciar servidor desarrollo

            python -m api.app

## 🌐 Documentación API

### Endpoints Principales
| Endpoint              | Método        |   Descripción                                  |
|-----------------------|---------------|------------------------------------------------|
| **/api/v1/chat**      | POST          | Chat principal (integra RAG + clasificador)    |
| **/api/v1/rag/query** | POST          | Consulta directa al sistema RAG                |


### Ejemplo cURL:
    curl -X POST http://localhost:5000/api/v1/chat \
    -H "Content-Type: application/json" \
    -d '{"message":"¿Cómo activo mi tarjeta Lemon?", "use_rag": false}'

    Response:
        {
                "confidence": 0.6034479861678984,
                "intent": "Denuncia de Tarjeta Perdida",
                "response": "",
                "response_type": "intent",
                "status": "success"
        }

    curl -X POST http://localhost:5000/api/v1/chat \
    -H "Content-Type: application/json" \
    -d '{"message":"¿Cómo activo mi tarjeta Lemon?", "use_rag": true}'

    Response:
        {
                "response": "Activá tu Lemon Card y empezá a operar en cualquier comercio con pesos argentinos o crypto.\nPodés activar tu Lemon Card siguiendo estos simples pasos:\nIngresá a la App.\n\n**Relevancia:** 77%",
                "response_type": "rag",
                "sources": [
                        {
                                "title": "¿Cómo activo mi tarjeta?",
                                "url": "https://help.lemon.me/es/articles/5444856-como-activo-mi-tarjeta"
                        }
                ],
                "status": "success"
        }

