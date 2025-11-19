# Safe Usage Guide - Avoiding Account Bans

## ⚠️ Why Accounts Get Banned

Your account was likely flagged because:

1. **Automated User-Agent Headers**: The proxy uses hardcoded KiroIDE headers that identify it as automated
2. **High Request Frequency**: Multiple rapid requests in testing
3. **Suspicious Patterns**: Sequential requests with identical headers
4. **Token Abuse Detection**: AWS monitors for proxy/sharing patterns

## 🛡️ Prevention Strategies

### 1. **Rate Limiting** (Most Important)

Add delays between requests to mimic human behavior:

```bash
# DON'T: Rapid fire requests
curl ... & curl ... & curl ...  # ❌ BANNED

# DO: Add delays between requests
curl ...
sleep 3
curl ...
sleep 5
curl ...  # ✅ SAFE
```

**Recommended Delays:**
- Minimum: 2-3 seconds between requests
- Optimal: 5-10 seconds between requests
- For testing: Use sparingly, max 5-10 requests per hour

### 2. **Limit Test Requests**

```bash
# ❌ DON'T: Test extensively
for i in {1..100}; do curl ...; done  # INSTANT BAN

# ✅ DO: Test minimally
curl ...  # Test once
# Wait 10 minutes before next test
```

### 3. **Use Realistic Request Patterns**

```bash
# ❌ Suspicious: All requests identical
curl -d '{"messages":[{"role":"user","content":"hi"}]}'
curl -d '{"messages":[{"role":"user","content":"hi"}]}'  # Same content

# ✅ Natural: Varied conversations
curl -d '{"messages":[{"role":"user","content":"How do I..."}]}'
sleep 5
curl -d '{"messages":[{"role":"user","content":"Can you explain..."}]}'
```

### 4. **Monitor Your Usage**

```bash
# Check remaining credits regularly
curl http://localhost:8080/api/tokens

# If you see 0 credits suddenly, STOP immediately
# Wait 24-48 hours before trying again
```

## 🚫 High-Risk Behaviors to Avoid

### ❌ **NEVER Do These:**

1. **Rapid Sequential Requests**
   ```bash
   # This WILL get you banned:
   for i in {1..10}; do
     curl -X POST http://localhost:8080/v1/messages ...
   done
   ```

2. **Automated Scripts Without Delays**
   ```python
   # Bad:
   for i in range(100):
       response = client.messages.create(...)  # ❌
   
   # Good:
   for i in range(10):  # Limit iterations
       response = client.messages.create(...)
       time.sleep(10)  # Add delay ✅
   ```

3. **Stress Testing**
   ```bash
   # DON'T benchmark or load test with your personal account
   ab -n 1000 http://localhost:8080/  # ❌ INSTANT BAN
   ```

4. **Sharing Your Proxy**
   - Don't let multiple people use your proxy simultaneously
   - Each user should have their own account

## ✅ Safe Usage Patterns

### For Development:

```bash
# Test API once
curl -X POST http://localhost:8080/v1/messages \
  -H "Authorization: Bearer your-token" \
  -d '{"model":"claude-sonnet-4-20250514","max_tokens":100,"messages":[{"role":"user","content":"test"}]}'

# Wait 5 minutes before next test

# Use Claude Code normally (it has built-in rate limiting)
export ANTHROPIC_BASE_URL="http://localhost:8080/v1"
export ANTHROPIC_API_KEY="your-token"
claude-code "help me with my code"

# Wait for response, then ask next question
# Claude Code naturally spaces out requests
```

### For Production:

```python
import anthropic
import time

client = anthropic.Anthropic(
    api_key="your-token",
    base_url="http://localhost:8080/v1"
)

# Good: Natural conversation flow with delays
messages = []
messages.append({"role": "user", "content": "First question"})

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages
)

# Add response to conversation
messages.append({"role": "assistant", "content": response.content[0].text})

# IMPORTANT: Wait before next request
time.sleep(5)  # Minimum 5 seconds

messages.append({"role": "user", "content": "Follow-up question"})
response = client.messages.create(...)
```

## 📊 Safe Request Limits

| Usage Pattern | Max Requests | Delay Between |
|---------------|-------------|---------------|
| **Testing** | 5-10 per hour | 5-10 minutes |
| **Development** | 20-30 per hour | 2-3 minutes |
| **Light Use** | 50-100 per day | 1-2 minutes |
| **Normal Use** | 200-300 per day | 30-60 seconds |

## 🔍 Signs You're About to Get Banned

Watch for these warnings:

1. **Sudden credit drop to 0** - Stop immediately
2. **429 Rate Limit errors** - Slow down significantly
3. **403 Forbidden errors** - Account may be flagged
4. **Token refresh failures** - Account suspended

If you see any of these:
- **STOP using the proxy immediately**
- Wait 24-48 hours
- Check if your account is still active
- Resume with much more conservative usage

## 🛠️ Recommended Setup

### 1. Add Request Logging

Monitor your own usage:

```bash
# Count requests per hour
tail -f kiro2api.log | grep "POST /v1/messages" | wc -l

# If you see more than 30 in an hour, slow down
```

### 2. Use Environment Variables

```bash
# Add to ~/.zshrc
export KIRO_MIN_DELAY=5  # Minimum 5 seconds between requests
export KIRO_MAX_REQUESTS_PER_HOUR=20
```

### 3. Client-Side Rate Limiting

Always implement rate limiting in your application:

```python
from datetime import datetime, timedelta
import time

class RateLimiter:
    def __init__(self, max_per_hour=20):
        self.max_per_hour = max_per_hour
        self.requests = []
    
    def wait_if_needed(self):
        now = datetime.now()
        # Remove requests older than 1 hour
        self.requests = [r for r in self.requests if r > now - timedelta(hours=1)]
        
        if len(self.requests) >= self.max_per_hour:
            wait_time = (self.requests[0] + timedelta(hours=1) - now).total_seconds()
            print(f"Rate limit reached. Waiting {wait_time:.0f} seconds...")
            time.sleep(wait_time + 1)
        
        self.requests.append(now)
        time.sleep(3)  # Minimum delay between requests

limiter = RateLimiter(max_per_hour=20)

# Before each request
limiter.wait_if_needed()
response = client.messages.create(...)
```

## 📝 Account Recovery

If your account is banned:

1. **Wait 24-48 hours** before trying again
2. **Contact Kiro support** if ban persists
3. **Don't create new accounts** - may result in permanent ban
4. **Review your usage patterns** before resuming
5. **Start very slowly** - 1-2 requests per hour at first

## 🎯 Best Practices Summary

✅ **DO:**
- Use realistic delays (5-10 seconds minimum)
- Limit test requests to 5-10 per session
- Monitor your credit usage
- Use Claude Code normally (has built-in limits)
- Add rate limiting to your apps
- Vary your request patterns

❌ **DON'T:**
- Fire multiple rapid requests
- Run automated tests/benchmarks
- Share your proxy with others
- Use loops without delays
- Ignore rate limit warnings
- Test excessively

## 🚀 Recommended Workflow

```bash
# Morning: Check status
curl http://localhost:8080/api/tokens

# Use for real work only
claude-code "help with my project"
# ... natural conversation ...

# Afternoon: Check status again
curl http://localhost:8080/api/tokens

# Evening: Final check
curl http://localhost:8080/api/tokens
```

**Remember**: Treat this like your personal developer account, not a production API. Be conservative!
