# Insurance RAG demo

Create a file named '.env' and store your OpenAI API key and MongoDB connection string in it, follow this format:

```bash
OPENAI_API_KEY=<your key>
MONGO_URI="mongodb+srv://<usr>:<pswd>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority"
```
In MongoDB Atlas create a databse called "demo_rag_insurance" and a collection called "claims_final", import the dataset "demo_rag_insurance.claims.json" into the collection. You have to create two Vector Search Indexes, one for "claimDescriptionEmbedding" called "vector_index_claim_description" and one for "photoEmbedding" called "default":

```json
{
  "fields": [
    {
      "type": "vector",
      "path": "claimDescriptionEmbedding",
      "numDimensions": 350,
      "similarity": "cosine"
    }
  ]
}
```
```json
{
  "fields": [
    {
      "type": "vector",
      "path": "photoEmbedding",
      "numDimensions": 1000,
      "similarity": "cosine"
    }
  ]
}
```

Refer to backend and frontend folder to run both apps