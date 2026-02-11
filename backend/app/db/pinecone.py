
from pinecone import Pinecone,ServerlessSpec
from app.core.config import settings

__pc: Pinecone | None = None
def get_pinecone_client():


    global __pc
    if not settings.PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is not set")
    __pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    return __pc

def get_pinecone_index():
    __pc = get_pinecone_client()
    #Finding the index exist in Pinecone database
    existing_index = [index.name for index in __pc.list_indexes()]
    if settings.PINECONE_INDEX  in existing_index:
        print(f"Index '{settings.PINECONE_INDEX}' already exists.")
        return __pc.Index(settings.PINECONE_INDEX)
    else:
        print(f"Index '{settings.PINECONE_INDEX}' does not exist. Creating...")

        __pc.create_index(
            name=settings.PINECONE_INDEX,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud = "aws",
                region=settings.PINECONE_ENV
            )
        )
        return __pc.Index(settings.PINECONE_INDEX)

    
    
