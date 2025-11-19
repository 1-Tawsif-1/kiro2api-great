# Ace MCP API Server

A lightweight API server for code indexing and semantic search, compatible with the acemcp MCP client.

## Features

- **Code Indexing**: Accept and store code blobs for semantic search
- **Search API**: Query indexed code with keyword matching
- **Project Management**: Organize code by projects
- **Authentication**: Token-based API security
- **Fast & Lightweight**: Built with FastAPI

## API Endpoints

### Health Check
```bash
GET /
GET /health
```

### Indexing
```bash
POST /api/v1/index
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
  "project_id": "my-project",
  "blobs": [
    {
      "content": "func main() { ... }",
      "file_path": "main.go",
      "start_line": 1,
      "end_line": 10,
      "language": "go"
    }
  ]
}
```

### Search
```bash
POST /api/v1/search
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN

{
  "project_id": "my-project",
  "query": "authentication middleware",
  "limit": 10
}
```

### Project Management
```bash
# List projects
GET /api/v1/projects
Authorization: Bearer YOUR_TOKEN

# Get project details
GET /api/v1/projects/{project_id}
Authorization: Bearer YOUR_TOKEN

# Delete project
DELETE /api/v1/projects/{project_id}
Authorization: Bearer YOUR_TOKEN
```

## Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ACE_API_TOKEN=your-secret-token
export PORT=8000

# Run server
python main.py

# Or with uvicorn
uvicorn main:app --reload --port 8000
```

### Render Deployment

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build/start commands:
   - **Build Command**: `pip install -r acemcp-api/requirements.txt`
   - **Start Command**: `cd acemcp-api && python main.py`
4. Add environment variable:
   - `ACE_API_TOKEN`: Your secure token
5. Deploy!

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ACE_API_TOKEN` | API authentication token | `dev-token-change-me` |
| `PORT` | Server port | `8000` |

## Usage with acemcp

After deploying, configure acemcp to use your API:

```toml
# ~/.acemcp/settings.toml
BASE_URL = "https://your-app.onrender.com"
TOKEN = "your-secret-token"
BATCH_SIZE = 10
MAX_LINES_PER_BLOB = 800
```

Then use acemcp normally:
```bash
droid
> search for authentication code
```

## Architecture

```
┌─────────────────┐
│  acemcp client  │
│  (MCP server)   │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI       │
│   /api/v1/*     │
├─────────────────┤
│ In-Memory Store │ ← Replace with DB for production
│ (dict storage)  │
└─────────────────┘
```

## Production Improvements

For production use, consider:

1. **Vector Database**: Use ChromaDB, Pinecone, or Weaviate for true semantic search
2. **Embeddings**: Add sentence-transformers for code embeddings
3. **Persistent Storage**: Use PostgreSQL or MongoDB
4. **Caching**: Add Redis for frequently searched queries
5. **Rate Limiting**: Protect against abuse
6. **Monitoring**: Add logging and metrics

## Security

- Always use strong tokens in production
- Enable HTTPS (Render provides this automatically)
- Implement rate limiting for API endpoints
- Validate all inputs
- Consider adding user authentication

## License

MIT License - Use freely for your projects
