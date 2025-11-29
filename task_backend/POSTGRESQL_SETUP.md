# PostgreSQL Setup Guide

## Local Development Setup

### 1. Install PostgreSQL

**Windows:**
- Download from https://www.postgresql.org/download/windows/
- Run the installer and remember the password you set for the `postgres` user
- Default port: 5432

### 2. Create Database

Open PowerShell or Command Prompt and run:

```powershell
# Login to PostgreSQL (enter your password when prompted)
psql -U postgres

# Create the database
CREATE DATABASE candidates_db;

# Exit psql
\q
```

### 3. Install Python Dependencies

```powershell
cd task_backend
pip install -r requirements.txt
```

### 4. Set Environment Variable (Optional)

By default, the app connects to: `postgresql://postgres:postgres@localhost:5432/candidates_db`

To use a different connection:

**Windows PowerShell:**
```powershell
$env:DATABASE_URL="postgresql://username:password@localhost:5432/candidates_db"
```

**Or create a `.env` file:**
```
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/candidates_db
```

### 5. Run the Application

```powershell
python app.py
```

The database tables will be created automatically on first run.

---

## Render.com Deployment

### 1. Create PostgreSQL Database on Render

1. Go to https://render.com/
2. Click "New +" → "PostgreSQL"
3. Choose a name (e.g., `candidates-db`)
4. Select "Free" plan
5. Click "Create Database"
6. Copy the **Internal Database URL** (starts with `postgresql://`)

### 2. Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Settings:
   - **Name:** `ai-agent-bcg`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Python 3

### 3. Add Environment Variables

In your web service settings, add:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `<paste your PostgreSQL Internal URL>` |
| `OPENROUTER_API_KEY` | `<your OpenRouter API key>` |
| `EMAIL_ADDRESS` | `<your email>` |
| `EMAIL_PASSWORD` | `<your email app password>` |

### 4. Deploy

Click "Create Web Service" and wait for deployment to complete.

---

## Migrating from SQLite to PostgreSQL

If you have existing data in SQLite:

1. **Export SQLite data:**
```powershell
sqlite3 candidates.db .dump > dump.sql
```

2. **Convert to PostgreSQL format:**
- Replace `INTEGER PRIMARY KEY AUTOINCREMENT` with `SERIAL PRIMARY KEY`
- Replace `?` placeholders with `%s`
- Replace `BOOLEAN DEFAULT 0` with `BOOLEAN DEFAULT FALSE`

3. **Import to PostgreSQL:**
```powershell
psql -U postgres -d candidates_db -f dump.sql
```

---

## Troubleshooting

### Connection Error
- Verify PostgreSQL is running: `pg_isready`
- Check connection string format
- Ensure database exists

### Permission Denied
- Grant permissions: `GRANT ALL PRIVILEGES ON DATABASE candidates_db TO postgres;`

### Port Already in Use
- Change port in connection string or stop conflicting service

---

## Connection String Format

```
postgresql://[user[:password]@][host][:port][/dbname]
```

Examples:
- Local: `postgresql://postgres:password@localhost:5432/candidates_db`
- Render: `postgresql://user:pass@dpg-xxx.oregon-postgres.render.com/dbname`
