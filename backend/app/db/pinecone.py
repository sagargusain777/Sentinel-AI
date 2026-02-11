
from pinecone import Pinecone,ServerlessSpec
from app.core.config import settings

__pc: Pinecone | None = None
def get_pinecone_client():


    global __pc
    if __pc is None:
        if not settings.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY is not set")
        __pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    return __pc

def get_pinecone_index():
    if not settings.PINECONE_INDEX:
        raise RuntimeError("PINECONE_INDEX is not set")
    pc = get_pinecone_client()
    #Finding the index exist in Pinecone database
    existing_index = [index.name for index in pc.list_indexes()]
    if settings.PINECONE_INDEX not in existing_index:
        print(f"Index '{settings.PINECONE_INDEX}' does not exist. Creating...")

        pc.create_index(
            name=settings.PINECONE_INDEX,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=settings.PINECONE_ENV
            )
        )
    else:
        print(f"Index '{settings.PINECONE_INDEX}' already exists.")
   
    return pc.Index(settings.PINECONE_INDEX)

    
    
