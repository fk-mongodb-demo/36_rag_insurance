from pymongo import MongoClient
import voyageai
from dotenv import load_dotenv
import os
load_dotenv()
    
def generate_embedding(content: str):

    vo = voyageai.Client()
    documents_embedding = vo.embed(
        content, model="voyage-3", input_type="document"
    ).embeddings[0]
    return documents_embedding

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_KEY_REGION = os.getenv('AWS_KEY_REGION')

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["demo_rag_insurance"]
collection = db["claims_final"]

for doc in collection.find():    
    text = doc["claimDescription"]
    embedding = generate_embedding(text)
    collection.update_one({"_id": doc["_id"]}, {"$set": {"claimDescriptionEmbeddingVoyage": embedding}})
    