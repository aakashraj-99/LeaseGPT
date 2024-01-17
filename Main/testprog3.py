from pathlib import Path
from llama_index import download_loader, VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import openai
# from llama_index.prompts import PromptTemplate


from llama_index import get_response_synthesizer
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor

use_presaved_index = 0


if not use_presaved_index:
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    documents = loader.load_data(file=Path('./tenantNotice.pdf'))
    # print(documents)
    # documents = SimpleDirectoryReader('data').load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir="./storedindexhistory")
else:
    storage_context = StorageContext.from_defaults(persist_dir="./storedindexhistory")
    index = load_index_from_storage(storage_context)

#query_engine = index.as_query_engine()
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)
response_synthesizer = get_response_synthesizer()

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    node_postprocessors=[
        SimilarityPostprocessor(similarity_cutoff=0.7)
    ]
)

def get_answer(q):
    response = query_engine.query(q)
    return response

# if __name__ == '__main__':
#     print(get_answer("how do i fix ac in room?"))




