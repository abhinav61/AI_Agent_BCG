import os
import re
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from difflib import SequenceMatcher

class DocumentVerifier:
    def __init__(self):
        # Set tesseract path (update this based on your installation)
        # For Windows, typically: C:\Program Files\Tesseract-OCR\tesseract.exe
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def extract_text_from_image(self, image_path):
        """Extract text from image using OCR"""
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img, lang='eng')
            return text
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return ""
    
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF by converting to images first"""
        try:
            images = convert_from_path(pdf_path)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img, lang='eng') + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_text_from_document(self, file_path):
        """Extract text based on file type"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext in ['.jpg', '.jpeg', '.png']:
            return self.extract_text_from_image(file_path)
        elif file_ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        else:
            return ""
    
    def extract_name_from_aadhaar(self, text):
        """Extract name from Aadhaar card text"""
        # Clean text
        text = text.strip()
        lines = text.split('\n')
        
        # Common patterns for Aadhaar cards
        # Look for lines after "Government of India" or before Aadhaar number
        name = None
        
        # Pattern 1: Look for name after certain keywords
        for i, line in enumerate(lines):
            line_clean = line.strip()
            
            # Skip common headers
            if any(keyword in line_clean.lower() for keyword in ['government', 'india', 'aadhaar', 'uid']):
                continue
            
            # Check if line contains Aadhaar number (12 digits)
            if re.search(r'\d{4}\s*\d{4}\s*\d{4}', line_clean):
                # Name is usually before the Aadhaar number
                if i > 0:
                    name = lines[i-1].strip()
                break
            
            # Check if line looks like a name (alphabets with possible spaces)
            if re.match(r'^[A-Za-z\s]{3,50}$', line_clean) and len(line_clean.split()) >= 2:
                if not name:
                    name = line_clean
        
        # Pattern 2: Look for name in first few meaningful lines
        if not name:
            for line in lines[:10]:
                line_clean = line.strip()
                if len(line_clean) > 5 and re.match(r'^[A-Za-z\s]{3,50}$', line_clean):
                    if len(line_clean.split()) >= 2:  # At least first and last name
                        name = line_clean
                        break
        
        return name.strip() if name else None
    
    def extract_name_from_pan(self, text):
        """Extract name from PAN card text"""
        text = text.strip()
        lines = text.split('\n')
        
        name = None
        
        # Look for PAN number pattern (5 letters, 4 digits, 1 letter)
        for i, line in enumerate(lines):
            line_clean = line.strip()
            
            # Skip headers
            if any(keyword in line_clean.lower() for keyword in ['income', 'tax', 'department', 'permanent', 'account']):
                continue
            
            # Check if line contains PAN number
            if re.search(r'[A-Z]{5}\d{4}[A-Z]', line_clean):
                # Name is usually above PAN number
                if i > 0:
                    # Look backwards for name
                    for j in range(i-1, max(0, i-4), -1):
                        potential_name = lines[j].strip()
                        if re.match(r'^[A-Za-z\s]{3,50}$', potential_name) and len(potential_name.split()) >= 2:
                            name = potential_name
                            break
                break
        
        # Fallback: Look for name patterns in first few lines
        if not name:
            for line in lines[:10]:
                line_clean = line.strip()
                if len(line_clean) > 5 and re.match(r'^[A-Za-z\s]{3,50}$', line_clean):
                    if len(line_clean.split()) >= 2:
                        name = line_clean
                        break
        
        return name.strip() if name else None
    
    def normalize_name(self, name):
        """Normalize name for comparison"""
        if not name:
            return ""
        # Convert to lowercase, remove extra spaces, remove special characters
        name = re.sub(r'[^a-zA-Z\s]', '', name)
        name = ' '.join(name.lower().split())
        return name
    
    def calculate_name_similarity(self, name1, name2):
        """Calculate similarity between two names (0-1)"""
        norm1 = self.normalize_name(name1)
        norm2 = self.normalize_name(name2)
        
        if not norm1 or not norm2:
            return 0.0
        
        # Use sequence matcher for fuzzy matching
        similarity = SequenceMatcher(None, norm1, norm2).ratio()
        
        # Also check if one name is contained in the other (partial match)
        words1 = set(norm1.split())
        words2 = set(norm2.split())
        
        # Calculate word overlap
        if words1 and words2:
            word_overlap = len(words1.intersection(words2)) / max(len(words1), len(words2))
            # Use higher of sequence similarity or word overlap
            similarity = max(similarity, word_overlap)
        
        return similarity
    
    def extract_aadhaar_number(self, text):
        """Extract 16-digit Aadhaar number from text"""
        # Remove all spaces and newlines
        clean_text = text.replace(' ', '').replace('\n', '').replace('\r', '')
        
        # Try to find 16 consecutive digits
        pattern = r'\b\d{16}\b'
        matches = re.findall(pattern, clean_text)
        
        if matches:
            return matches[0]
        
        # Alternative: Look for 12-digit Aadhaar and try to find 4 more digits nearby
        # Note: Standard Aadhaar is 12 digits, but user wants 16
        pattern_12 = r'\d{12}'
        matches_12 = re.findall(pattern_12, text.replace(' ', ''))
        
        # If we find 12-digit number, look for nearby 4-digit number
        for match in matches_12:
            # Try to find if there are 4 more digits adjacent
            extended_pattern = rf'{match}\d{{4}}'
            extended = re.search(extended_pattern, clean_text)
            if extended:
                return extended.group()
        
        return None
    
    def extract_pan_number(self, text):
        """Extract 10-character PAN number from text"""
        # PAN format: 5 letters, 4 digits, 1 letter (e.g., ABCDE1234F)
        pattern = r'\b[A-Z]{5}\d{4}[A-Z]\b'
        matches = re.findall(pattern, text)
        
        if matches:
            return matches[0]
        
        return None
    
    def validate_aadhaar_number(self, aadhaar_number):
        """Validate Aadhaar number format: 16 digits"""
        if not aadhaar_number:
            return False
        
        # Check length is 16
        if len(aadhaar_number) != 16:
            return False
        
        # Check all characters are digits
        if not aadhaar_number.isdigit():
            return False
        
        return True
    
    def validate_pan_number(self, pan_number):
        """Validate PAN number format: 10 alphanumeric (5 letters, 4 digits, 1 letter)"""
        if not pan_number:
            return False
        
        # Check length is 10
        if len(pan_number) != 10:
            return False
        
        # Check format: First 5 are letters
        if not pan_number[:5].isalpha() or not pan_number[:5].isupper():
            return False
        
        # Next 4 are digits
        if not pan_number[5:9].isdigit():
            return False
        
        # Last 1 is letter
        if not pan_number[9].isalpha() or not pan_number[9].isupper():
            return False
        
        return True
    
    def verify_document(self, file_path, document_type, candidate_name, threshold=0.7):
        """
        Verify document by extracting and matching name only
        
        Args:
            file_path: Path to the document file
            document_type: 'PAN Card' or 'Aadhaar Card'
            candidate_name: Expected name from candidate profile
            threshold: Minimum similarity score (0-1) for verification to pass
        
        Returns:
            dict with verification result
        """
        print(f"\n{'='*60}")
        print(f"Verifying {document_type}")
        print(f"{'='*60}")
        print(f"File: {file_path}")
        print(f"Expected Name: {candidate_name}")
        
        # Extract text from document
        text = self.extract_text_from_document(file_path)
        print(f"Extracted Text Length: {len(text)} characters")
        
        if not text or len(text) < 10:
            return {
                'verified': False,
                'status': 'Verification Failed',
                'reason': 'Unable to extract text from document',
                'extracted_name': None,
                'similarity_score': 0.0
            }
        
        # Extract name based on document type
        extracted_name = None
        
        if 'aadhaar' in document_type.lower():
            extracted_name = self.extract_name_from_aadhaar(text)
        elif 'pan' in document_type.lower():
            extracted_name = self.extract_name_from_pan(text)
        
        print(f"Extracted Name: {extracted_name}")
        
        if not extracted_name:
            return {
                'verified': False,
                'status': 'Verification Failed',
                'reason': 'Unable to extract name from document',
                'extracted_name': None,
                'similarity_score': 0.0
            }
        
        # Calculate similarity
        similarity = self.calculate_name_similarity(candidate_name, extracted_name)
        print(f"Name Similarity: {similarity:.2%}")
        print(f"Threshold: {threshold:.2%}")
        
        verified = similarity >= threshold
        
        result = {
            'verified': verified,
            'status': 'Pass' if verified else 'Verification Failed',
            'reason': f'Name match: {similarity:.2%}' if verified else f'Name mismatch (similarity: {similarity:.2%})',
            'extracted_name': extracted_name,
            'similarity_score': similarity
        }
        
        print(f"Result: {result['status']}")
        print(f"{'='*60}\n")
        
        return result
