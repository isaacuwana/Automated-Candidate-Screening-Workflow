# Automated Candidate Screening Workflow - Walkthrough

## Overview

This automated candidate screening workflow is a comprehensive Python-based solution that handles the entire process of receiving job applications via email, screening candidates based on keywords, updating Google Sheets, and sending appropriate responses to candidates.

### High-Level Architecture

The workflow consists of several key components:

1. **Email Processing Service** - Monitors and processes incoming emails
2. **Keyword Screening Engine** - Analyzes email content for required keywords
3. **Google Sheets Integration** - Updates candidate tracking spreadsheets
4. **Email Communication System** - Sends personalized responses to candidates
5. **Workflow Orchestrator** - Coordinates all components and manages the process flow

## Workflow Design

### Process Flow

```
Incoming Email → Email Processing → Keyword Screening → Google Sheets Update → Candidate Response
```

#### Detailed Steps:

1. **Email Monitoring**: The system continuously monitors a designated email address for new applications
2. **Email Parsing**: Extracts candidate information, email content, and attachments
3. **Keyword Analysis**: Searches for required keywords ("Mid-level", "Python", "GenAI") in email content
4. **Screening Decision**: Determines if candidate is a "match" (≥2 keywords) or "not a match"
5. **Data Storage**: Adds candidate information to appropriate Google Sheets tab
6. **Response Generation**: Creates personalized email responses using templates
7. **Communication**: Sends acceptance or rejection emails to candidates

### Key Features

- **Flexible Keyword Matching**: Supports variations and synonyms of required keywords
- **Resume Handling**: Automatically saves resume attachments with organized naming
- **Duplicate Prevention**: Checks for existing candidates to avoid duplicates
- **Error Handling**: Comprehensive error handling with notifications to HR team
- **Logging**: Detailed logging for monitoring and debugging
- **Template System**: Professional email templates with personalization
- **Statistics Tracking**: Monitors workflow performance and success rates

## Prerequisites

### 1. Email Configuration

**Gmail Setup (Recommended):**
- Enable 2-Factor Authentication on your Gmail account
- Generate an App Password for the application
- Use IMAP settings: `imap.gmail.com:993` (SSL)
- Use SMTP settings: `smtp.gmail.com:587` (TLS)

**Required Email Permissions:**
- IMAP access enabled
- Less secure app access or App Password configured

### 2. Google Sheets API Setup

**Steps to Configure:**

1. **Create Google Cloud Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable Google Sheets API and Google Drive API

2. **Create Service Account:**
   - Navigate to "IAM & Admin" → "Service Accounts"
   - Create a new service account
   - Download the JSON credentials file
   - Rename it to `credentials.json` and place in project root

3. **Create Google Spreadsheet:**
   - Create a new Google Spreadsheet
   - Share it with the service account email (found in credentials.json)
   - Give "Editor" permissions
   - Copy the spreadsheet ID from the URL

### 3. Environment Configuration

1. **Copy Environment File:**
   ```bash
   cp .env.example .env
   ```

2. **Configure Variables:**
   ```env
   # Email Configuration
   EMAIL_USERNAME=careers-new-applicants@yourcompany.com
   EMAIL_PASSWORD=your_app_password_here
   
   # Google Sheets Configuration
   CANDIDATE_TRACKER_SHEET_ID=your_google_sheet_id_here
   
   # Scheduling Configuration
   CALENDLY_LINK=https://calendly.com/your-link
   
   # Company Information
   COMPANY_NAME=Seismic Consulting Group
   HR_EMAIL=hr@seismicgroup.com
   ```

### 4. Python Environment

**Requirements:**
- Python 3.8 or higher
- Virtual environment (recommended)

**Installation:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Installation & Setup

### 1. Clone and Setup Project

```bash
# Navigate to project directory
cd Task1_Isaac_Adeyeye

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs resumes
```

### 2. Configuration Files

Ensure these files are properly configured:
- `.env` - Environment variables
- `credentials.json` - Google Sheets API credentials

### 3. Test Connections

```bash
# Test the workflow connections
python main.py test
```

## Usage

### Running the Workflow

**Continuous Mode (Production):**
```bash
python main.py run
```

**Single Cycle (Testing):**
```bash
python main.py single
```

**View Status:**
```bash
python main.py status
```

**Test with Sample Data:**
```bash
python main.py test
```

### Command Line Options

```bash
python main.py --help
```

Available commands:
- `run` - Run continuous workflow
- `single` - Run single processing cycle
- `test` - Test with sample data
- `status` - Show current statistics

## Assumptions Made

### Email Format Assumptions
- **Resume Attachment**: Assumes resume is attached as PDF, DOC, DOCX, or TXT file
- **Sender Information**: Extracts candidate name from email headers or email body
- **Email Structure**: Assumes standard email format with proper headers

### Keyword Matching Assumptions
- **Case Insensitive**: All keyword matching is case-insensitive
- **Flexible Matching**: Includes variations and synonyms (e.g., "GenAI" matches "Generative AI")
- **Content Location**: Searches both email subject and body for keywords

### Google Sheets Assumptions
- **Sheet Structure**: Creates predefined column headers automatically
- **Permissions**: Service account has edit access to the spreadsheet
- **Sheet Names**: Uses configurable sheet names for different candidate types

### Communication Assumptions
- **Email Delivery**: Assumes SMTP server is accessible and configured correctly
- **Template Variables**: Uses predefined template variables for personalization
- **Response Timing**: Sends responses immediately after processing

## Potential Improvements & Edge Cases

### Current Limitations

1. **No Attachment Validation**: Doesn't verify if attachment is actually a resume
2. **Limited File Formats**: Only handles common resume formats (PDF, DOC, DOCX, TXT)
3. **Single Email Account**: Monitors only one email address
4. **No Duplicate Resume Detection**: Doesn't check for duplicate resume content
5. **Basic Name Extraction**: Name extraction could be more sophisticated

### Edge Cases Not Handled

1. **No Attachment Scenario**: 
   - Current: Processes application without resume
   - Improvement: Could require resume attachment or send follow-up request

2. **Multiple Attachments**:
   - Current: Saves first resume-like attachment
   - Improvement: Could save all attachments or ask candidate to specify

3. **Malformed Emails**:
   - Current: Basic error handling and logging
   - Improvement: More sophisticated email parsing and recovery

4. **API Rate Limits**:
   - Current: No rate limiting implemented
   - Improvement: Add rate limiting for Google Sheets and email APIs

5. **Large Volume Handling**:
   - Current: Processes emails sequentially
   - Improvement: Could implement parallel processing for high volumes

### Suggested Enhancements

#### Short-term Improvements
1. **Resume Content Analysis**: Use OCR or text extraction to analyze resume content
2. **Advanced Name Extraction**: Implement NLP-based name extraction
3. **Email Templates Management**: Web interface for managing email templates
4. **Monitoring Dashboard**: Real-time dashboard for workflow monitoring

#### Long-term Enhancements
1. **Machine Learning Integration**: Use ML for better candidate screening
2. **Multi-language Support**: Handle applications in different languages
3. **Integration with ATS**: Connect with Applicant Tracking Systems
4. **Video/Portfolio Analysis**: Handle video resumes or portfolio links
5. **Automated Interview Scheduling**: Direct integration with calendar systems

### Error Recovery Scenarios

1. **Google Sheets Unavailable**: 
   - Queues candidates for later processing
   - Sends notification to HR team

2. **Email Server Issues**:
   - Implements retry logic with exponential backoff
   - Maintains processing queue

3. **Credential Expiration**:
   - Detects authentication failures
   - Sends alerts to administrators

## Monitoring & Maintenance

### Logging
- **Location**: `logs/candidate_screening.log`
- **Rotation**: 10MB files, 30-day retention
- **Compression**: Automatic ZIP compression of old logs

### Statistics Tracking
- Total applications processed
- Match/rejection rates
- Email delivery success rates
- Error frequencies and types

### Regular Maintenance Tasks
1. **Log Review**: Weekly review of error logs
2. **Credential Rotation**: Quarterly password/key updates
3. **Template Updates**: Regular review of email templates
4. **Performance Monitoring**: Monthly performance analysis

## Security Considerations

### Data Protection
- **Credentials**: Stored in environment variables, not in code
- **Resume Files**: Stored locally with restricted access
- **Email Content**: Logged without sensitive information
- **API Keys**: Rotated regularly

### Access Control
- **Service Account**: Minimal required permissions
- **Email Account**: Dedicated account for applications only
- **File System**: Restricted access to resume storage directory

## Support & Troubleshooting

### Common Issues

1. **Authentication Errors**: Check credentials and API access
2. **Email Connection Issues**: Verify IMAP/SMTP settings
3. **Google Sheets Errors**: Confirm service account permissions
4. **Missing Dependencies**: Run `pip install -r requirements.txt`

### Debug Mode
```bash
python main.py run --log-level DEBUG
```

### Contact Information
For technical support or questions about this workflow, contact the development team at the email specified in the configuration.

---

This walkthrough provides comprehensive guidance for setting up, running, and maintaining the automated candidate screening workflow. The system is designed to be robust, scalable, and maintainable while handling the core requirements of the hiring process automation.