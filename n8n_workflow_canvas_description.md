# n8n Workflow Canvas Visual Description

## Workflow Canvas Layout

Since I cannot generate actual screenshots, here's a detailed description of how the workflow would appear in the n8n visual editor:

### Main Flow (Left to Right)

```
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│   Email Trigger │───▶│ Filter Valid Apps   │───▶│ Extract Candidate   │───▶│ Keyword         │
│   (IMAP Read)   │    │     (IF Node)       │    │     Info (Code)     │    │ Screening (Code)│
│   📧 Every 5min │    │ ✓ Correct address   │    │ 👤 Name extraction  │    │ 🔍 Mid-level    │
└─────────────────┘    │ ✓ Has attachments   │    │ 📎 Resume files     │    │ 🐍 Python       │
                       └─────────────────────┘    └─────────────────────┘    │ 🤖 GenAI        │
                                │                                             └─────────────────┘
                                │ (False)                                              │
                                ▼                                                      ▼
                       ┌─────────────────┐                                   ┌─────────────────┐
                       │ Error Handler   │                                   │ Route by Match  │
                       │    (Code)       │                                   │ Status (IF Node)│
                       │ ⚠️ Log errors   │                                   │ ≥2 keywords?   │
                       └─────────────────┘                                   └─────────────────┘
                                │                                                      │
                                ▼                                                      │
                       ┌─────────────────┐                                           │
                       │ Send Error      │                                           │
                       │ Notification    │                                           │
                       │ 📧 Alert HR     │                                           │
                       └─────────────────┘                                           │
                                                                                     │
                                                                    ┌────────────────┴────────────────┐
                                                                    │ (True - Match)    (False - No Match)
                                                                    ▼                              ▼
```

### Branching Paths (Match vs No Match)

#### Matched Candidate Path (Top Branch)
```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│ Add to Candidate    │───▶│ Generate Matched    │───▶│                     │
│ Tracker (Sheets)    │    │ Email (Code)        │    │                     │
│ 📊 Pending Review   │    │ ✅ Acceptance email │    │                     │
│ 📝 Keywords found   │    │ 📅 Calendly link    │    │                     │
└─────────────────────┘    └─────────────────────┘    │                     │
                                                      │   Send Email        │
                                                      │   Response          │
                                                      │   (Email Send)      │
                                                      │   📧 To candidate   │
                                                      │                     │
┌─────────────────────┐    ┌─────────────────────┐    │                     │
│ Add to Rejected     │───▶│ Generate Rejection  │───▶│                     │
│ Applications        │    │ Email (Code)        │    │                     │
│ (Sheets)            │    │ ❌ Polite rejection │    │                     │
│ 📊 Rejection reason │    │ 🔗 Careers page     │    └─────────────────────┘
└─────────────────────┘    └─────────────────────┘                │
```

#### Rejected Candidate Path (Bottom Branch)
```
                                                                    ▼
                                                      ┌─────────────────────┐
                                                      │ Log Workflow        │
                                                      │ Completion (Code)   │
                                                      │ 📝 Statistics       │
                                                      │ ✅ Success status   │
                                                      └─────────────────────┘
```

## Node Visual Characteristics

### Node Colors and Icons (as they appear in n8n)

1. **Email Trigger** 
   - Color: Blue
   - Icon: 📧 (Email icon)
   - Shape: Rounded rectangle
   - Status indicator: Green dot when active

2. **IF Nodes (Filter, Route)**
   - Color: Orange
   - Icon: ❓ (Question mark)
   - Shape: Diamond-like
   - Branches: True/False paths clearly marked

3. **Code Nodes**
   - Color: Purple
   - Icon: </> (Code brackets)
   - Shape: Rounded rectangle
   - Custom labels for each function

4. **Google Sheets Nodes**
   - Color: Green
   - Icon: 📊 (Spreadsheet icon)
   - Shape: Rounded rectangle
   - Shows sheet name in subtitle

5. **Email Send Nodes**
   - Color: Red
   - Icon: 📤 (Send icon)
   - Shape: Rounded rectangle
   - Shows recipient in subtitle

### Connection Lines
- **Success paths**: Solid green lines
- **Error paths**: Dashed red lines
- **Conditional branches**: Labeled with TRUE/FALSE
- **Data flow direction**: Arrows on connection lines

## Canvas Organization

### Horizontal Layout (Left to Right)
```
Column 1: Trigger & Validation
├── Email Trigger (240, 300)
├── Filter Valid Applications (460, 300)
└── Error Handler (680, 500)

Column 2: Data Processing
├── Extract Candidate Info (680, 200)
└── Keyword Screening (900, 200)

Column 3: Routing & Decision
└── Route by Match Status (1120, 200)

Column 4: Data Storage
├── Add to Candidate Tracker (1340, 100)
└── Add to Rejected Applications (1340, 300)

Column 5: Email Generation
├── Generate Matched Email (1560, 100)
└── Generate Rejection Email (1560, 300)

Column 6: Communication & Logging
├── Send Email Response (1780, 200)
├── Log Workflow Completion (2000, 200)
└── Send Error Notification (900, 500)
```

### Vertical Spacing
- **Main flow**: Y-coordinate 200 (top level)
- **Standard flow**: Y-coordinate 300 (middle level)
- **Error handling**: Y-coordinate 500 (bottom level)

## Interactive Elements

### Node Configuration Panels
Each node when clicked shows:
- **Parameters tab**: Node-specific settings
- **Settings tab**: Node name, notes, retry settings
- **Credentials tab**: Authentication settings (where applicable)

### Execution Flow Visualization
- **Green checkmarks**: Successful execution
- **Red X marks**: Failed execution
- **Data preview**: Click connections to see data flow
- **Execution time**: Shows processing duration

### Workflow Controls
- **Play button**: Manual execution
- **Active toggle**: Enable/disable workflow
- **Settings gear**: Workflow-level configuration
- **Save button**: Persist changes

## Canvas Features

### Zoom and Navigation
- **Zoom controls**: + / - buttons in bottom right
- **Fit to view**: Button to show entire workflow
- **Pan**: Click and drag empty canvas areas
- **Node selection**: Click nodes to select/configure

### Visual Indicators
- **Active workflow**: Green "Active" badge
- **Execution status**: Color-coded node borders
- **Data flow**: Animated dots during execution
- **Error states**: Red highlighting on failed nodes

### Workflow Statistics (Bottom Panel)
- **Total executions**: Count of workflow runs
- **Success rate**: Percentage of successful runs
- **Average execution time**: Performance metrics
- **Last execution**: Timestamp of most recent run

This visual layout provides a clear, logical flow from email receipt through processing to final communication, with proper error handling and logging throughout the process. The n8n interface would show this as an interactive, visual workflow that can be easily understood and modified by non-technical users.