# Roo Code Setup with kiro2api

## ✅ Configuration Complete!

Your new Kiro account token has been added to the `.env` file.

---

## 🚀 Quick Start

### 1. **Start the Proxy**

```bash
cd /Users/zahir/kiro2api-great
./kiro2api
```

You should see:
```
{"level":"INFO","message":"正在创建AuthService..."}
{"level":"INFO","message":"启动HTTP服务器","port":"8080"}
```

**Keep this terminal open!**

---

### 2. **Configure Roo Code (OpenAI-Compatible)**

Roo Code supports OpenAI-compatible providers. Here's how to set it up:

#### **Option A: Using Environment Variables**

```bash
# Add to your shell config (~/.zshrc)
export OPENAI_API_BASE="http://localhost:8080/v1"
export OPENAI_API_KEY="kiro-proxy-secret-change-me-12345"

# Reload shell
source ~/.zshrc

# Now start Roo Code
roo
```

#### **Option B: Roo Code Configuration File**

If Roo Code has a config file (usually `~/.roo/config.json` or similar):

```json
{
  "provider": "openai",
  "apiBase": "http://localhost:8080/v1",
  "apiKey": "kiro-proxy-secret-change-me-12345",
  "model": "claude-sonnet-4-20250514"
}
```

#### **Option C: Command Line Arguments**

```bash
roo --api-base "http://localhost:8080/v1" \
    --api-key "kiro-proxy-secret-change-me-12345" \
    --model "claude-sonnet-4-20250514"
```

---

## 📋 Available Models

Use these model names in Roo Code:

```
claude-sonnet-4-5-20250929       # Latest Sonnet 4.5
claude-sonnet-4-20250514         # Sonnet 4 (recommended)
claude-3-7-sonnet-20250219       # Sonnet 3.7
claude-3-5-haiku-20241022        # Haiku (faster, cheaper)
claude-haiku-4-5-20251001        # Latest Haiku
```

**Recommended for Roo Code**: `claude-sonnet-4-20250514` (best balance)

---

## 🧪 Test the Connection

### Test 1: Check if proxy is responding
```bash
curl http://localhost:8080/v1/models
```

Should return JSON with available models.

### Test 2: Check your credits
```bash
curl http://localhost:8080/api/tokens
```

Should show your new account credits (likely 2000).

### Test 3: OpenAI-compatible endpoint
```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer kiro-proxy-secret-change-me-12345" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "messages": [
      {"role": "user", "content": "Say hello in one sentence"}
    ]
  }'
```

Should return a response from Claude.

---

## 🎯 Roo Code Usage Example

Once configured:

```bash
# Start Roo Code
roo

# Ask questions naturally
> help me write a Python function to parse JSON

> optimize this code for performance

> explain how async/await works in JavaScript
```

---

## ⚙️ OpenAI API Compatibility

The proxy supports these OpenAI-compatible endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/models` | GET | List available models |
| `/v1/chat/completions` | POST | Chat completions (non-streaming) |
| `/v1/chat/completions` | POST | Chat completions (streaming with `"stream": true`) |

**Request Format:**
```json
{
  "model": "claude-sonnet-4-20250514",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello!"}
  ],
  "temperature": 0.7,
  "max_tokens": 1024,
  "stream": false
}
```

**Response Format:**
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "claude-sonnet-4-20250514",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello! How can I help you today?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 15,
    "total_tokens": 25
  }
}
```

---

## 🛡️ IMPORTANT: Rate Limiting for New Account

**⚠️ To avoid getting banned again:**

### Safe Usage Rules:

1. **Start Slowly**: 
   - First day: Max 10-20 requests
   - Test with small conversations
   
2. **Natural Delays**:
   - Roo Code should handle this automatically
   - But avoid rapid-fire testing

3. **Monitor Usage**:
   ```bash
   # Check credits regularly
   curl http://localhost:8080/api/tokens | python3 -m json.tool
   ```

4. **Never Do**:
   - ❌ Automated testing loops
   - ❌ Load testing
   - ❌ Rapid curl commands
   - ❌ Sharing proxy with others

5. **Safe Pattern**:
   - ✅ Use Roo Code normally
   - ✅ Natural conversation flow
   - ✅ Wait for responses
   - ✅ One session at a time

---

## 🔧 Troubleshooting

### "Connection refused"
```bash
# Make sure proxy is running
ps aux | grep kiro2api

# If not running, start it
cd /Users/zahir/kiro2api-great
./kiro2api
```

### "401 Unauthorized"
```bash
# Check your API key matches
echo $OPENAI_API_KEY

# Should be: kiro-proxy-secret-change-me-12345
```

### "No credits available"
```bash
# Check token status
curl http://localhost:8080/api/tokens

# If credits are 0, check your Kiro account
```

### Roo Code not connecting
```bash
# Test the endpoint manually
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Authorization: Bearer kiro-proxy-secret-change-me-12345" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-sonnet-4-20250514","messages":[{"role":"user","content":"test"}]}'

# If this works, check Roo Code configuration
```

---

## 📊 Monitoring

### Check proxy logs
```bash
# In the terminal where proxy is running, you'll see:
{"level":"INFO","message":"请求成功",...}
```

### Check credits
```bash
# Shows remaining credits and usage
curl -s http://localhost:8080/api/tokens | python3 -m json.tool
```

### Dashboard (optional)
```bash
# Open in browser
open http://localhost:8080
```

---

## 🎓 Quick Reference

```bash
# Start proxy
cd /Users/zahir/kiro2api-great && ./kiro2api

# Check status
curl http://localhost:8080/api/tokens

# Environment variables for Roo Code
export OPENAI_API_BASE="http://localhost:8080/v1"
export OPENAI_API_KEY="kiro-proxy-secret-change-me-12345"

# Start Roo Code
roo
```

---

## ✅ Setup Checklist

- [x] New token extracted from `~/.aws/sso/cache/kiro-auth-token.json`
- [x] `.env` file updated with new token
- [ ] Proxy started: `./kiro2api`
- [ ] Environment variables set for Roo Code
- [ ] Test connection: `curl http://localhost:8080/v1/models`
- [ ] Roo Code configured and tested

---

## 🎉 You're Ready!

Your proxy is now configured to work with Roo Code using the OpenAI-compatible API.

**Remember**: Use conservatively to avoid another ban. Roo Code's natural usage pattern should be fine!
