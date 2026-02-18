from app.tools.textsplitternormal import chunk_text
from app.db.pinecone  import get_pinecone_index
from app.services.embedding_service import get_embedding


def ingestdocument(filename:str, text:str):
    if not filename:
        raise ValueError("file name is mandatory")
    if not text:
        raise ValueError("Text is mandatory")
    

    index = get_pinecone_index()

    chunks: List[str] = chunk_text(
        text = text,
        chunk_size = 1000,
        chunk_overlap = 200
    )

    if not chunks :
        raise ValueError("Could chunk the given text")
    
    batch_size = 100
    vector_embeddings = []
    for i in range(0,len(chunks),batch_size):

       genratedEmbeddings = get_embedding(text=chunks[i:i+batch_size],embedding_model ="text-embedding-3-small")
       vector_embeddings.extend(genratedEmbeddings)

    vectors_to_upsert = []

    for chunk_index,(chunk,vector_embedding) in enumerate(zip(chunks,vector_embeddings)):
        vectorid = f"{filename}-{chunk_index}"

        vectors_to_upsert.append({
            "id": vectorid ,
            "values":vector_embedding,
            "metadata":{
                "text":chunk,
                "source":filename,
                "chunk_index": chunk_index
            }
        })
    index.upsert(vectors=vectors_to_upsert)



     
