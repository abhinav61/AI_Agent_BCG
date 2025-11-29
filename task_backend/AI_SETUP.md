# AI Document Request Setup Guide

## ✅ Complete! Your AI Agent is Ready

### What's Been Added:

1. **AI Agent** (`ai_agent.py`)
   - Uses OpenRouter API with free Llama 3.1 model
   - Generates personalized document request emails
   - API Key already configured: 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

2. **New Backend Endpoints:**
   - `POST /api/candidates/<id>/request-documents` - AI generates & sends email
   - `POST /api/candidates/<id>/submit-documents` - Accept PAN/Aadhaar uploads

3. **Frontend Integration:**
   - "Request Additional Documents" button now connected to AI agent
   - Shows AI-generated email preview in alert
   - Loading state while sending request

## 🚀 How to Use:

### 1. Install New Dependencies:
```cmd
cd C:\Users\ruchi\Documents\task\task_Backend
pip install requests
```

### 2. Restart Flask Server:
```cmd
python app.py
```

### 3. Test the Feature:
1. Go to your React app (http://localhost:5173)
2. Upload a resume or select existing candidate
3. Click "View Details" on any candidate
4. Click "📨 Request Additional Documents"
5. AI will generate a personalized email!

## 📧 Email Configuration (Optional):

The AI will generate emails, but to actually SEND them via email:

1. Add to `.env` file:
```
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

2. For Gmail App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Generate app-specific password
   - Use that password in .env

**Note:** Email sending is optional. The AI will still generate personalized requests even without email configured.

## 🤖 What the AI Does:

When you click "Request Additional Documents":
1. ✅ Fetches candidate details (name, position, company)
2. ✅ Sends data to OpenRouter's free Llama 3.1 model
3. ✅ AI generates personalized, professional email
4. ✅ Saves request to database
5. ✅ Updates candidate status to "Documents Requested"
6. ✅ (Optional) Sends email if SMTP configured

## 📝 Example AI-Generated Email:

```
Dear Abhinav Kumar,

Thank you for your interest in Software Engineer position. To proceed with 
your application, we need to verify your identity documents.

Please upload the following documents within 7 days:
1. PAN Card (clear photo or scanned copy)
2. Aadhaar Card (both front and back)

You can upload these documents through our secure portal. These documents 
are required for verification and onboarding purposes.

Best regards,
HR Team
TraqCheck
```

## ✨ Features:

- 🤖 AI-powered personalized emails
- 🆓 100% FREE (using OpenRouter free tier)
- ⚡ Fast response (Llama 3.1 is optimized)
- 💾 All requests logged in database
- 📊 Candidate status auto-updates
- 🔒 Secure document upload storage

Everything is ready to go! Just restart your Flask server and test it out! 🎉
