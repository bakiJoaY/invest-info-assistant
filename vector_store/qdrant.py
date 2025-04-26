from langchain_community.embeddings import DashScopeEmbeddings

from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

qdrantVectorStore = None

def get_qdrant_vector_store():
    """获取qdrant向量存储实例"""
    global qdrantVectorStore
    if qdrantVectorStore is None:
        raise ValueError("qdrantVectorStore is not initialized. Please call init_vector_database() first.")
    return qdrantVectorStore

# todo 
def init_vector_database():    
    # todo api-key配置到环境变量中
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v3",
        dashscope_api_key="your_api_key",
    )
    # todo 先存储在memory中，后续改为持久化存储
    qdrantClient = QdrantClient(":memory:")
    qdrantClient.create_collection(
        collection_name="test",
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    )
    global qdrantVectorStore
    qdrantVectorStore = QdrantVectorStore(
        client=qdrantClient,
        collection_name="test",
        embedding=embeddings
    )

def save_vector(docList: List):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,  # chunk size (characters)
        chunk_overlap=50,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )

    for doc in docList:
        docSplits = [split for split in text_splitter.split_documents(doc)]
        #todo 太长得暂时先不处理
        if (len(docSplits) > 10):
            continue
        global qdrantVectorStore
        qdrantVectorStore.add_documents(docSplits)

    #print(splitBatches)

