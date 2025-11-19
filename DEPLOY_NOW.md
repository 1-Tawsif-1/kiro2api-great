# 🚀 Deploy Ace MCP API to Render - Quick Guide

## ✅ **Code Pushed to GitHub Successfully!**

**Commit**: `bef7f31 - feat: add Ace MCP API server for code indexing`  
**Repository**: https://github.com/1-Tawsif-1/kiro2api-great  
**Status**: Ready to deploy! 🎉

---

## 📋 **Deploy to Render NOW**

### **Method 1: Automatic with Blueprint (Easiest)**

1. **Go to Render Dashboard**  
   👉 https://dashboard.render.com

2. **Create New Blueprint**
   - Click **"New"** button (top right)
   - Select **"Blueprint"**
   
3. **Connect Repository**
   - Select your GitHub account
   - Choose repository: **1-Tawsif-1/kiro2api-great**
   - Render will detect `render-acemcp.yaml`
   
4. **Review & Deploy**
   - Render shows the service configuration
   - Click **"Apply"**
   - Render will:
     - Create the web service
     - Install dependencies
     - Generate secure API token
     - Deploy automatically
   
5. **Get Your URL**
   - Service will be available at: `https://acemcp-api.onrender.com`
   - Or custom name you choose during setup

---

### **Method 2: Manual Setup (More Control)**

1. **Go to Render Dashboard**  
   👉 https://dashboard.render.com

2. **New Web Service**
   - Click **"New"** → **"Web Service"**
   
3. **Connect GitHub**
   - Select: **1-Tawsif-1/kiro2api-great**
   - Branch: **main**
   
4. **Configure Service**
   ```
   Name:           acemcp-api
   Region:         Oregon (or your choice)
   Branch:         main
   Runtime:        Python 3
   Build Command:  pip install -r acemcp-api/requirements.txt
   Start Command:  cd acemcp-api && python main.py
   ```
   
5. **Add Environment Variables**
   - Click **"Add Environment Variable"**
   - **Key**: `ACE_API_TOKEN`
   - **Value**: Click **"Generate"** for secure random token
     - Or paste your own: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
   
6. **Set Instance Type**
   - Free tier is fine for testing
   - Upgrade to Starter ($7/mo) for production
   
7. **Create Service**
   - Click **"Create Web Service"**
   - Render will build and deploy (takes 2-5 minutes)

---

## 🎯 **After Deployment**

### **Step 1: Get Your API Details**

Once deployed, Render shows:
```
URL:   https://acemcp-api.onrender.com
Token: (check Environment tab for ACE_API_TOKEN)
```

### **Step 2: Test the API**

```bash
# Replace with your actual URL and token
export ACE_URL="https://your-app.onrender.com"
export ACE_TOKEN="your-generated-token"

# Test health
curl $ACE_URL/health

# Should return:
# {"status":"healthy","indexed_projects":0,"total_blobs":0}
```

### **Step 3: Configure acemcp Locally**

```bash
# Edit settings
nano ~/.acemcp/settings.toml
```

Update these lines:
```toml
BASE_URL = "https://your-app.onrender.com"  # Your Render URL
TOKEN = "your-generated-token"               # From Render environment
```

### **Step 4: Re-enable acemcp in Droid**

```bash
# Add acemcp MCP server
droid mcp add acemcp "uvx acemcp"

# Verify configuration
cat ~/.factory/mcp.json
```

### **Step 5: Test It!**

```bash
# Start Droid
droid

# Check MCP status
/mcp

# Should show acemcp as connected

# Test search
> Find all authentication middleware code

# acemcp will now:
# - Index your local code
# - Upload to your Render API
# - Perform search
# - Return results ✅
```

---

## 📊 **Monitoring Your Deployment**

### **View Logs**
```bash
# In Render Dashboard:
# Your Service → Logs tab → View real-time logs
```

### **Check Status**
```bash
curl https://your-app.onrender.com/health
```

### **View Projects**
```bash
curl -H "Authorization: Bearer your-token" \
  https://your-app.onrender.com/api/v1/projects
```

---

## ⚡ **Important Notes**

### **Free Tier Sleep**
- ⚠️ Service sleeps after 15 min of inactivity
- 🐌 First request after sleep is slow (30-60 sec cold start)
- ✅ Subsequent requests are fast

**Solution**: Upgrade to Starter plan ($7/mo) for always-on service

### **Storage**
- ⚠️ Current implementation uses in-memory storage
- 🔄 Data is lost on restart/redeploy
- ✅ Fine for testing and development

**For Production**: Add PostgreSQL or Redis (available as Render add-ons)

---

## 🔧 **Troubleshooting**

### **Issue: Deploy Failed**

Check Render logs for:
```bash
# Build phase errors
pip install -r acemcp-api/requirements.txt

# Start phase errors
cd acemcp-api && python main.py
```

**Solution**: Verify all files are in the repository

### **Issue: Can't Access API**

```bash
# Check if service is running
curl https://your-app.onrender.com/health

# If 502: Service is not started yet (wait 2-3 min)
# If 404: Wrong URL
# If 401: Wrong/missing token
```

### **Issue: acemcp Still Failing**

```bash
# Check acemcp logs
tail -f ~/.acemcp/log/acemcp.log

# Verify settings
cat ~/.acemcp/settings.toml

# Ensure BASE_URL and TOKEN match Render configuration
```

---

## 📱 **Quick Reference**

```bash
# View your deployment
https://dashboard.render.com

# Test health
curl https://your-app.onrender.com/health

# Check Render logs
# Dashboard → Your Service → Logs

# Update acemcp settings
nano ~/.acemcp/settings.toml

# Test in Droid
droid
> search for token manager
```

---

## ✅ **Deployment Checklist**

- [x] Code created (✅ Done)
- [x] Committed to Git (✅ Done - commit bef7f31)
- [x] Pushed to GitHub (✅ Done)
- [ ] **Deploy on Render** (👈 Do this now!)
- [ ] Copy API token from Render
- [ ] Update ~/.acemcp/settings.toml
- [ ] Re-enable acemcp in Droid
- [ ] Test search functionality

---

## 🎯 **What to Do Now**

### **1. Go to Render**
👉 https://dashboard.render.com/new/blueprint

### **2. Select Repository**
- Connect: **1-Tawsif-1/kiro2api-great**
- Render detects: **render-acemcp.yaml**

### **3. Deploy**
- Click **"Apply"**
- Wait 2-5 minutes
- Get your URL

### **4. Configure & Test**
- Update `~/.acemcp/settings.toml`
- Run `droid mcp add acemcp "uvx acemcp"`
- Test in Droid!

---

## 🎉 **Summary**

**Status**: ✅ Code is on GitHub!  
**Commit**: `bef7f31`  
**Next**: Deploy on Render (takes 5 minutes)  
**URL**: Will be `https://your-chosen-name.onrender.com`

Ready to deploy? Go to Render now! 🚀
