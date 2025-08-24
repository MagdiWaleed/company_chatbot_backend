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



load_dotenv()

embedd_model = GeminiEmbedding(
    model="models/embeddings-001",
)
llm = Gemini(
    model="models/gemini-2.0-flash"
)

documents = SimpleDirectoryReader("./data").load_data()

for i in range(len(documents)):
    documents[i].excluded_embed_metadata_keys.extend(['page_label',"file_path"])
    documents[i].excluded_llm_metadata_keys.extend(['page_label',"file_path"])

parser  = SentenceSplitter(chunk_size=1024, chunk_overlap=20)
nodes = parser.get_nodes_from_documents(documents,show_progress=True)

db = chromadb.PersistentClient(path="./agent/chroma_db")
collection = db.get_or_create_collection(name="collection")

vectorStore = ChromaVectorStore(chroma_collection=collection)
storage_context = StorageContext.from_defaults(vector_store=vectorStore)

index = VectorStoreIndex(
    nodes,storage_context=storage_context,embed_model=embedd_model,show_progress=True
)