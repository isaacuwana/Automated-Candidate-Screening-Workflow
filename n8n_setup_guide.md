# n8n Automated Candidate Screening - Setup Guide

## Prerequisites

### 1. n8n Installation
Choose one of the following installation methods:

#### Option A: n8n Cloud (Recommended for beginners)
1. Go to [n8n.cloud](https://n8n.cloud)
2. Sign up for an account
3. Create a new workspace
4. No local installation required

#### Option B: Self-hosted with Docker
```bash
# Create directory for n8n data
mkdir n8n-data

# Run n8n with Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n-data:/home/node/.n8n \
  n8nio/n8n
```

#### Option C: Local Installation with npm
```bash
# Install n8n globally
npm install n8n -g

# Start n8n
n8n start
```

### 2. Email Account Setup

#### Gmail Configuration (Recommended)
1. **Create dedicated email account**: `careers-new-applicants@yourcompany.com`
2. **Enable 2-Factor Authentication**
3. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Save this password for n8n credentials

#### Alternative Email Providers
- **Outlook**: Use app passwords with IMAP/SMTP
- **Custom IMAP**: Any IMAP-compatible email server

### 3. Google Sheets Setup

#### Create Spreadsheet
1. Go to [Google Sheets](https://sheets.google.com)
2. Create new spreadsheet: "Candidate Screening Tracker"
3. Create two sheets:

**Sheet 1: "Candidate Tracker"**
```
| Name | Email | Application Date | Status | Keywords Found | Resume File | Application ID |
|------|-------|------------------|--------|----------------|-------------|----------------|
```

**Sheet 2: "Rejected Applications"**
```
| Name | Email | Application Date | Rejection Reason | Keywords Found |
|------|-------|------------------|------------------|----------------|
```

#### Google Service Account Setup
1. **Go to Google Cloud Console**
2. **Create new project** or select existing
3. **Enable Google Sheets API**:
   - APIs & Services → Library
   - Search "Google Sheets API"
   - Click Enable
4. **Create Service Account**:
   - APIs & Services → Credentials
   - Create Credentials → Service Account
   - Name: "n8n-candidate-screening"
   - Role: Editor
5. **Generate JSON Key**:
   - Click on created service account
   - Keys → Add Key → Create New Key
   - Choose JSON format
   - Download and save securely
6. **Share Spreadsheet**:
   - Copy service account email from JSON file
   - Share your spreadsheet with this email
   - Give "Editor" permissions

## n8n Workflow Setup

### Step 1: Import Workflow

1. **Open n8n interface** (http://localhost:5678 or your cloud URL)
2. **Go to Workflows**
3. **Click "Import from File"**
4. **Select** `n8n_workflow_export.json`
5. **Click Import**

### Step 2: Configure Credentials

#### Gmail IMAP Credentials
1. **Go to Credentials** in n8n
2. **Create New Credential**
3. **Select "IMAP"**
4. **Configure**:
   ```
   Name: Gmail IMAP
   Host: imap.gmail.com
   Port: 993
   Security: SSL/TLS
   Username: careers-new-applicants@yourcompany.com
   Password: [Your App Password]
   ```
5. **Test Connection** and **Save**

#### Google Sheets Service Account
1. **Create New Credential**
2. **Select "Google Service Account"**
3. **Configure**:
   ```
   Name: Google Sheets Service Account
   Service Account Email: [From JSON file]
   Private Key: [From JSON file - entire key including headers]
   ```
4. **Test Connection** and **Save**

#### SMTP Credentials
1. **Create New Credential**
2. **Select "SMTP"**
3. **Configure**:
   ```
   Name: SMTP Credentials
   Host: smtp.gmail.com
   Port: 587
   Security: STARTTLS
   Username: noreply@yourcompany.com
   Password: [App Password for sending account]
   ```
4. **Test Connection** and **Save**

### Step 3: Set Environment Variables

1. **Go to Settings** → **Environment Variables**
2. **Add the following variables**:

```bash
# Email Configuration
SMTP_FROM_EMAIL=noreply@yourcompany.com

# Google Sheets
GOOGLE_SHEETS_CANDIDATE_TRACKER_ID=your_spreadsheet_id_here

# Company Information
COMPANY_NAME=Seismic Consulting Group
POSITION_TITLE=Mid-level Python Developer
CALENDLY_LINK=https://calendly.com/your-scheduling-link
CAREERS_PAGE=https://yourcompany.com/careers
HR_EMAIL=hr@yourcompany.com
HR_NAME=HR Team
```

**To find your Google Sheets ID**:
- Open your spreadsheet in browser
- Copy ID from URL: `https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit`

### Step 4: Configure Workflow Nodes

#### Update Email Trigger Node
1. **Click on "Email Trigger" node**
2. **Select your Gmail IMAP credential**
3. **Verify settings**:
   - Mailbox: INBOX
   - Poll interval: Every 5 minutes
   - Download attachments: Yes

#### Update Google Sheets Nodes
1. **Click on "Add to Candidate Tracker" node**
2. **Select your Google Sheets credential**
3. **Set Document ID**: Use environment variable `{{ $env.GOOGLE_SHEETS_CANDIDATE_TRACKER_ID }}`
4. **Set Sheet Name**: "Candidate Tracker"
5. **Repeat for "Add to Rejected Applications" node** with sheet name "Rejected Applications"

#### Update Email Send Nodes
1. **Click on "Send Email Response" node**
2. **Select your SMTP credential**
3. **Verify FROM email** uses environment variable
4. **Repeat for "Send Error Notification" node**

## Testing the Workflow

### Step 1: Test Email Reception
1. **Send test email** to `careers-new-applicants@yourcompany.com`
2. **Include keywords**: "I am a mid-level Python developer with GenAI experience"
3. **Attach resume** (PDF, DOC, or DOCX)
4. **Check n8n executions** for successful processing

### Step 2: Verify Google Sheets Updates
1. **Check "Candidate Tracker" sheet** for new row
2. **Verify all columns** are populated correctly
3. **Check application ID** format

### Step 3: Confirm Email Response
1. **Check candidate email** for acceptance message
2. **Verify personalization** (name, keywords)
3. **Test Calendly link** functionality

### Step 4: Test Rejection Flow
1. **Send email without required keywords**
2. **Verify rejection email** is sent
3. **Check "Rejected Applications" sheet** for entry

## Workflow Activation

### Step 1: Enable Workflow
1. **Go to workflow editor**
2. **Click "Active" toggle** in top right
3. **Confirm activation**

### Step 2: Monitor Initial Executions
1. **Go to Executions tab**
2. **Watch for successful runs**
3. **Check for any errors**

### Step 3: Set Up Monitoring
1. **Configure error notifications**
2. **Set up regular health checks**
3. **Monitor execution statistics**

## Troubleshooting

### Common Issues

#### Email Trigger Not Working
- **Check IMAP credentials** are correct
- **Verify email account** allows IMAP access
- **Check firewall/network** restrictions
- **Test with manual execution**

#### Google Sheets Errors
- **Verify service account** has sheet access
- **Check spreadsheet ID** is correct
- **Ensure sheet names** match exactly
- **Test API permissions**

#### Email Sending Failures
- **Check SMTP credentials**
- **Verify sending limits** not exceeded
- **Test with different email provider**
- **Check spam/security settings**

#### Keyword Matching Issues
- **Review screening logic** in code node
- **Test with known keyword combinations**
- **Check case sensitivity** settings
- **Verify regex patterns**

### Error Recovery
1. **Check execution logs** for detailed errors
2. **Use manual re-execution** for failed runs
3. **Update credentials** if authentication fails
4. **Contact support** for persistent issues

## Maintenance

### Regular Tasks
- **Monitor execution success rate**
- **Update email templates** as needed
- **Rotate credentials** periodically
- **Review and update keywords**
- **Clean up old executions**

### Performance Optimization
- **Adjust polling frequency** based on volume
- **Optimize code nodes** for efficiency
- **Monitor resource usage**
- **Scale infrastructure** if needed

### Security Best Practices
- **Use app passwords** instead of main passwords
- **Limit service account** permissions
- **Regular credential rotation**
- **Monitor access logs**
- **Keep n8n updated**

## Support and Resources

### n8n Documentation
- [Official n8n Docs](https://docs.n8n.io/)
- [Node Reference](https://docs.n8n.io/integrations/)
- [Community Forum](https://community.n8n.io/)

### API Documentation
- [Gmail API](https://developers.google.com/gmail/api)
- [Google Sheets API](https://developers.google.com/sheets/api)

### Workflow Support
- Check execution logs for detailed error information
- Use n8n community forum for workflow-specific questions
- Review node documentation for configuration options

This setup guide provides everything needed to deploy the n8n workflow successfully. Follow each step carefully and test thoroughly before putting into production use.