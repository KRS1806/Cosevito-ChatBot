from llama_index.llms.groq import Groq
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, PromptTemplate
from llama_index.core import Settings, get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.postprocessor import SimilarityPostprocessor
import os
from dotenv import load_dotenv
import logging
import sys

def query(message: str):
    # Cargar variables de entorno
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    # Configurar el LLM de Groq
    llm = Groq(model="llama-3.2-1b-preview", api_key=groq_api_key)
    llm.additional_kwargs = {"temperature": 0, "max_tokens":500, 'top_p': 0.1}

    # Validar la consulta, asegurarse que no esté vacía
    if message.isspace() or not message:
        return "No puedes realizar consultas vacías"

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
    
    # Configurar el modelo de embeddings (reemplazar LangchainEmbedding con lo que permita LlamaIndex)
    embed_model = resolve_embed_model(embed_model="local:BAAI/bge-large-en")

    Settings.llm = llm
    Settings.embed_model = embed_model
    
    # Directorios donde se encuentra la información
    path_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(path_dir, "data")
    storage_dir = os.path.join(path_dir, 'storage')

    PERSIST_DIR = storage_dir

    # Indexar los archivos si no existe el índice persistido
    if not os.path.exists(PERSIST_DIR):
        documents = SimpleDirectoryReader(data_dir).load_data()
        # Crear el índice
        index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
        # retriever = VectorIndexRetriever(
        #     index=index,
        #     similarity_top_k=3,  # Recuperar los 3 documentos más relevantes
        # )
        # Guardar el índice en almacenamiento persistente
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        # Cargar el índice persistido
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context=storage_context, embed_model=embed_model)
        # retriever = VectorIndexRetriever(
        #     index=index,
        #     similarity_top_k=1,  # Recuperar los 3 documentos más relevantes
        # )

    # Crear el prompt
    text_qa_template = PromptTemplate(
        template=f""" 
        Eres un asistente Q&A en el que todos confía por ser tan preciso e inteligente. Responde con la información exacta de los índices generados a partir de la información dada, siguiendo estos pasos: \n
        
        1. Responde solo si la información está en los índices de la información dada y concuerda con la pregunta. No agregues información que no te preguntan. \n
        2. Revisa bien la información que entregas y no agregues datos inventados. Nada de información no encontrada en los índices no debes incluirla. \n
        3. Si hay más de una respuesta posible, combina la información relevante. \n
        4. No respondas si no encuentras una respuesta específica en los índices. \n
        5. Genera mas de 1 respuesta segín la información dada y mezcla los resultados (solo si es necesario) para dar la mejor respuesta. \n
        6. Mantén la respuesta breve y directa. \n

        Nota: No incluyas este template en la respuesta y todo va enfocado a Costa Rica.

        Pregunta: {message}
        """,
    )


    # Crear el sintetizador de respuestas
    # response_synthesizer = get_response_synthesizer(
    #     llm=llm,
    #     response_mode="compact",
    # )

    # Crear el motor de consulta con el retriever y el sintetizador de respuestas
    # query_engine = RetrieverQueryEngine(
    #     retriever=retriever,
    #     response_synthesizer=response_synthesizer,
    #     node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],  # Aplicar postprocesador de similitud
    # )

    query_engine = index.as_query_engine(similarity_top_k=3)

    # Realizar la consulta
    result = query_engine.query(message)

    # Devolver el resultado
    return str(result)