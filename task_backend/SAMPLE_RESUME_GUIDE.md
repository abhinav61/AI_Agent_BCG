# Sample Resume Format Guide

This is a reference CV format that the resume parser is designed to extract information from.

## Expected Extraction Results for sample_resume.txt:

**Name:** Abhinav Kumar  
**Email:** abhinav.kumar@gmail.com (Score: 100% - contains @ and gmail.com)  
**Phone:** +91 9876543210 (Score: 100% - has country code + and 10 digits)  
**Company:** Tech Mahindra (extracted from WORK EXPERIENCE section)  
**Designation:** AI Engineer (extracted from WORK EXPERIENCE section)  
**Location:** Mumbai, MH  

**Skills:** Python, Java, JavaScript, C++, TensorFlow, AWS, Azure, GCP, Docker, Kubernetes, Git, Jenkins, MySQL, MongoDB, PostgreSQL, React, Node.js, Flask, Django, CI/CD, Agile, Scrum  
**Skills Score:** 100% (all skills match common_skills list)

**Degree:** Bachelor of Technology in Computer Science  
**Degree Score:** 100% (contains "Bachelor" keyword)  
**University:** Indian Institute of Technology, Mumbai

## Key Resume Sections the Parser Looks For:

1. **Contact Information** (Top of resume)
   - Name (first 5 lines, capitalized format)
   - Email (contains @)
   - Phone (with + or 0, 10-12 digits)
   - Location (City, STATE format)

2. **WORK EXPERIENCE / PROFESSIONAL EXPERIENCE**
   - Company Name (first line after job entry)
   - Job Title/Designation (contains keywords like Engineer, Developer, Manager, etc.)
   - Dates (optional)

3. **EDUCATION**
   - Degree (Bachelor, Master, B.Tech, M.Tech, MBA, etc.)
   - University (line containing "university")

4. **SKILLS / TECHNICAL SKILLS**
   - Matches against predefined common_skills list
   - Programming languages, frameworks, tools, cloud platforms

## Tips for Resume Format:

✓ Use clear section headers: WORK EXPERIENCE, EDUCATION, SKILLS  
✓ List company name on a separate line  
✓ List job title below or next to company name  
✓ Use standard degree names (Bachelor, Master, B.Tech, etc.)  
✓ Include common email domains (gmail.com, yahoo.com, outlook.com, hotmail.com) for 100% confidence  
✓ Format phone as: +91 XXXXXXXXXX or 0XXXXXXXXXX or plain 10 digits  

## Confidence Score Criteria:

- **Name:** 100% if found and valid (length > 3)
- **Email:** 100% if contains @ AND (gmail/yahoo/outlook/hotmail), 85% for other valid emails
- **Phone:** 100% if matches format (+XX..., 0XXX..., or 10 digits)
- **Skills:** 100% if 80%+ skills match common_skills list
- **Degree:** 100% if contains standard degree keywords
- **Company:** 75% if found
- **Designation:** 80% if found
- **Location:** 70% if found
- **University:** 85% if found
