# TraqCheck Backend

Flask backend for resume extraction and document management.

## Setup Instructions

### 1. Create and Activate Virtual Environment

```cmd
python -m venv env
env\Scripts\activate
```

### 2. Install Dependencies

```cmd
pip install -r requirements.txt
```

### 3. Run the Application

```cmd
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### POST /api/candidates/upload
Upload a resume (PDF/DOCX) for extraction
- **Body**: FormData with 'resume' file
- **Returns**: Extracted candidate data with ID

### GET /api/candidates
Get list of all candidates
- **Returns**: Array of candidate objects

### GET /api/candidates/<id>
Get detailed candidate profile
- **Returns**: Full candidate object with extracted data, skills, and confidence scores

### GET /api/health
Health check endpoint
- **Returns**: Server status

## Additional API Endpoints

#### POST `/api/candidates/upload`
- **Description**: Accepts a resume (PDF/DOCX) and extracts information.
- **Request Body**: FormData with 'resume' file.
- **Response**: Extracted candidate data with ID.

#### GET `/api/candidates`
- **Description**: Retrieves a list of all candidates.
- **Response**: Array of candidate objects.

#### GET `/api/candidates/<id>`
- **Description**: Retrieves detailed candidate profile.
- **Response**: Full candidate object with extracted data, skills, and confidence scores.

#### POST `/api/candidates/<id>/request-documents`
- **Description**: AI agent generates and sends personalized document requests.
- **Response**: Status of the request.

#### POST `/api/candidates/<id>/submit-documents`
- **Description**: Accepts uploaded PAN/Aadhaar documents with OCR verification.
- **Request Body**: FormData with document files.
- **Response**: Verification status and document details.

#### GET `/api/candidates/<id>/documents/debug`
- **Description**: Debug endpoint to check existing documents for a candidate.
- **Response**: List of documents and their details.

#### GET `/upload-documents/<id>`
- **Description**: Serves the document upload page for candidates.
- **Response**: HTML page for uploading documents.

## Database

- SQLite database: `candidates.db`
- Automatic initialization on first run
- Tables: candidates, candidate_skills, confidence_scores, documents

## File Structure

```
task_Backend/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── parsers/
│   ├── __init__.py
│   └── resume_parser.py   # Resume extraction logic
├── uploads/               # Uploaded resume files (created automatically)
└── candidates.db          # SQLite database (created automatically)
```

## Recent Updates

### Resume Parsing Enhancements
- Improved logic to extract the current company, designation, and work duration based on structured formats.
- Added support for identifying the current company when followed by a designation and date range.

### API Improvements
- Enhanced `/api/candidates/upload` endpoint to return more structured data, including detailed work experience.

### File Structure Updates
- Updated `resume_parser.py` to include robust regex checks for better accuracy in parsing resumes.
