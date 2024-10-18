from llama_index.llms.groq import Groq
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, PromptTemplate
from llama_index.core import Settings
from llama_index.core.embeddings import resolve_embed_model
import os
from dotenv import load_dotenv
import logging
import sys

def query(message: str):
    # Cargar variables de entorno
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    # Configurar Groq
    llm = Groq(model='llama-3.2-1b-preview', api_key=groq_api_key, is_chat_model=True)

    # Validar la consulta, que no tenga espacios solamente o el mensaje en sí esté vacío
    if message.isspace() or not message:
        return "No puedes realizar consultas vacias"
    
    Settings.llm = llm

    # Configurar el logger, que lo que hace es mostrar todo el proceso en consola
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))  

    # Configurar el contexto de servicio, se encarga de leer los datos y pasarselos al modelo
    embed_model = resolve_embed_model("local:BAAI/bge-large-en")

    Settings.embed_model = embed_model

    # Configurar Settings, le decimos que embedding y LLM tiene que usar

    # Directorios de donde se saca la información
    path_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(path_dir, "data")
    storage_dir = os.path.join(path_dir, 'storage')

    PERSIST_DIR = storage_dir

    # Indexar los archivos si no existe en el almacenamiento
    if not os.path.exists(PERSIST_DIR):
        documents = SimpleDirectoryReader(data_dir).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        # Cargar el índice persistido, guardado en Storage
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context=storage_context, embed_model=embed_model)

    # Cargar el motor de consulta
    query_engine = index.as_query_engine()

    # Realizar la consulta
    result = query_engine.query(message)

    # Devolver el resultado de la consulta
    return str(result)