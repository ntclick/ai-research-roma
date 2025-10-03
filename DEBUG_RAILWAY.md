# 🔍 Debug Railway Gemini Issue

## ✅ Code đã đúng:
```python
self.gemini_api_key = os.getenv('GOOGLE_API_KEY')  ✓
```

## 🔍 Kiểm tra Railway Variables:

### **Step 1: Verify Variable Name**
Railway Dashboard → Your Project → **Variables** tab

Đảm bảo tên chính xác:
```
GOOGLE_API_KEY   (không phải GEMINI_API_KEY)
```

### **Step 2: Check Variable Value**
Click "eye icon" để xem value, đảm bảo:
- Không có space đầu/cuối
- Key đầy đủ: `AIzaSy...`
- Không có quotes `""`

### **Step 3: Force Restart**
Sau khi sửa variables:
1. Tab **Settings** → Scroll down
2. Click **"Restart Deployment"**
3. HOẶC: Push empty commit để trigger rebuild

### **Step 4: Check Deploy Logs**
Tab **Deployments** → Click deployment mới nhất → **Deploy Logs**

Xem có dòng này:
```
🤖 Worker (Simple Answers): Google Gemini ✓
```

---

## 🧪 Test Manual

Add debug print vào code:

```python
# In api_integrations.py __init__
google_key = os.getenv('GOOGLE_API_KEY')
print(f"[DEBUG] GOOGLE_API_KEY loaded: {google_key[:20]}..." if google_key else "[DEBUG] GOOGLE_API_KEY: NOT FOUND")
```

---

## 🔧 Common Issues:

### Issue 1: Variable Name Typo
❌ `GOOGLE_KEY` 
❌ `GEMINI_API_KEY`
✅ `GOOGLE_API_KEY`

### Issue 2: Variable Not Applied
Railway cần restart để load variables mới:
- Settings → Restart Deployment
- Hoặc push new commit

### Issue 3: API Key Invalid
Test Gemini key manually:
```bash
curl https://generativelanguage.googleapis.com/v1/models?key=YOUR_KEY
```

Should return list of models, not error.

---

## 📋 Current Railway Variables Should Be:

```
GOOGLE_API_KEY = your_google_api_key_here
GOOGLE_MODEL = gemini-1.5-flash
OPENAI_API_KEY = your_openai_api_key_here
COINGECKO_API_KEY = your_coingecko_api_key_here
FAL_API_KEY = your_fal_api_key_here
HOST = 0.0.0.0
```

**Note:** Use your REAL API keys in Railway Dashboard → Variables (they're encrypted there)

---

## 🚀 Quick Fix:

1. Railway Dashboard → Variables
2. Delete `GOOGLE_API_KEY` 
3. Re-add: `GOOGLE_API_KEY` = `AIzaSyCdZoaE4sB6RVBtEYdeB6n9ewveH2X2gkI`
4. Settings → Restart Deployment
5. Check Deploy Logs for ✓

---

**If still failing, screenshot Railway Variables tab and send me!**

