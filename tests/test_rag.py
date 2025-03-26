from rag_system import RAGSystem

# Inicializar con la versión que prefieras
rag = RAGSystem()  # Usará la versión por defecto

# Probar con diferentes preguntas
questions = [
    "¿Cómo activo mi tarjeta Lemon?",
    "¿Qué hago si olvidé mi contraseña?",
    "¿Cuáles son los límites de transferencia?"
]

for question in questions:
    print(f"\nPregunta: {question}")
    response = rag.query(question)
    print("Respuesta:", response["answer"])
    print("Fuentes:")
    for src in response["sources"]:
        print(f"- {src['title']}")