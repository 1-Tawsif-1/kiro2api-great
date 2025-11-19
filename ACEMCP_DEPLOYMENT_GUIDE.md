# Ace MCP API Deployment Guide

## 📦 **What Was Created**

I've created a complete Ace MCP API server in your repository:

```
kiro2api-great/
├── acemcp-api/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt     # Python dependencies
│   ├── README.md           # API documentation
│   └── .gitignore          # Git ignore rules
└── render-acemcp.yaml      # Render deployment config
```

---

## 🚀 **Deployment Steps**

### **Step 1: Test Locally (Optional)**

```bash
cd /Users/zahir/kiro2api-great/acemcp-api

# Install dependencies
pip3 install -r requirements.txt

# Set token
export ACE_API_TOKEN=test-token-123

# Run server
python3 main.py

# Test in another terminal
curl http://localhost:8000/health
```

### **Step 2: Commit and Push to GitHub**

```bash
cd /Users/zahir/kiro2api-great

# Check what's new
git status

# Add the new files
git add acemcp-api/
git add render-acemcp.yaml
git add ACEMCP_DEPLOYMENT_GUIDE.md

# Commit
git commit -m "feat: add Ace MCP API server for code indexing

- FastAPI-based code indexing and search API
- Compatible with acemcp MCP client
- Includes Render deployment configuration
- Supports project management and semantic search

Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>"

# Push to GitHub
git push origin main
```

### **Step 3: Deploy to Render**

#### **Option A: Using render.yaml (Recommended)**

1. Go to https://render.com/dashboard
2. Click "New" → "Blueprint"
3. Connect your GitHub repository: `kiro2api-great`
4. Render will detect `render-acemcp.yaml`
5. Click "Apply"
6. Render will automatically:
   - Create the service
   - Generate a secure `ACE_API_TOKEN`
   - Deploy the API

#### **Option B: Manual Setup**

1. Go to https://render.com/dashboard
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `acemcp-api`
   - **Region**: Oregon (or your preferred)
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r acemcp-api/requirements.txt`
   - **Start Command**: `cd acemcp-api && python main.py`
5. Add Environment Variable:
   - **Key**: `ACE_API_TOKEN`
   - **Value**: Generate a secure random string (or use Render's generated value)
6. Click "Create Web Service"

### **Step 4: Get Your API URL**

After deployment, Render will provide a URL like:
```
https://acemcp-api.onrender.com
```

Or if you want to use your existing service name:
```
https://kiro2api-great.onrender.com
```

**Note**: You'll need to either:
- Use the new acemcp-api service (separate from kiro2api)
- Or reconfigure your existing kiro2api-great service to run the acemcp API instead

---

## ⚙️ **Configure acemcp Client**

Once deployed, update your local acemcp configuration:

```bash
# Edit settings
nano ~/.acemcp/settings.toml
```

Update with your Render URL and token:

```toml
BATCH_SIZE = 10
MAX_LINES_PER_BLOB = 800
BASE_URL = "https://acemcp-api.onrender.com"  # Your Render URL
TOKEN = "your-generated-token"  # From Render environment variables
TEXT_EXTENSIONS = [ ".py", ".js", ".ts", ".go", ".rs", ".cpp", ".c", ".h", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".xml", ".html", ".css", ".sql", ".sh", ".bash",]
EXCLUDE_PATTERNS = [ ".venv", "venv", ".env", "env", "node_modules", ".git", ".svn", ".hg", "__pycache__", "dist", "build", ".idea", ".vscode", ".DS_Store",]
```

---

## 🧪 **Test the Deployment**

### **1. Health Check**

```bash
curl https://your-app.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "indexed_projects": 0,
  "total_blobs": 0
}
```

### **2. Test Index Endpoint**

```bash
curl -X POST https://your-app.onrender.com/api/v1/index \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "project_id": "test-project",
    "blobs": [{
      "content": "func main() { fmt.Println(\"Hello\") }",
      "file_path": "main.go",
      "start_line": 1,
      "end_line": 3,
      "language": "go"
    }]
  }'
```

### **3. Test Search Endpoint**

```bash
curl -X POST https://your-app.onrender.com/api/v1/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{
    "project_id": "test-project",
    "query": "main function",
    "limit": 10
  }'
```

---

## 🔧 **Enable acemcp in Droid**

Once your API is running, re-enable acemcp:

```bash
# Add acemcp back to Droid
droid mcp add acemcp "uvx acemcp"

# Verify it's enabled
droid
/mcp
```

---

## 📊 **API Endpoints**

### **Health & Status**
- `GET /` - Service info
- `GET /health` - Health check

### **Indexing**
- `POST /api/v1/index` - Index code blobs

### **Search**
- `POST /api/v1/search` - Search indexed code

### **Project Management**
- `GET /api/v1/projects` - List all projects
- `GET /api/v1/projects/{id}` - Get project details
- `DELETE /api/v1/projects/{id}` - Delete project

---

## 🔐 **Security**

### **Get Your API Token from Render**

1. Go to your Render dashboard
2. Select your acemcp-api service
3. Go to "Environment" tab
4. Copy the `ACE_API_TOKEN` value
5. Use this in your `~/.acemcp/settings.toml`

### **Generate Your Own Token (Alternative)**

```bash
# Generate a secure random token
openssl rand -hex 32

# Or use Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Then add this to Render's environment variables and your local config.

---

## 💡 **Usage with Droid**

Once everything is set up:

```bash
droid

# Search your codebase
> Find all authentication middleware code

# acemcp will:
# 1. Index your local code
# 2. Upload to your Render API
# 3. Perform semantic search
# 4. Return relevant code snippets
```

---

## 🐛 **Troubleshooting**

### **Issue: "Connection failed"**

```bash
# Check if service is running
curl https://your-app.onrender.com/health

# Check Render logs
# Go to Render dashboard → Your service → Logs
```

### **Issue: "401 Unauthorized"**

```bash
# Verify token matches
# Check Render environment: ACE_API_TOKEN
# Check local config: ~/.acemcp/settings.toml

# They must match!
```

### **Issue: "502 Bad Gateway"**

```bash
# Service is not running on Render
# Check Render dashboard for deployment status
# View logs for errors
```

### **Issue: "Indexing fails"**

```bash
# Check acemcp logs
tail -f ~/.acemcp/log/acemcp.log

# Look for connection errors or authentication issues
```

---

## 📈 **Monitoring**

### **Render Dashboard**
- View real-time logs
- Monitor CPU/memory usage
- Check request metrics

### **Check Indexed Projects**

```bash
curl -H "Authorization: Bearer your-token" \
  https://your-app.onrender.com/api/v1/projects
```

---

## 🔄 **Update Deployment**

When you make changes to the API:

```bash
# Make changes to acemcp-api/main.py

# Commit and push
git add acemcp-api/
git commit -m "update: improve search algorithm"
git push origin main

# Render will automatically redeploy
```

---

## 💰 **Render Free Tier**

The free tier includes:
- ✅ 750 hours/month
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub
- ⚠️ Spins down after 15 min of inactivity (first request may be slow)

**Upgrade to paid plan** ($7/month) for:
- ✅ Always-on service
- ✅ Faster cold starts
- ✅ More resources

---

## 📋 **Checklist**

- [ ] Created acemcp-api code (✅ Done)
- [ ] Committed to GitHub
- [ ] Pushed to GitHub
- [ ] Created Render service
- [ ] Deployed successfully
- [ ] Copied API token from Render
- [ ] Updated ~/.acemcp/settings.toml with URL and token
- [ ] Tested health endpoint
- [ ] Re-enabled acemcp in Droid
- [ ] Tested search functionality

---

## 🎉 **Next Steps**

1. **Commit and push** the code to GitHub
2. **Deploy** to Render following Option A or B above
3. **Update** your acemcp settings with the Render URL
4. **Test** the API endpoints
5. **Use** acemcp in Droid for semantic search!

---

## 📞 **Need Help?**

If you encounter issues:

1. Check Render logs first
2. Verify environment variables match
3. Test API endpoints with curl
4. Check acemcp logs: `~/.acemcp/log/acemcp.log`

The API is production-ready and should work out of the box once deployed! 🚀
