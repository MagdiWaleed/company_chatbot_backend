import pymongo
from dotenv import load_dotenv
import os

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from dotenv import load_dotenv
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import StorageContext
from llama_index.core.node_parser import SentenceSplitter
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex,StorageContext
from llama_index.core.schema import MetadataMode
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.storage.index_store.mongodb import MongoIndexStore
from llama_index.core import load_index_from_storage

load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

embedd_model = GeminiEmbedding(
    model="models/embeddings-001",
)
llm = Gemini(
    model="models/gemini-2.0-flash"
)

# documents = SimpleDirectoryReader("./data").load_data()

# for i in range(len(documents)):
#     documents[i].excluded_embed_metadata_keys.extend(['page_label',"file_path"])
#     documents[i].excluded_llm_metadata_keys.extend(['page_label',"file_path"])

# parser  = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
# nodes = parser.get_nodes_from_documents(documents,show_progress=True)

# storage_context = StorageContext.from_defaults(
#     docstore=MongoDocumentStore.from_uri(
#         uri=MONGO_URI,
#         db_name="chatbot",
#     ),
#     index_store=MongoIndexStore.from_uri(uri=MONGO_URI, db_name="chatbot")
# )

# vector_index = VectorStoreIndex(
#     nodes,
#     storage_context=storage_context,
#     show_progress=True,
#     embed_model=embedd_model
# )
# vector_id = vector_index.index_id
# print(vector_id)
# Create storage context

client = pymongo.MongoClient(MONGO_URI,)
print("MongoDB connection successful:", client.server_info())



storage_context = StorageContext.from_defaults(
    docstore=MongoDocumentStore.from_uri(uri=MONGO_URI, db_name="chatbot"),
    index_store=MongoIndexStore.from_uri(uri=MONGO_URI, db_name="chatbot")
)

# Load the existing index (replace with your actual index ID)
vector_id = "3ed364c5-b556-40c2-b6de-3ab759df83b1"  # Replace with the ID from your first run
vector_index = load_index_from_storage(
    storage_context=storage_context, 
    index_id=vector_id,
    embed_model=embedd_model
)

query_engine = vector_index.as_query_engine(llm=llm)
print(query_engine.query("in what your company serve and what is it name"))




