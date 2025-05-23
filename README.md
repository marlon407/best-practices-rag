# Best Practices RAG

This project uses RAG (Retrieval-Augmented Generation) with LangChain, OpenAI, and Pinecone to index and query documents from a remote repository.

## Prerequisites

- Python 3.8+
- OpenAI account (for embeddings and LLM)
- Pinecone account (for vector storage)

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
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```
REPO_URL=<url-of-the-repository-to-be-cloned>
PINECONE_API_KEY=<your-pinecone-key>
PINECONE_INDEX_NAME=<your-pinecone-index-name>
OPENAI_API_KEY=<your-openai-key>
```

## How to index documents

Run the ingestion script to clone the repository and index the `.md` files:

```bash
python ingest.py
```

## How to ask questions

After indexing, run the query script:

```bash
python query.py
```

Type your question in the prompt. To exit, type `sair` (or `exit`).

## Notes

- The `ingest.py` script only clones the repository if it does not already exist in the `repo-isb` folder.
- Only `.md` files from the cloned repository are indexed.
- The `.env` file is in `.gitignore` and will not be versioned.

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