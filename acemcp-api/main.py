"""
Ace MCP API Server
A lightweight semantic search API for code indexing
Compatible with acemcp MCP client
"""

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict, Any
import hashlib
import time
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ace MCP API", version="1.0.0")


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Log and return validation errors"""
    logger.error(f"Validation error for {request.url}: {exc.errors()}")
    logger.error(f"Request body: {await request.body()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": str(await request.body())}
    )


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with database for production)
code_index: Dict[str, Dict[str, Any]] = {}
projects: Dict[str, Dict[str, Any]] = {}

# Authentication
API_TOKEN = os.getenv("ACE_API_TOKEN", "dev-token-change-me")


class CodeBlob(BaseModel):
    """Code blob for indexing"""
    content: str
    file_path: Optional[str] = None
    path: Optional[str] = None  # acemcp uses 'path' instead of 'file_path'
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    language: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow extra fields from acemcp client
    
    @property
    def get_file_path(self) -> str:
        """Get file path from either field name"""
        return self.file_path or self.path or "unknown"


class IndexRequest(BaseModel):
    """Request to index code"""
    project_id: Optional[str] = None  # acemcp doesn't send this, we'll infer it
    blobs: List[CodeBlob]
    batch_id: Optional[int] = None
    
    class Config:
        extra = "allow"  # Allow extra fields from acemcp client


class SearchRequest(BaseModel):
    """Request to search code"""
    project_id: str
    query: str
    limit: Optional[int] = 10


class SearchResult(BaseModel):
    """Search result"""
    file_path: str
    content: str
    start_line: int
    end_line: int
    score: float


def verify_token(authorization: Optional[str] = Header(None)):
    """Verify API token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = authorization.replace("Bearer ", "").strip()
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return token


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Ace MCP API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "index": "/api/v1/index",
            "search": "/api/v1/search",
            "projects": "/api/v1/projects"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "indexed_projects": len(projects),
        "total_blobs": len(code_index)
    }


@app.post("/batch-upload")
async def batch_upload(
    request: Request,
    token: str = Depends(verify_token)
):
    """
    Batch upload endpoint - acemcp client expects this exact endpoint name
    """
    try:
        body = await request.json()
        logger.info(f"Received batch-upload request: {body}")
        index_req = IndexRequest(**body)
        return await index_code_impl(index_req)
    except ValidationError as e:
        logger.error(f"Validation error: {e.errors()}")
        logger.error(f"Request body: {body}")
        raise HTTPException(status_code=422, detail={"errors": e.errors(), "body_sample": str(body)[:500]})


@app.post("/api/v1/index")
async def index_code(
    request: IndexRequest,
    token: str = Depends(verify_token)
):
    """
    Alternative index endpoint for manual API calls
    """
    return await index_code_impl(request)


async def index_code_impl(request: IndexRequest):
    try:
        # Infer project_id from file paths if not provided
        if not request.project_id and request.blobs:
            # Extract common path prefix from first blob as project identifier
            first_path = request.blobs[0].get_file_path
            # Use first directory as project name
            project_id = first_path.split('/')[0] if '/' in first_path else "default"
        else:
            project_id = request.project_id or "default"
        
        # Initialize project if not exists
        if project_id not in projects:
            projects[project_id] = {
                "id": project_id,
                "created_at": datetime.utcnow().isoformat(),
                "blob_count": 0,
                "last_indexed": None
            }
        
        # Index each blob
        indexed_count = 0
        for blob in request.blobs:
            # Get file path (handle both 'path' and 'file_path')
            file_path = blob.get_file_path
            start_line = blob.start_line or 0
            end_line = blob.end_line or 0
            
            # Create unique ID for blob
            blob_id = hashlib.md5(
                f"{project_id}:{file_path}:{start_line}".encode()
            ).hexdigest()
            
            # Store blob (in production, generate embeddings here)
            code_index[blob_id] = {
                "project_id": project_id,
                "file_path": file_path,
                "content": blob.content,
                "start_line": start_line,
                "end_line": end_line,
                "language": blob.language,
                "indexed_at": datetime.utcnow().isoformat(),
                # In production, add: "embedding": model.encode(blob.content)
            }
            
            indexed_count += 1
        
        # Update project stats
        projects[project_id]["blob_count"] += indexed_count
        projects[project_id]["last_indexed"] = datetime.utcnow().isoformat()
        
        # Generate blob_names (SHA-256 hashes) for acemcp client compatibility
        blob_names = []
        for blob in request.blobs:
            file_path = blob.get_file_path
            # Calculate blob hash similar to acemcp's calculate_blob_name
            blob_hash = hashlib.md5(f"{project_id}:{file_path}".encode()).hexdigest()
            blob_names.append(blob_hash)
        
        return {
            "status": "success",
            "project_id": project_id,
            "batch_id": request.batch_id,
            "indexed_count": indexed_count,
            "total_blobs": projects[project_id]["blob_count"],
            "blob_names": blob_names  # Required by acemcp client
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {str(e)}")


@app.post("/agents/codebase-retrieval")
async def codebase_retrieval(
    request: Request,
    token: str = Depends(verify_token)
):
    """
    ACE API compatible codebase retrieval endpoint
    Expected by acemcp client for search
    """
    try:
        body = await request.json()
        query = body.get("information_request", "")
        blobs_info = body.get("blobs", {})
        added_blobs = blobs_info.get("added_blobs", [])
        
        if not query:
            return {"formatted_retrieval": "No query provided"}
        
        # Search across all indexed code
        results = []
        query_lower = query.lower()
        
        for blob_id, blob in code_index.items():
            # Search all blobs (ignore added_blobs list since our IDs are different)
            # In production, you'd filter by the blob list
                
            content_lower = blob["content"].lower()
            file_path_lower = blob["file_path"].lower()
            
            # Calculate relevance score
            score = 0.0
            query_words = query_lower.split()
            
            for word in query_words:
                if word in content_lower:
                    score += content_lower.count(word) * 10
                if word in file_path_lower:
                    score += file_path_lower.count(word) * 5
            
            if score > 0:
                results.append({
                    "file_path": blob["file_path"],
                    "content": blob["content"],
                    "score": score
                })
        
        # Sort by score and take top 10
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:10]
        
        # Format results for ACE API compatibility
        if results:
            formatted_text = f"Found {len(results)} relevant code snippets:\n\n"
            for i, result in enumerate(results, 1):
                formatted_text += f"## {i}. {result['file_path']}\n\n```\n{result['content'][:500]}...\n```\n\n"
        else:
            formatted_text = "No relevant code found for your query."
        
        return {
            "formatted_retrieval": formatted_text,
            "results": results
        }
    except Exception as e:
        logger.error(f"Codebase retrieval failed: {e}")
        return {"formatted_retrieval": f"Error: {str(e)}"}


@app.post("/api/v1/search")
async def search_code(
    request: SearchRequest,
    token: str = Depends(verify_token)
) -> Dict[str, Any]:
    """
    Search code using semantic search
    
    In production, this should:
    1. Generate query embedding
    2. Find similar code using vector similarity
    3. Return ranked results
    
    For now, we're using simple keyword matching.
    """
    try:
        project_id = request.project_id
        query = request.query.lower()
        limit = request.limit or 10
        
        if project_id not in projects:
            return {
                "results": [],
                "total": 0,
                "query": request.query
            }
        
        # Simple keyword search (replace with semantic search in production)
        results = []
        for blob_id, blob in code_index.items():
            if blob["project_id"] != project_id:
                continue
            
            content_lower = blob["content"].lower()
            file_path_lower = blob["file_path"].lower()
            
            # Calculate simple relevance score
            score = 0.0
            query_words = query.split()
            
            for word in query_words:
                if word in content_lower:
                    score += content_lower.count(word) * 10
                if word in file_path_lower:
                    score += file_path_lower.count(word) * 5
            
            if score > 0:
                results.append({
                    "file_path": blob["file_path"],
                    "content": blob["content"],
                    "start_line": blob["start_line"],
                    "end_line": blob["end_line"],
                    "score": score
                })
        
        # Sort by score and limit results
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:limit]
        
        return {
            "results": results,
            "total": len(results),
            "query": request.query,
            "project_id": project_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/api/v1/projects")
async def list_projects(token: str = Depends(verify_token)):
    """List all indexed projects"""
    return {
        "projects": list(projects.values()),
        "total": len(projects)
    }


@app.get("/api/v1/projects/{project_id}")
async def get_project(
    project_id: str,
    token: str = Depends(verify_token)
):
    """Get project details"""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return projects[project_id]


@app.delete("/api/v1/projects/{project_id}")
async def delete_project(
    project_id: str,
    token: str = Depends(verify_token)
):
    """Delete a project and all its blobs"""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Delete all blobs for this project
    blob_ids_to_delete = [
        blob_id for blob_id, blob in code_index.items()
        if blob["project_id"] == project_id
    ]
    
    for blob_id in blob_ids_to_delete:
        del code_index[blob_id]
    
    del projects[project_id]
    
    return {
        "status": "success",
        "project_id": project_id,
        "deleted_blobs": len(blob_ids_to_delete)
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
