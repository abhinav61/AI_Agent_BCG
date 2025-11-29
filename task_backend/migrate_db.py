"""
Database migration script to add upload_attempts and documents_submitted columns
"""
import sqlite3

DATABASE = 'candidates.db'

def migrate():
    """Add new columns to candidates table"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(candidates)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add upload_attempts column if it doesn't exist
        if 'upload_attempts' not in columns:
            print("Adding upload_attempts column...")
            cursor.execute('''
                ALTER TABLE candidates 
                ADD COLUMN upload_attempts INTEGER DEFAULT 0
            ''')
            print("Added upload_attempts column")
        else:
            print("upload_attempts column already exists")
        
        # Add documents_submitted column if it doesn't exist
        if 'documents_submitted' not in columns:
            print("Adding documents_submitted column...")
            cursor.execute('''
                ALTER TABLE candidates 
                ADD COLUMN documents_submitted BOOLEAN DEFAULT 0
            ''')
            print("Added documents_submitted column")
        else:
            print("documents_submitted column already exists")
        
        conn.commit()
        print("\nDatabase migration completed successfully!")
        
    except Exception as e:
        print(f"Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    print("Starting database migration...")
    migrate()
