from openai import OpenAI
from app.core.config import settings
import logging
__client: OpenAI | None = None
logger = logging.getLogger(__name__)

def get_openai_client()->OpenAI:
      global __client
      if __client is None:
        if not settings.OPENAI_API_KEY:
           raise ValueError("OPENAI_API_KEY is not set")
        __client = OpenAI(api_key=settings.OPENAI_API_KEY)
        logger.info("OpenAI client initialized")

      return __client
     
def get_embedding(text:list[str],embedding_model:str)->list[list[float]]:
    """
    Generate embedding for a given text using OpenAI's embedding model.
    """
    if not embedding_model:
        raise ValueError("embedding_model is not set in get_embedding function")
    if not text:
        raise ValueError("text data  is not set in get_embedding function")
    
    client = get_openai_client()
    response = client.embeddings.create(
    input=text,
    model=embedding_model
    )
    embeddings = [item.embedding for item in response.data]
    logger.info("Embedding generated successfully")
    return embeddings
    