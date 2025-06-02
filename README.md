# Best Practices RAG

This project uses RAG (Retrieval-Augmented Generation) with LangChain, OpenAI, and Pinecone to index and query documents from a remote repository.

## Prerequisites

- Python 3.8+
- OpenAI account (for embeddings and LLM)
- Pinecone account (for vector storage)
- AWS account (for DynamoDB usage)

## Installation

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd best-practices-rag
   ```

2. Create and activate a virtual environment (optional, but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   pip install fastapi uvicorn
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```
REPO_URL=<url-of-the-repository-to-be-cloned>
PINECONE_API_KEY=<your-pinecone-key>
PINECONE_INDEX_NAME=<your-pinecone-index-name>
PINECONE_OPENAPI_INDEX_NAME=<your-pinecone-openApi-index-name>
OPENAI_API_KEY=<your-openai-key>

# AWS credentials for DynamoDB
AWS_ACCESS_KEY_ID=<your-aws-access-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
AWS_DEFAULT_REGION=us-east-1

DYNAMO_LOCAL=1
```

## How to index documents

Run the ingestion script to clone the repository and index the `.md` files:

```bash
python ingest.py
```

## How to ask questions (CLI)

After indexing, run the query script:

```bash
python query.py
```

Type your question in the prompt. To exit, type `exit`.

## How to use the REST API

You can also interact with the project via a REST API using FastAPI. Go to the backend folder:

1. Start the API server:
   ```bash
   uvicorn api:app --reload
   ```

2. Access the automatic documentation at:
   http://127.0.0.1:8000/docs

3. Make a POST request to `/ask` with a JSON body:
   ```json
   {
     "thread_id": "my-session-id",
     "question": "What is the purpose of this project?"
   }
   ```
   The response will be:
   ```json
   {
     "answer": "..."
   }
   ```

## Using Local DynamoDB (for testing)

You can run DynamoDB Local using Docker:

```bash
docker run -p 8001:8000 amazon/dynamodb-local
```

To make the code use Local DynamoDB, include in your `.env`:

```
DYNAMO_LOCAL=1
```

In local mode, the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables in your `.env` can be any value (example: `fakeMyKeyId` and `fakeSecretAccessKey`).

**Important:**
- You need to create the table locally before using it. Run:
  ```bash
  python create_table_local.py
  ```
- When using in production (AWS), remove the `DYNAMO_LOCAL` variable and use your real credentials in `.env`.

## How to run the frontend

Enter the frontend folder:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
# or
yarn install
```

Start the development server:
```bash
npm start
# or
yarn start
```

The frontend will be available at `http://localhost:3000`

### Frontend Features
- Chat interface with question and answer timeline
- Loading indicator during response processing
- Thread ID persistence to maintain conversation context

## How to run the backend

Enter the backend folder:
```bash
cd backend
```
And follow the normal instructions for running scripts, installing dependencies, etc, as described at the begining

## Notes

- The `ingest.py` script only clones the repository if it does not already exist in the `repo-isb` folder.
- Only `.md` files from the cloned repository are indexed.
- The `.env` file is in `.gitignore` and will not be versioned.
- If you get a 404 error from Pinecone, make sure you have run `python ingest.py` and that your Pinecone index exists and is correctly named in your `.env` file.
- For DynamoDB usage, you must provide valid AWS credentials in your `.env` file as shown above.

## License

MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 