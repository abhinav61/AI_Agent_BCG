# import imaplib
# import email
# from email.header import decode_header
# import os
# import time
# import sqlite3
# import re
# from parsers.document_verifier import DocumentVerifier
# from datetime import datetime

# class EmailReceiver:
#     def __init__(self, email_address, password, imap_server='imap.gmail.com'):
#         """Initialize email receiver with credentials"""
#         self.email_address = email_address
#         self.password = password
#         self.imap_server = imap_server
#         self.doc_verifier = DocumentVerifier()
#         self.upload_folder = 'uploads'
#         self.database = 'candidates.db'
    
#     def get_db_connection(self):
#         """Get database connection"""
#         conn = sqlite3.connect(self.database)
#         conn.row_factory = sqlite3.Row
#         return conn
    
#     def connect(self):
#         """Connect to email inbox"""
#         try:
#             print(f"Connecting to {self.imap_server}...")
#             self.mail = imaplib.IMAP4_SSL(self.imap_server)
#             self.mail.login(self.email_address, self.password)
#             print(f"Successfully connected to {self.email_address}")
#             return True
#         except Exception as e:
#             print(f"Failed to connect: {e}")
#             return False
    
#     def find_candidate_by_email(self, sender_email):
#         """Find candidate in database by email address"""
#         conn = self.get_db_connection()
#         cursor = conn.cursor()
        
#         cursor.execute('SELECT * FROM candidates WHERE email = ?', (sender_email,))
#         candidate = cursor.fetchone()
        
#         conn.close()
#         return dict(candidate) if candidate else None
    
#     def save_attachment(self, part, candidate_id, candidate_name):
#         """Save email attachment to candidate's folder"""
#         filename = part.get_filename()
#         if filename:
#             # Decode filename if needed
#             if decode_header(filename)[0][1] is not None:
#                 filename = decode_header(filename)[0][0].decode(decode_header(filename)[0][1])
            
#             # Create candidate folder
#             safe_name = re.sub(r'[^\w\s-]', '', candidate_name).strip().replace(' ', '_')
#             folder_name = f"{candidate_id}_{safe_name}"
#             docs_dir = os.path.join(self.upload_folder, 'documents', folder_name)
#             os.makedirs(docs_dir, exist_ok=True)
            
#             # Save file
#             filepath = os.path.join(docs_dir, filename)
#             with open(filepath, 'wb') as f:
#                 f.write(part.get_payload(decode=True))
            
#             print(f"Saved attachment: {filepath}")
#             return filepath, filename
#         return None, None
    
#     def detect_document_type(self, filename):
#         """Detect if attachment is PAN or Aadhaar"""
#         filename_lower = filename.lower()
#         if 'pan' in filename_lower:
#             return 'PAN Card'
#         elif 'aadhaar' in filename_lower or 'aadhar' in filename_lower:
#             return 'Aadhaar Card'
#         return None
    
#     def process_email(self, email_id):
#         """Process a single email and extract attachments"""
#         try:
#             # Fetch email
#             status, data = self.mail.fetch(email_id, '(RFC822)')
#             if status != 'OK':
#                 return
            
#             # Parse email
#             msg = email.message_from_bytes(data[0][1])
            
#             # Get sender email
#             sender = email.utils.parseaddr(msg['From'])[1]
            
#             # Find candidate first - skip if not a candidate
#             candidate = self.find_candidate_by_email(sender)
#             if not candidate:
#                 # Skip emails from non-candidates (don't print anything)
#                 return
            
#             # Only process and print details for candidate emails
#             subject = decode_header(msg['Subject'])[0][0]
#             if isinstance(subject, bytes):
#                 subject = subject.decode()
            
#             print(f"\n{'='*60}")
#             print(f"✅ Incoming mail from candidate: {sender}")
#             print(f"👤 Candidate: {candidate['name']} (ID: {candidate['id']})")
#             print(f"📋 Subject: {subject}")
#             print(f"{'='*60}")
            
#             # Check if candidate has pending document request
#             conn = self.get_db_connection()
#             cursor = conn.cursor()
#             cursor.execute('''
#                 SELECT * FROM document_requests 
#                 WHERE candidate_id = ? AND status = 'sent'
#                 ORDER BY request_date DESC LIMIT 1
#             ''', (candidate['id'],))
#             doc_request = cursor.fetchone()
            
#             if not doc_request:
#                 print(f"No pending document request for this candidate")
#                 conn.close()
#                 return
            
#             # Process attachments
#             attachments_saved = []
#             documents_uploaded = []
            
#             if msg.is_multipart():
#                 for part in msg.walk():
#                     content_type = part.get_content_type()
#                     content_disposition = str(part.get("Content-Disposition"))
                    
#                     # Check if it's an attachment
#                     if "attachment" in content_disposition:
#                         filepath, filename = self.save_attachment(part, candidate['id'], candidate['name'])
#                         if filepath:
#                             attachments_saved.append((filepath, filename))
            
#             if not attachments_saved:
#                 print(f"No attachments found in email")
#                 conn.close()
#                 return
            
#             print(f"Found {len(attachments_saved)} attachment(s)")
            
#             # Process each attachment
#             processed_types = set()
#             for filepath, filename in attachments_saved:
#                 # Detect document type
#                 doc_type = self.detect_document_type(filename)
                
#                 # Auto-assign if not detected
#                 if not doc_type:
#                     if 'PAN Card' not in processed_types:
#                         doc_type = 'PAN Card'
#                     elif 'Aadhaar Card' not in processed_types:
#                         doc_type = 'Aadhaar Card'
#                     else:
#                         continue
                
#                 print(f"Processing {doc_type}: {filename}")
                
#                 # No verification - just mark as uploaded
#                 verification_result = {
#                     'status': 'Pass',
#                     'extracted_name': 'Not verified',
#                     'similarity_score': None,
#                     'reason': 'Document uploaded successfully (no validation)'
#                 }
                
#                 # # Commented out: Original verification logic
#                 # # Verify document using OCR
#                 # try:
#                 #     verification_result = self.doc_verifier.verify_document(
#                 #         filepath,
#                 #         doc_type,
#                 #         candidate['name'],
#                 #         threshold=0.6
#                 #     )
#                 # except Exception as e:
#                 #     print(f"❌ Verification error: {e}")
#                 #     verification_result = {
#                 #         'status': 'Verification Failed',
#                 #         'extracted_name': None,
#                 #         'similarity_score': 0.0,
#                 #         'reason': f'Verification error: {str(e)}',
#                 #         'document_number': None,
#                 #         'number_valid': False
#                 #     }
                
#                 # Store in database
#                 cursor.execute('''
#                     INSERT INTO submitted_documents 
#                     (candidate_id, document_type, file_path, verification_status, 
#                      extracted_name, similarity_score, verification_reason)
#                     VALUES (?, ?, ?, ?, ?, ?, ?)
#                 ''', (
#                     candidate['id'],
#                     doc_type,
#                     filepath,
#                     verification_result['status'],
#                     verification_result.get('extracted_name'),
#                     verification_result.get('similarity_score'),
#                     verification_result.get('reason')
#                 ))
                
#                 documents_uploaded.append({
#                     'type': doc_type,
#                     'status': verification_result['status'],
#                     'document_number': verification_result.get('document_number')
#                 })
                
#                 processed_types.add(doc_type)
#                 print(f"{'Pass' if verification_result['status'] == 'Pass' else 'Fail'} {doc_type}: {verification_result['status']}")
            
#             # Update candidate status - no validation, always completed
#             if documents_uploaded:
#                 extraction_status = 'Completed'
                
#                 # # Commented out: Original validation logic
#                 # all_passed = all(doc['status'] == 'Pass' for doc in documents_uploaded)
#                 # extraction_status = 'Completed' if all_passed else 'Verification Failed'
                
#                 cursor.execute('''
#                     UPDATE candidates 
#                     SET extraction_status = ?
#                     WHERE id = ?
#                 ''', (extraction_status, candidate['id']))
                
#                 # Update document request status
#                 cursor.execute('''
#                     UPDATE document_requests
#                     SET status = 'completed'
#                     WHERE id = ?
#                 ''', (doc_request['id'],))
                
#                 print(f"Updated candidate status to: {extraction_status}")
            
#             conn.commit()
#             conn.close()
            
#             print(f"Email processed successfully!")
#             print(f"{'='*60}\n")
            
#         except Exception as e:
#             print(f"Error processing email: {e}")
#             import traceback
#             traceback.print_exc()
    
#     def check_inbox(self):
#         """Check inbox for new emails with attachments"""
#         try:
#             # Select inbox
#             self.mail.select('INBOX')
            
#             # Search for unread emails
#             status, messages = self.mail.search(None, 'UNSEEN')
            
#             if status != 'OK':
#                 print("Failed to search inbox")
#                 return
            
#             email_ids = messages[0].split()
            
#             if not email_ids:
#                 print("No new emails")
#                 return
            
#             print(f"Found {len(email_ids)} new email(s)")
            
#             # Process each email
#             for email_id in email_ids:
#                 self.process_email(email_id)
            
#         except Exception as e:
#             print(f"Error checking inbox: {e}")
#             import traceback
#             traceback.print_exc()
    
#     def monitor(self, interval=60):
#         """Monitor inbox continuously"""
#         print(f"\n{'='*60}")
#         print(f"🔄 Starting Email Monitor")
#         print(f"{'='*60}")
#         print(f"📧 Monitoring: {self.email_address}")
#         print(f"⏱️  Check interval: {interval} seconds")
#         print(f"📋 Only showing emails from registered candidates")
#         print(f"{'='*60}\n")
        
#         if not self.connect():
#             return
        
#         try:
#             while True:
#                 print(f"Checking inbox at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
#                 self.check_inbox()
#                 print(f"Waiting {interval} seconds...\n")
#                 time.sleep(interval)
#         except KeyboardInterrupt:
#             print("\nStopping email monitor...")
#         finally:
#             self.mail.logout()
#             print("Disconnected from email server")

# if __name__ == '__main__':
#     # Email credentials (same as sending email)
#     EMAIL_ADDRESS = "abhinavk806@gmail.com"
#     EMAIL_PASSWORD = "rtnmgzboncpfxyge"  # App password
    
#     receiver = EmailReceiver(EMAIL_ADDRESS, EMAIL_PASSWORD)
#     receiver.monitor(interval=20)  # Check every 20 seconds
