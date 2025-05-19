from pymongo import MongoClient
from dotenv import load_dotenv
import voyageai
import json
import os
from openai import OpenAI
# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI
mdb_uri = os.getenv("MONGO_URI")
client = MongoClient(mdb_uri)

# Set database and collection names
DB_NAME = "demo_rag_insurance"
COLLECTION_NAME = "claims_final"
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index_claim_description_voyage"
ATLAS_VECTOR_SEARCH_INDEX_PATH = "claimDescriptionEmbeddingVoyage"

def generate_embedding(content: str):

    vo = voyageai.Client()
    documents_embedding = vo.embed(
        content, model="voyage-3", input_type="document"
    ).embeddings[0]
    return documents_embedding


def vector_search(question):
    
    pipeline = [
        {
            "$vectorSearch": {
                "index": ATLAS_VECTOR_SEARCH_INDEX_NAME,
                "path": ATLAS_VECTOR_SEARCH_INDEX_PATH,
                "queryVector": generate_embedding(content=question),
                "numCandidates": 100,
                "limit": 5,
            }
        },
        {
            "$project": {
                "_id": 0,
                "damageDescriptionEmbedding": 0,
                "photoEmbedding": 0,
                "claimDescriptionEmbedding": 0,
                "claimDescriptionEmbeddingVoyage": 0,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]

    semantic_search_results = MONGODB_COLLECTION.aggregate(pipeline).to_list()
    
    return semantic_search_results


def ask_llm(question, semantic_search_results):

    client = OpenAI()

    # Create the body with the new question
    body = {
        "Additional Information": str(semantic_search_results),
        "Instructions": "Be brief and don't go through too many steps",
        "message": question,
    }

    input_text = json.dumps(body)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a insurance claim expert"},
            {"role": "user", "content": input_text},
        ],
    )

    return response.choices[0].message.content


def retrieval(question):

    search_results = vector_search(question)
    response = ask_llm(question, search_results)
    return search_results, response

if __name__ == "__main__":
   retrieval("test")
