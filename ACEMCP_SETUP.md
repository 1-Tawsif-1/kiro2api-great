# Ace MCP Setup Guide

## ✅ Installation Complete!

Ace MCP has been successfully added to your Droid configuration.

---

## 🎯 What is Ace MCP?

**Ace MCP** (Model Context Protocol) is a codebase indexing and semantic search server that provides:
- **Semantic Search**: Find code by meaning, not just keywords
- **Automatic Indexing**: Indexes your codebase automatically before each search
- **Real-time Updates**: Always searches the latest version of your code
- **Smart Context**: Helps AI understand your entire codebase

---

## 📋 Configuration

Your Ace MCP server is configured in `~/.factory/mcp.json`:

```json
{
  "acemcp": {
    "type": "stdio",
    "command": "uvx",
    "args": ["acemcp"],
    "disabled": false
  }
}
```

---

## ⚙️ Ace MCP Settings

On first run, acemcp creates a settings file at `~/.acemcp/settings.toml`.

### Default Settings:

```toml
# Indexing Configuration
BATCH_SIZE = 10                  # Files uploaded per batch
MAX_LINES_PER_BLOB = 800         # Max lines per code chunk

# API Configuration
BASE_URL = "your_api_endpoint"   # Your Ace API endpoint
TOKEN = "your_token"             # Authentication token

# File Types to Index
TEXT_EXTENSIONS = [".py", ".js", ".ts", ".go", ".java", ".cpp", ".c", ".h", ".rs", ".rb", ".php"]

# Exclude Patterns
EXCLUDE_PATTERNS = [
    "node_modules/**",
    ".git/**",
    "dist/**",
    "build/**",
    "*.min.js",
    "__pycache__/**"
]
```

### Configure Settings:

```bash
# Edit the settings file
nano ~/.acemcp/settings.toml

# Or let it auto-generate on first use
# Settings will be created automatically
```

---

## 🚀 Using Ace MCP in Droid

Once configured, Ace MCP tools are available in your Droid session:

### **1. Semantic Code Search**

```bash
# In Droid session
> Search for authentication logic in the codebase

# Ace MCP will:
# 1. Index your current project automatically
# 2. Perform semantic search
# 3. Return relevant code snippets with context
```

### **2. Find Related Code**

```bash
> Find all error handling patterns

> Show me database connection code

> Where is the token refresh logic?
```

### **3. Understand Codebase**

```bash
> Explain how the authentication flow works

> What are the main components of this project?

> How does the streaming response handler work?
```

---

## 🛠️ Available Tools

Ace MCP provides the `search_context` tool:

### **Tool: search_context**

**Purpose**: Semantic search across your codebase

**Parameters**:
- `project_root_path`: Absolute path to your project (automatically set)
- `query`: Natural language search query

**Example Queries**:
```
"logging configuration setup initialization logger"
"user authentication login"
"database connection pool"
"error handling exception"
"API endpoint routes"
```

**Returns**: Code snippets with:
- File paths
- Line numbers
- Relevant code sections
- Context around matches

---

## 📂 Project Configuration

Ace MCP works with your current project automatically. For the kiro2api project:

```bash
# Project root
/Users/zahir/kiro2api-great

# Indexed files include:
- *.go files (main.go, handlers.go, etc.)
- Configuration files
- Documentation

# Automatically excluded:
- node_modules/
- .git/
- vendor/ (if exists)
- Binary files
```

---

## 🎯 Practical Examples

### Example 1: Find Authentication Code
```bash
# In Droid
> Use Ace MCP to find all authentication-related code

# Ace MCP searches for:
# - Token management
# - Auth middleware
# - Refresh token logic
# - Access control
```

### Example 2: Understand Error Handling
```bash
> Show me how errors are handled in this codebase

# Returns code from:
# - server/error_mapper.go
# - server/common.go
# - Error response functions
```

### Example 3: Find Usage Examples
```bash
> Find examples of how to make API requests

# Shows:
# - Test files
# - Handler implementations
# - Client usage patterns
```

---

## 🔄 How It Works

### Automatic Workflow:

1. **You ask a question** in Droid
2. **Ace MCP indexes** new/modified files automatically
3. **Semantic search** finds relevant code
4. **Results returned** with file paths and line numbers
5. **Droid uses context** to answer your question

### Incremental Indexing:

```
First search:  [Index all files] → Search → Results
Second search: [Index only new/modified] → Search → Results
Third search:  [Index only changes] → Search → Results
```

**Benefits**:
- Always up-to-date
- Fast incremental updates
- No manual indexing needed

---

## 🎨 Integration with Other MCP Servers

You now have **two MCP servers** configured:

### **1. Serena** (Code Manipulation)
- Find symbols (functions, classes)
- Navigate code structure
- Edit/refactor code
- Rename symbols

### **2. Ace MCP** (Semantic Search)
- Understand codebase
- Find relevant code by meaning
- Discover patterns
- Contextual search

**Together they provide**:
- Complete codebase understanding
- Precise code navigation
- Intelligent code modifications

---

## 🧪 Testing Ace MCP

### Test in Droid:

```bash
# Start a new Droid session
droid

# Test semantic search
> Find the token refresh implementation

# Expected: Ace MCP returns code from auth/refresh.go

# Test pattern search
> Show me all HTTP handlers

# Expected: Code from server/handlers.go, server/openai_handlers.go

# Test understanding
> How does the proxy authenticate requests?

# Expected: Context from middleware.go and auth logic
```

---

## 📊 Performance Tips

### 1. **First Search is Slower**
```bash
# First time: ~30-60 seconds (indexes everything)
# After that: ~5-10 seconds (incremental)
```

### 2. **Optimize File Types**
```bash
# In ~/.acemcp/settings.toml
# Only index relevant file types

TEXT_EXTENSIONS = [".go", ".md", ".json"]  # For Go projects
```

### 3. **Exclude Large Directories**
```bash
EXCLUDE_PATTERNS = [
    "vendor/**",
    "node_modules/**",
    ".git/**",
    "*.log"
]
```

---

## 🔍 Advanced Configuration

### Custom API Endpoint

If you have your own Ace API instance:

```toml
# ~/.acemcp/settings.toml
BASE_URL = "https://your-ace-api.com"
TOKEN = "your-api-token"
```

### Command Line Arguments

```bash
# Start with custom settings
uvx acemcp --web-port 8080

# Opens web management interface at http://localhost:8080
```

### Environment Variables

```bash
# Override settings via environment
export ACEMCP_BASE_URL="https://api.example.com"
export ACEMCP_TOKEN="your-token"
export ACEMCP_BATCH_SIZE=20
```

---

## 🛡️ Privacy & Security

### Local Processing:
- Code is indexed locally
- Only sends to API if BASE_URL is configured
- Can work offline for local search

### Data Handling:
- Respects .gitignore patterns
- Excludes sensitive files
- No credentials indexed

### Best Practices:
```bash
# Add to .gitignore
.acemcp/
*.acemcp-index

# Exclude sensitive files in settings.toml
EXCLUDE_PATTERNS = [
    "*.env",
    "*.pem",
    "*.key",
    "*secret*",
    "*password*"
]
```

---

## 🐛 Troubleshooting

### Issue: "acemcp not found"
```bash
# Solution: Install acemcp
uvx acemcp --help

# Or check if uvx is working
which uvx
```

### Issue: "No results found"
```bash
# Possible causes:
# 1. Files not indexed yet (wait for first search)
# 2. Query too specific (try broader terms)
# 3. Files excluded by patterns

# Check settings
cat ~/.acemcp/settings.toml
```

### Issue: "Indexing taking too long"
```bash
# Solutions:
# 1. Exclude large directories
# 2. Reduce file types
# 3. Increase BATCH_SIZE

# Edit settings
nano ~/.acemcp/settings.toml
```

### Issue: "Connection error"
```bash
# If using remote API:
# 1. Check BASE_URL is correct
# 2. Verify TOKEN is valid
# 3. Test network connection

# For local-only usage:
# Remove or comment out BASE_URL in settings
```

---

## 📚 Resources

- **PyPI**: https://pypi.org/project/acemcp/
- **MCP Protocol**: https://modelcontextprotocol.io/
- **Factory Droid**: https://docs.factory.ai/
- **Serena MCP**: https://github.com/oraios/serena

---

## ✅ Quick Reference

```bash
# Check Ace MCP status in Droid
/mcp

# View settings
cat ~/.acemcp/settings.toml

# Edit settings
nano ~/.acemcp/settings.toml

# Test acemcp directly
uvx acemcp --help

# Enable/disable in Droid
droid mcp remove acemcp  # Disable
droid mcp add acemcp "uvx acemcp"  # Re-enable
```

---

## 🎉 You're Ready!

Ace MCP is now configured and ready to use with Droid. Try these:

```bash
# Start Droid
droid

# Use semantic search
> Find the authentication middleware

> Show me how streaming responses work

> Where is the error handling logic?

# Ace MCP will provide relevant code snippets!
```

**Tip**: Combine with Serena for powerful code navigation and modification!
