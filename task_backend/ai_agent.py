import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# LangChain imports - Fixed imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

class AIDocumentAgent:
    def __init__(self):
        # OpenRouter API configuration
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        
        # Initialize LangChain ChatOpenAI with OpenRouter
        self.llm = ChatOpenAI(
            model="meta-llama/llama-3.1-8b-instruct:free",
            openai_api_key=self.api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.7,
            max_tokens=800,
            model_kwargs={
                "headers": {
                    "HTTP-Referer": os.getenv('FRONTEND_URL', 'https://ai-agent-bcg-1-front.onrender.com'),
                    "X-Title": "TraqCheck HR System"
                }
            }
        )
        
        # Email configuration from .env
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        
        # Create LangChain prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a professional HR assistant who writes clear, friendly, and personalized emails."),
            ("human", """Generate a professional and friendly email requesting identity documents from a candidate.

Candidate Details:
- Name: {name}
- Position Applied: {designation}
- Company: {company}
- Upload Link: {upload_link}

Requirements:
1. Request PAN Card (10 alphanumeric) and Aadhaar Card (12 digits) documents
2. Be professional yet warm
3. Explain why we need these documents (verification, onboarding)
4. Prominently mention they should click the upload link to submit documents
5. Include a deadline (7 days from now)
6. Keep it concise (150-200 words)
7. Make the upload link stand out

Generate only the email body, no subject line.""")
        ])
    
    def generate_document_request_email(self, candidate_data):
        """Use LangChain to generate a personalized document request email"""
        
        try:
            print(f"Generating email using LangChain for {candidate_data.get('name')}...")
            
            # Create upload link
            candidate_id = candidate_data.get('id')
            upload_link = f"https://ai-agent-bcg-1-flask.onrender.com/upload-documents/{candidate_id}"
            
            # Use LangChain to generate email with prompt template
            messages = self.prompt_template.format_messages(
                name=candidate_data.get('name', 'Candidate'),
                designation=candidate_data.get('designation', 'the position'),
                company=candidate_data.get('company', 'our company'),
                upload_link=upload_link
            )
            
            response = self.llm.invoke(messages)
            email_body = response.content
            print(f"AI generated email successfully using LangChain")
            
            return email_body
            
        except Exception as e:
            print(f"Error generating email with LangChain: {e}")
            # Fallback to template if AI fails
            return self._get_fallback_template(candidate_data)
    
    def generate_with_messages(self, candidate_data):
        """Alternative method using LangChain messages directly"""
        try:
            messages = [
                SystemMessage(content="You are a professional HR assistant who writes clear, friendly emails."),
                HumanMessage(content=f"""Generate a professional email requesting documents from:
                
Name: {candidate_data.get('name', 'Candidate')}
Position: {candidate_data.get('designation', 'the position')}
Company: {candidate_data.get('company', 'our company')}

Request PAN Card and Aadhaar Card. Be professional, explain verification needs, 7 day deadline, 150-200 words.""")
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            print(f"Error with messages approach: {e}")
            return self._get_fallback_template(candidate_data)
    
    def _get_fallback_template(self, candidate_data):
        """Fallback email template if AI generation fails"""
        name = candidate_data.get('name', 'Candidate')
        position = candidate_data.get('designation', 'the position')
        candidate_id = candidate_data.get('id')
        upload_link = f"https://ai-agent-bcg-1-flask.onrender.com/upload-documents/{candidate_id}"
        
        return f"""Dear {name},

Thank you for your interest in {position}. To proceed with your application, we need to verify your identity documents.

Please upload the following documents within 7 days:
1. PAN Card (10 alphanumeric characters - clear photo or scanned copy)
2. Aadhaar Card (12 digits - both front and back)

📎 UPLOAD YOUR DOCUMENTS HERE:
<a href=\"{upload_link}\" style=\"color: blue; text-decoration: underline;\">click</a>

Click the link above to access our secure upload portal. The system will automatically verify your documents.

Requirements:
• Clear, readable images (JPG, PNG) or PDF format
• File size: Maximum 10MB per document
• Ensure all text is clearly visible

These documents are required for verification and onboarding purposes. All information will be kept confidential and secure.

If you have any questions, please don't hesitate to contact us.

Best regards,
HR Team
TraqCheck"""
    
    def send_email(self, recipient_email, subject, body, candidate_name="Candidate"):
        """Send email using SMTP"""
        try:
            print(f"\nPreparing to send email...")
            print(f"From: {self.sender_email}")
            print(f"To: {recipient_email}")
            print(f"Subject: {subject}")
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Add HTML version
            html_body = f"""
            <html>
              <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                  {body.replace(chr(10), '<br>')}
                  <br><br>
                  <hr style="border: 1px solid #eee;">
                  <p style="font-size: 12px; color: #666;">
                    This is an automated email from TraqCheck System.<br>
                    Please do not reply to this email.
                  </p>
                </div>
              </body>
            </html>
            """
            
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
            
            # Send email
            print(f"Connecting to {self.smtp_server}:{self.smtp_port}...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                print(f"Starting TLS...")
                server.starttls()
                print(f"Logging in...")
                server.login(self.sender_email, self.sender_password)
                print(f"Sending email...")
                server.send_message(message)
            
            print(f"Email sent successfully from {self.sender_email} to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def request_documents(self, candidate_data):
        """Main method to generate and send document request using LangChain"""
        
        print(f"\n{'='*60}")
        print(f"AI Agent Processing Document Request")
        print(f"{'='*60}")
        print(f"Candidate Data: {candidate_data}")
        
        # Generate personalized email using LangChain
        email_body = self.generate_document_request_email(candidate_data)
        
        # Create subject
        subject = f"Document Request - {candidate_data.get('name', 'Candidate')} | TraqCheck"
        
        # Send email (if email credentials are configured)
        recipient_email = candidate_data.get('email')
        print(f"Recipient Email: {recipient_email}")
        
        if not recipient_email:
            return {
                'success': False,
                'message': 'No email address found for candidate',
                'email_body': email_body
            }
        
        # Check if email credentials are configured
        print(f"Sender Email: {self.sender_email}")
        print(f"Password Configured: {'Yes' if self.sender_password else 'No'}")
        
        if not self.sender_email or not self.sender_password:
            print("Warning: Email credentials not configured. Cannot send email.")
            return {
                'success': False,
                'message': 'Email credentials not configured. Please add SENDER_PASSWORD to .env file',
                'email_body': email_body
            }
        
        success = self.send_email(
            recipient_email=recipient_email,
            subject=subject,
            body=email_body,
            candidate_name=candidate_data.get('name', 'Candidate')
        )
        
        print(f"{'='*60}\n")
        
        return {
            'success': success,
            'message': 'Document request sent successfully' if success else 'Failed to send email',
            'email_body': email_body
        }