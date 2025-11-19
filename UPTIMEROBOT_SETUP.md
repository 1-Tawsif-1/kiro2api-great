# UptimeRobot Setup Guide for Ace MCP API

## 🎯 Purpose

Keep your Ace MCP API running 24/7 on Render's free tier by preventing it from sleeping due to inactivity.

---

## 📋 Quick Setup

### 1. Create UptimeRobot Account
- Go to: https://uptimerobot.com
- Sign up for a **free account** (50 monitors included)

### 2. Add New Monitor

**Monitor Settings:**
```
Monitor Type:       HTTP(s)
Friendly Name:      Ace MCP API Health Check
URL:                https://kiro2api-great.onrender.com/health
Monitoring Interval: 5 minutes (minimum for free plan)
Monitor Timeout:    30 seconds
```

**Advanced Settings (Optional):**
```
HTTP Method:        GET
HTTP Auth:          None (health endpoint is public)
Alert Contacts:     Your email (to get notified if API goes down)
```

### 3. Save Monitor

Click **Create Monitor** - that's it! UptimeRobot will now ping your API every 5 minutes.

---

## ✅ Verification

### Check UptimeRobot Dashboard
- Monitor should show **"Up"** status within 5 minutes
- Response time should be < 1 second

### Check Render Logs
Go to: https://dashboard.render.com → Your Service → Logs

You should see entries like:
```
INFO:     ⏰ UptimeRobot ping received at 2025-11-19 14:25:00 UTC
INFO:     ⏰ UptimeRobot ping received at 2025-11-19 14:30:00 UTC
INFO:     ⏰ UptimeRobot ping received at 2025-11-19 14:35:00 UTC
```

### Test Health Endpoint Manually
```bash
curl https://kiro2api-great.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "indexed_projects": 8,
  "total_blobs": 93,
  "timestamp": "2025-11-19T14:30:45.123456"
}
```

---

## 🔧 Configuration Details

### Why This URL?
`https://kiro2api-great.onrender.com/health`

- ✅ **Public endpoint** - No authentication required
- ✅ **Fast response** - Returns immediately
- ✅ **Lightweight** - Doesn't trigger heavy operations
- ✅ **Informative** - Shows API status and indexed data count

### Why 5 Minutes?
- **Free Render** services sleep after 15 minutes of inactivity
- **5-minute pings** keep service awake continuously
- **Free UptimeRobot** allows minimum 5-minute intervals
- Perfect balance to prevent sleeping without excessive requests

---

## 📊 What Gets Logged?

Every UptimeRobot ping logs:
```
⏰ UptimeRobot ping received at 2025-11-19 14:30:00 UTC
```

This helps you verify:
- ✅ UptimeRobot is pinging correctly
- ✅ API is responding to health checks
- ✅ Service stays awake 24/7

---

## 🚨 Troubleshooting

### Monitor Shows "Down"
1. Check Render dashboard - is service running?
2. Test health endpoint manually with curl
3. Check Render logs for errors

### No Ping Logs in Render
1. Verify monitor URL is exactly: `https://kiro2api-great.onrender.com/health`
2. Check UptimeRobot monitor is "Enabled"
3. Wait 5 minutes for next ping

### API Still Sleeping
1. Verify ping interval is 5 minutes (not higher)
2. Check UptimeRobot monitor status is "Up"
3. Ensure URL uses HTTPS (not HTTP)

---

## 💡 Pro Tips

### Monitor Multiple Endpoints
You can add monitors for:
- Health: `https://kiro2api-great.onrender.com/health`
- Root: `https://kiro2api-great.onrender.com/`

### Set Up Alerts
Configure UptimeRobot to email you when:
- API goes down
- Response time exceeds threshold
- SSL certificate expires

### Check Uptime Statistics
UptimeRobot provides:
- 24-hour uptime percentage
- 7-day uptime history
- Response time graphs

---

## ✨ Expected Behavior

**Normal Operation:**
```
[14:25 UTC] ⏰ UptimeRobot ping received
[14:30 UTC] ⏰ UptimeRobot ping received
[14:35 UTC] ⏰ UptimeRobot ping received
[14:40 UTC] ⏰ UptimeRobot ping received
```

Your Ace MCP API will now:
- ✅ Stay awake 24/7
- ✅ Respond instantly to Droid requests
- ✅ Never timeout due to cold starts
- ✅ Maintain indexed data in memory

---

## 🎉 Success!

Once you see regular ping logs every 5 minutes, your API is running 24/7. No more waiting for cold starts when using acemcp!
