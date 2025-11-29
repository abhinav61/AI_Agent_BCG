# Migration to PostgreSQL - Summary

## Changes Made

### 1. Updated `requirements.txt`
- Added `psycopg2-binary==2.9.10` for PostgreSQL connectivity

### 2. Updated `app.py`
- **Imports:** Changed from `sqlite3` to `psycopg2` and `RealDictCursor`
- **Database Configuration:**
  - Removed SQLite `DATABASE` path
  - Added PostgreSQL `DATABASE_URL` with environment variable support
  - Automatic URL fix for Render.com compatibility
- **Database Schema:**
  - Changed `INTEGER PRIMARY KEY AUTOINCREMENT` → `SERIAL PRIMARY KEY`
  - Changed `BOOLEAN DEFAULT 0` → `BOOLEAN DEFAULT FALSE`
  - Updated foreign key syntax for PostgreSQL
- **Query Syntax:**
  - Replaced all `?` placeholders with `%s` (PostgreSQL parameter style)
  - Added `RETURNING id` clause instead of using `cursor.lastrowid`
  - Added `RealDictCursor` to all database connections for dict-based row access
  - Converted timestamps to strings for JSON serialization

### 3. Created Setup Documentation
- `POSTGRESQL_SETUP.md`: Complete setup guide for local and Render deployment
- `.env.example`: Template for environment variables

## What to Do Next

### For Local Development:

1. **Install PostgreSQL** (if not already installed)
   ```powershell
   # Download from https://www.postgresql.org/download/windows/
   ```

2. **Create Database**
   ```powershell
   psql -U postgres
   CREATE DATABASE candidates_db;
   \q
   ```

3. **Install Dependencies**
   ```powershell
   cd task_backend
   pip install -r requirements.txt
   ```

4. **Set Environment Variable (if needed)**
   ```powershell
   $env:DATABASE_URL="postgresql://postgres:your_password@localhost:5432/candidates_db"
   ```

5. **Run the App**
   ```powershell
   python app.py
   ```

### For Render Deployment:

1. **Create PostgreSQL Database on Render**
   - Dashboard → New + → PostgreSQL
   - Copy the Internal Database URL

2. **Update Web Service Environment Variable**
   - Add `DATABASE_URL` with the PostgreSQL connection string

3. **Redeploy**
   - Render will automatically redeploy and create tables

## Key Differences: SQLite vs PostgreSQL

| Feature | SQLite | PostgreSQL |
|---------|--------|-----------|
| Auto Increment | `INTEGER PRIMARY KEY AUTOINCREMENT` | `SERIAL PRIMARY KEY` |
| Parameters | `?` | `%s` |
| Boolean | `0`/`1` | `FALSE`/`TRUE` |
| Row Factory | `sqlite3.Row` | `RealDictCursor` |
| Get Last ID | `cursor.lastrowid` | `RETURNING id` |
| File Storage | Single `.db` file | Client-server database |
| Persistence | Lost on Render restarts | Persists across restarts |

## Benefits of PostgreSQL

✅ **Persistent Storage:** Data survives Render service restarts
✅ **Production Ready:** Better for multi-user applications
✅ **Scalability:** Can handle more concurrent connections
✅ **ACID Compliance:** Stronger data integrity guarantees
✅ **Free Tier:** Render offers free PostgreSQL databases

## Notes

- The code now automatically detects if `DATABASE_URL` starts with `postgres://` and converts it to `postgresql://` (Render compatibility)
- Default local connection: `postgresql://postgres:postgres@localhost:5432/candidates_db`
- All timestamps are converted to strings for JSON serialization
- Tables are created automatically on first run via `init_db()`
