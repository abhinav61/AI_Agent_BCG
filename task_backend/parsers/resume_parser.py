import re
import os
from PyPDF2 import PdfReader
from docx import Document

class ResumeParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = self._extract_text()
    
    def _extract_text(self):
        """Extract text from PDF or DOCX file"""
        file_extension = os.path.splitext(self.file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self._extract_from_pdf()
        elif file_extension in ['.doc', '.docx']:
            return self._extract_from_docx()
        else:
            return ""
    
    def _extract_from_pdf(self):
        """Extract text from PDF"""
        try:
            reader = PdfReader(self.file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    
    def _extract_from_docx(self):
        """Extract text from DOCX"""
        try:
            doc = Document(self.file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return ""
    
    def extract_name(self):
        """Extract candidate name from resume"""
        lines = self.text.split('\n')
        # Usually name is in the first few lines
        for line in lines[:5]:
            line = line.strip()
            # Name is typically a short line with capital letters
            if len(line.split()) <= 4 and len(line) > 3 and not '@' in line:
                if re.match(r'^[A-Z][a-z]+(\s[A-Z][a-z]+)+', line):
                    return line
        return "Unknown"
    
    def extract_email(self):
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.text)
        return emails[0] if emails else None
    
    def extract_phone(self):
        """Extract phone number"""
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+?\d{10,}',
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, self.text)
            if phones:
                return phones[0].strip()
        return None
    
    def extract_skills(self):
        """Extract skills from resume"""
        common_skills = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'Ruby', 'PHP', 'Swift',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'SQLite',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins',
            'Git', 'GitHub', 'GitLab', 'Agile', 'Scrum', 'DevOps',
            'Machine Learning', 'AI', 'Deep Learning', 'Data Science',
            'HTML', 'CSS', 'REST API', 'GraphQL', 'Microservices',
            'Linux', 'Windows', 'MacOS', 'CI/CD', 'Testing', 'TDD'
        ]
        
        found_skills = []
        text_lower = self.text.lower()
        
        for skill in common_skills:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills[:10]  # Return top 10 skills
    
    def extract_experience(self):
        """Extract years of experience"""
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience',
            r'experience[:\s]+(\d+)\+?\s*(?:years?|yrs?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.text, re.IGNORECASE)
            if match:
                return f"{match.group(1)} years"
        
        return None
    
    def extract_education(self):
        """Extract education information"""
        degree_keywords = [
            'Bachelor', 'Master', 'PhD', 'B.Tech', 'M.Tech', 'B.E', 'M.E',
            'B.S', 'M.S', 'MBA', 'BBA', 'MCA', 'BCA', 'B.Sc', 'M.Sc'
        ]
        
        degree = None
        university = None
        
        lines = self.text.split('\n')
        for i, line in enumerate(lines):
            for degree_keyword in degree_keywords:
                if degree_keyword.lower() in line.lower():
                    degree = line.strip()
                    # Check next few lines for university
                    for j in range(i+1, min(i+4, len(lines))):
                        if len(lines[j].strip()) > 5 and 'university' in lines[j].lower():
                            university = lines[j].strip()
                            break
                    break
            if degree:
                break
        
        return degree, university
    
    def extract_company(self):
        """Extract current/recent company from Work Experience section"""
        # Find Work Experience section
        experience_patterns = [
            r'(?:WORK EXPERIENCE|Work Experience|PROFESSIONAL EXPERIENCE|Professional Experience|EMPLOYMENT|Employment|EXPERIENCE|Experience)[:\s]*\n([\s\S]*?)(?=\n(?:EDUCATION|Education|SKILLS|Skills|PROJECTS|Projects|CERTIFICATIONS|Certifications)|$)',
        ]

        experience_section = None
        for pattern in experience_patterns:
            match = re.search(pattern, self.text, re.IGNORECASE | re.MULTILINE)
            if match:
                experience_section = match.group(1)
                break

        if not experience_section:
            return None  # No Work Experience section found

        # Split the section into lines
        lines = experience_section.split('\n')

        # Look for the first company name
        for i, line in enumerate(lines):
            line = line.strip()

            # Skip empty lines and bullet points
            if not line or line.startswith('•'):
                continue

            # Check if the line looks like a company name
            if re.match(r'^[A-Z][A-Za-z0-9\s&,.\-]+$', line):
                # Ensure the next line contains a designation and the following line contains a date range
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if re.match(r'^[A-Z][A-Za-z\s]+$', next_line):
                        if i + 2 < len(lines):
                            date_line = lines[i + 2].strip()
                            if re.search(r'\b(?:\d{4}|Present)\b', date_line):
                                return line  # Return the company name

        return None
    
    def extract_designation(self):
        """Extract job title/designation from Work Experience section"""
        # Find Work Experience or Professional Experience section
        experience_patterns = [
            r'(?:WORK EXPERIENCE|Work Experience|PROFESSIONAL EXPERIENCE|Professional Experience|EMPLOYMENT|Employment|EXPERIENCE|Experience)[:\s]*\n([\s\S]*?)(?=\n(?:EDUCATION|Education|SKILLS|Skills|PROJECTS|Projects|CERTIFICATIONS|Certifications)|$)',
        ]
        
        experience_section = None
        for pattern in experience_patterns:
            match = re.search(pattern, self.text, re.IGNORECASE | re.MULTILINE)
            if match:
                experience_section = match.group(1)
                break
        
        if not experience_section:
            experience_section = self.text  # Fallback to full text
        
        title_keywords = [
            'Engineer', 'Developer', 'Manager', 'Analyst', 'Consultant',
            'Designer', 'Architect', 'Lead', 'Senior', 'Junior', 'Director',
            'Specialist', 'Coordinator', 'Administrator', 'Executive', 'AI',
            'Software', 'Data', 'Product', 'Project', 'Technical', 'Business'
        ]
        
        lines = experience_section.split('\n')
        for line in lines[:15]:  # Check first 15 lines of experience section
            line_lower = line.lower()
            for keyword in title_keywords:
                if keyword.lower() in line_lower and len(line.strip()) < 100:
                    # Clean up the designation
                    designation = line.strip()
                    if designation and '@' not in designation and len(designation) > 3:
                        # Make sure it's not a company name or other section
                        if not designation.isupper() or len(designation.split()) <= 4:
                            return designation
        
        return None
    
    def extract_location(self):
        """Extract location"""
        location_pattern = r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*),\s*([A-Z]{2})'
        match = re.search(location_pattern, self.text)
        if match:
            return f"{match.group(1)}, {match.group(2)}"
        return None
    
    def calculate_confidence(self, field_name, value):
        """Calculate confidence score for extracted field based on validation rules"""
        if value is None or value == "Unknown" or value == "":
            return 0.0
        
        # Name: If found and valid, score = 100
        if field_name == 'name':
            if value and value != "Unknown" and len(value) > 3:
                return 1.0  # 100%
            return 0.0
        
        # Email: Check for @ and valid domains (gmail, yahoo, outlook, hotmail)
        elif field_name == 'email':
            value_str = str(value).lower()
            if '@' in value_str:
                valid_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
                if any(domain in value_str for domain in valid_domains):
                    return 1.0  # 100%
                else:
                    return 0.85  # Valid email but not common domain
            return 0.0
        
        # Phone: Check for 10 or 12 digits with country code (+) or starting with 0
        elif field_name == 'phone':
            phone_str = str(value)
            digits = re.sub(r'\D', '', phone_str)  # Extract only digits
            
            # Pattern 1: +XX XXXXXXXXXX (country code + 10 digits) = 12 digits total
            # Pattern 2: 0XXXXXXXXXX (0 + 10 digits) = 11 digits total
            # Pattern 3: XXXXXXXXXX (10 digits)
            
            if phone_str.startswith('+'):
                # Country code format: should have 11-13 digits total
                if 11 <= len(digits) <= 13:
                    return 1.0  # 100%
            elif phone_str.startswith('0'):
                # Starting with 0: should have 11 digits (0 + 10)
                if len(digits) == 11:
                    return 1.0  # 100%
            elif len(digits) == 10:
                # Plain 10 digit number
                return 1.0  # 100%
            
            return 0.5  # Phone found but doesn't match expected format
        
        # Skills: Check compatibility with common_skills list
        elif field_name == 'skills':
            if isinstance(value, list) and len(value) > 0:
                common_skills = [
                    'Python', 'Java', 'JavaScript', 'C++', 'C#', 'Ruby', 'PHP', 'Swift',
                    'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring',
                    'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'SQLite',
                    'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins',
                    'Git', 'GitHub', 'GitLab', 'Agile', 'Scrum', 'DevOps',
                    'Machine Learning', 'AI', 'Deep Learning', 'Data Science',
                    'HTML', 'CSS', 'REST API', 'GraphQL', 'Microservices',
                    'Linux', 'Windows', 'MacOS', 'CI/CD', 'Testing', 'TDD'
                ]
                # Check how many skills match common_skills
                matched_skills = [s for s in value if s in common_skills]
                if len(matched_skills) > 0:
                    match_ratio = len(matched_skills) / len(value)
                    if match_ratio >= 0.8:  # 80% or more match
                        return 1.0  # 100%
                    else:
                        return match_ratio  # Proportional score
            return 0.0
        
        # Degree: Check compatibility with degree_keywords
        elif field_name == 'degree':
            if value:
                degree_keywords = [
                    'Bachelor', 'Master', 'PhD', 'B.Tech', 'M.Tech', 'B.E', 'M.E',
                    'B.S', 'M.S', 'MBA', 'BBA', 'MCA', 'BCA', 'B.Sc', 'M.Sc'
                ]
                value_str = str(value)
                # Check if any degree keyword is in the value
                if any(keyword.lower() in value_str.lower() for keyword in degree_keywords):
                    return 1.0  # 100%
                else:
                    return 0.6  # Degree found but not in standard format
            return 0.0
        
        # Default scores for other fields
        elif field_name == 'company':
            return 0.75 if value else 0.0
        elif field_name == 'designation':
            return 0.80 if value else 0.0
        elif field_name == 'location':
            return 0.70 if value else 0.0
        elif field_name == 'experience':
            return 0.75 if value else 0.0
        elif field_name == 'university':
            return 0.85 if value else 0.0
        
        return 0.5
    
    def extract_data(self):
        """Extract all data from resume"""
        name = self.extract_name()
        email = self.extract_email()
        phone = self.extract_phone()
        skills = self.extract_skills()
        experience = self.extract_experience()
        degree, university = self.extract_education()
        company = self.extract_company()
        designation = self.extract_designation()
        location = self.extract_location()
        
        data = {
            'name': name,
            'email': email,
            'phone': phone,
            'company': company,
            'designation': designation,
            'location': location,
            'experience': experience,
            'skills': skills,
            'degree': degree,
            'university': university,
            'confidence': {
                'fullName': self.calculate_confidence('name', name),
                'email': self.calculate_confidence('email', email),
                'phone': self.calculate_confidence('phone', phone),
                'company': self.calculate_confidence('company', company),
                'position': self.calculate_confidence('designation', designation),
                'location': self.calculate_confidence('location', location),
                'experience': self.calculate_confidence('experience', experience),
                'skills': self.calculate_confidence('skills', skills),
                'degree': self.calculate_confidence('degree', degree),
                'university': self.calculate_confidence('university', university)
            }
        }
        
        return data
