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

Type your question in the prompt. To exit, type `sair` (or `exit`).

## How to use the REST API

You can also interact with the project via a REST API using FastAPI.

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

## Usando o DynamoDB Local (para testes)

Você pode rodar o DynamoDB Local usando Docker:

```bash
docker run -p 8001:8001 amazon/dynamodb-local
```

Para que o código utilize o DynamoDB Local, inclua no seu `.env`:

```
DYNAMO_LOCAL=1
```

No modo local, as variáveis `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` do seu `.env` podem ser qualquer valor (exemplo: `fakeMyKeyId` e `fakeSecretAccessKey`).

**Importante:**
- Você precisa criar a tabela localmente antes de usar. Execute:
  ```bash
  python create_table_local.py
  ```
- Quando for usar em produção (AWS), remova a variável `DYNAMO_LOCAL` e use suas credenciais reais no `.env`.

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