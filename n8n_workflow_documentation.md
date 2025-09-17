# n8n Automated Candidate Screening Workflow

## Overview

This n8n workflow automates the complete candidate screening process from email receipt to candidate communication. The workflow is designed to handle job applications sent to a designated email address, perform keyword-based screening, update Google Sheets, and send appropriate responses to candidates.

## Workflow Architecture

### Visual Flow Diagram

```
Email Trigger → Filter Valid Applications → Extract Candidate Info → Keyword Screening
                        ↓                                                    ↓
                   Error Handler                                    Route by Match Status
                        ↓                                          ↙                    ↘
              Send Error Notification                Add to Candidate Tracker    Add to Rejected Applications
                                                            ↓                              ↓
                                                   Generate Matched Email        Generate Rejection Email
                                                            ↓                              ↓
                                                         Send Email Response ←────────────┘
                                                                    ↓
                                                        Log Workflow Completion
```

## Node Descriptions

### 1. Email Trigger (IMAP Email Read)
- **Type**: `n8n-nodes-base.emailReadImap`
- **Purpose**: Monitors the designated email address for new applications
- **Configuration**:
  - Poll interval: Every 5 minutes
  - Mailbox: INBOX
  - Download attachments: Yes
  - Post-process action: Mark as read
- **Credentials**: Gmail IMAP credentials

### 2. Filter Valid Applications (IF Node)
- **Type**: `n8n-nodes-base.if`
- **Purpose**: Validates that emails are sent to the correct address and have attachments
- **Conditions**:
  - Email TO field contains "careers-new-applicants@yourcompany.com"
  - Email has attachments (resume required)
- **Routing**: Valid applications continue, invalid ones go to error handler

### 3. Extract Candidate Info (Code Node)
- **Type**: `n8n-nodes-base.code`
- **Purpose**: Extracts candidate information from email content
- **Functions**:
  - Extract sender name and email address
  - Parse candidate name from email body using regex patterns
  - Process resume attachments
  - Generate application metadata
- **Output**: Structured candidate data object

### 4. Keyword Screening (Code Node)
- **Type**: `n8n-nodes-base.code`
- **Purpose**: Analyzes email content for required keywords
- **Logic**:
  - Searches for "Mid-level", "Python", "GenAI" and their variations
  - Combines email subject and body for comprehensive search
  - Determines match status (≥2 keywords = match)
- **Output**: Screening results with keyword details

### 5. Route by Match Status (IF Node)
- **Type**: `n8n-nodes-base.if`
- **Purpose**: Routes candidates based on screening results
- **Condition**: `isMatch === true`
- **Routing**: 
  - TRUE → Matched candidate path
  - FALSE → Rejected candidate path

### 6. Add to Candidate Tracker (Google Sheets)
- **Type**: `n8n-nodes-base.googleSheets`
- **Purpose**: Adds matched candidates to tracking spreadsheet
- **Configuration**:
  - Operation: Append or Update
  - Sheet: "Candidate Tracker"
  - Match column: Email (prevents duplicates)
- **Data**: Name, Email, Application Date, Status, Keywords Found, Resume File, Application ID

### 7. Add to Rejected Applications (Google Sheets)
- **Type**: `n8n-nodes-base.googleSheets`
- **Purpose**: Adds rejected candidates to separate tracking sheet
- **Configuration**:
  - Operation: Append or Update
  - Sheet: "Rejected Applications"
  - Match column: Email (prevents duplicates)
- **Data**: Name, Email, Application Date, Rejection Reason, Keywords Found

### 8. Generate Matched Email (Code Node)
- **Type**: `n8n-nodes-base.code`
- **Purpose**: Creates personalized acceptance email for matched candidates
- **Features**:
  - Professional email template
  - Personalization with candidate name and keywords
  - Calendly scheduling link integration
  - Application ID for tracking

### 9. Generate Rejection Email (Code Node)
- **Type**: `n8n-nodes-base.code`
- **Purpose**: Creates polite rejection email for unmatched candidates
- **Features**:
  - Professional and respectful tone
  - Encouragement to apply for future positions
  - Company careers page link
  - Application ID for tracking

### 10. Send Email Response (Email Send)
- **Type**: `n8n-nodes-base.emailSend`
- **Purpose**: Sends the generated email response to candidates
- **Configuration**:
  - Dynamic subject and body from previous nodes
  - Recipient from candidate data
  - SMTP credentials for sending
- **Credentials**: SMTP server credentials

### 11. Log Workflow Completion (Code Node)
- **Type**: `n8n-nodes-base.code`
- **Purpose**: Logs successful workflow completion and statistics
- **Data Logged**:
  - Timestamp, candidate details, screening results
  - Keywords found, email type sent
  - Application ID and processing status

### 12. Error Handler (Code Node)
- **Type**: `n8n-nodes-base.code`
- **Purpose**: Handles workflow errors and prepares notifications
- **Functions**:
  - Captures error details and context
  - Creates structured error logs
  - Prepares error notification email content

### 13. Send Error Notification (Email Send)
- **Type**: `n8n-nodes-base.emailSend`
- **Purpose**: Notifies HR team of workflow errors
- **Configuration**:
  - Sends to HR email address
  - Includes error details and timestamp
  - Automated error reporting

## Environment Variables Required

```bash
# Email Configuration
SMTP_FROM_EMAIL=noreply@yourcompany.com

# Google Sheets
GOOGLE_SHEETS_CANDIDATE_TRACKER_ID=your_spreadsheet_id

# Company Information
COMPANY_NAME=Seismic Consulting Group
POSITION_TITLE=Mid-level Python Developer
CALENDLY_LINK=https://calendly.com/your-link
CAREERS_PAGE=https://yourcompany.com/careers
HR_EMAIL=hr@yourcompany.com
HR_NAME=HR Team
```

## Credentials Setup

### 1. Gmail IMAP Credentials
- **Name**: Gmail IMAP
- **Type**: IMAP
- **Configuration**:
  - Host: imap.gmail.com
  - Port: 993
  - Security: SSL/TLS
  - Username: careers-new-applicants@yourcompany.com
  - Password: App-specific password (recommended)

### 2. Google Sheets Service Account
- **Name**: Google Sheets Service Account
- **Type**: Google Service Account
- **Setup**:
  - Create service account in Google Cloud Console
  - Download JSON key file
  - Share spreadsheet with service account email
  - Upload JSON to n8n credentials

### 3. SMTP Credentials
- **Name**: SMTP Credentials
- **Type**: SMTP
- **Configuration**:
  - Host: smtp.gmail.com (or your SMTP server)
  - Port: 587
  - Security: STARTTLS
  - Username: noreply@yourcompany.com
  - Password: App-specific password

## Google Sheets Structure

### Candidate Tracker Sheet
| Column | Description |
|--------|-------------|
| Name | Candidate's full name |
| Email | Candidate's email address |
| Application Date | Date application was received |
| Status | Current status (Pending Review) |
| Keywords Found | Matched keywords list |
| Resume File | Whether resume was attached |
| Application ID | Unique application identifier |

### Rejected Applications Sheet
| Column | Description |
|--------|-------------|
| Name | Candidate's full name |
| Email | Candidate's email address |
| Application Date | Date application was received |
| Rejection Reason | Why application was rejected |
| Keywords Found | Any keywords that were found |

## Workflow Features

### ✅ **Core Requirements Met**
- **Email Trigger**: Monitors designated email address
- **Information Extraction**: Candidate name, email, resume
- **Keyword Screening**: Mid-level, Python, GenAI (≥2 required)
- **Google Sheets Integration**: Separate sheets for matched/rejected
- **Automated Communication**: Personalized emails for both outcomes

### ✅ **Advanced Features**
- **Duplicate Prevention**: Uses email as unique identifier
- **Error Handling**: Comprehensive error capture and notification
- **Logging**: Detailed workflow execution logs
- **Template System**: Professional email templates
- **Resume Processing**: Handles multiple file formats
- **Statistics Tracking**: Monitors workflow performance

### ✅ **Production Ready**
- **Scalable**: Handles multiple applications efficiently
- **Reliable**: Error handling and retry mechanisms
- **Secure**: Service account authentication
- **Maintainable**: Clear node structure and documentation
- **Configurable**: Environment variables for easy customization

## Deployment Instructions

### 1. Import Workflow
1. Open n8n interface
2. Go to Workflows → Import from File
3. Select `n8n_workflow_export.json`
4. Workflow will be imported with all nodes and connections

### 2. Configure Credentials
1. Set up Gmail IMAP credentials
2. Create Google Sheets service account
3. Configure SMTP credentials for sending emails

### 3. Set Environment Variables
1. Add all required environment variables to n8n
2. Update company-specific information
3. Set correct Google Sheets ID

### 4. Test Workflow
1. Send test email to monitored address
2. Verify Google Sheets updates
3. Check email responses are sent
4. Review logs for any issues

### 5. Activate Workflow
1. Enable the workflow in n8n
2. Monitor initial executions
3. Set up alerting for errors
4. Schedule regular maintenance

## Monitoring and Maintenance

### Key Metrics to Monitor
- **Email Processing Rate**: Applications processed per hour
- **Match Rate**: Percentage of candidates that match criteria
- **Error Rate**: Failed executions per total executions
- **Response Time**: Time from email receipt to response sent

### Regular Maintenance Tasks
- **Credential Rotation**: Update passwords and API keys
- **Log Cleanup**: Archive old execution logs
- **Performance Review**: Analyze workflow efficiency
- **Template Updates**: Refresh email templates as needed

## Troubleshooting

### Common Issues
1. **Email Not Triggering**: Check IMAP credentials and connection
2. **Google Sheets Errors**: Verify service account permissions
3. **Email Sending Fails**: Check SMTP credentials and limits
4. **Keyword Matching Issues**: Review screening logic in code nodes

### Error Recovery
- Failed executions can be manually restarted
- Error notifications alert HR team immediately
- Duplicate prevention ensures data integrity
- Comprehensive logging aids in debugging

This n8n workflow provides a complete, production-ready solution for automated candidate screening that meets all the original requirements while adding enterprise-grade features for reliability and maintainability.