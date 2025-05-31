# Multi-Agent Requirement Engineering System

A modular, intelligent web system for requirements engineering, powered by LLMs and Hugging Face models. Supports end-to-end requirements intake, analysis, review, and test case generation.

---

## Features

- **Agent 1 (SYS.1 Elicitation):** Requirement intake, pre-processing, and SYS.1 drafting
- **Agent 2 (SYS.2 Analysis):** SYS.2 requirement drafting and structuring
- **Agent 3 (SYS.2 Review):** SYS.2 review, compliance & continuous learning
- **Agent 4 (SYS.5 Testcase Generation):** SYS.2 to SYS.5 test case generation, traceability, and export

---

## Prerequisites

- **Python 3.10** (recommended; 3.9+ may work)
- **pip** (Python package manager)
- Windows 10/11 or Linux/Mac (instructions below are for Windows)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AutoTestGen_MAPS_Agents123/AutoTestGen_MAPS
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate # On Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download spaCy Model
```bash
python -m spacy download en_core_web_sm
```

### 5. Create a `.env` File
Create a file named `.env` in the `AutoTestGen_MAPS` directory with at least:
```
SECRET_KEY=your-secret-key-here
# Add other environment variables as needed
```

---

## Running the Application

### Start the Flask App
```bash
python app.py
```
- The app will open at [http://localhost:5000](http://localhost:5000)
- If it does not open automatically, open your browser and go to that address.

---

## Directory Structure

```
AutoTestGen_MAPS/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create manually)
├── agents/                 # Agent logic (intake, sys2, review, testgen)
├── templates/              # Jinja2 HTML templates (UI for each agent)
├── static/                 # Static files (CSS, JS)
├── Inputs/                 # Input/output files (Excel, TXT)
│   ├── sys1_requirements.xlsx
│   ├── sys2_requirements.xlsx
│   ├── sys2_requirements_reviewed.xlsx
│   └── ...
└── uploads/                # Temporary uploaded files
```

---

## Agent Workflows

### Agent 1: SYS.1 Elicitation
- Upload customer requirements (TXT, DOCX, PDF, XLSX, etc.)
- Extracted SYS.1 requirements are displayed and can be exported (XLSX, CSV, DOCX, PDF)

### Agent 2: SYS.2 Analysis
- Loads SYS.1 requirements automatically or via upload
- Drafts and structures SYS.2 requirements
- Export options available

### Agent 3: SYS.2 Review
- Loads SYS.2 requirements (auto/manual)
- Review, accept, or reject each requirement
- Only "Approved" requirements are exported to `Inputs/sys2_requirements_reviewed.xlsx`

### Agent 4: SYS.5 Testcase Generation
- Loads reviewed SYS.2 requirements (auto/manual)
- Generates SYS.5 test cases for each SYS.2 requirement
- Displays traceability dashboard (charts, tables)
- Export test cases in multiple formats

---

## Example Input Files
- Place your input files in the `Inputs/` directory:
    - `sys1_requirements.xlsx` (for Agent 2)
    - `sys2_requirements.xlsx` (for Agent 3)
    - `sys2_requirements_reviewed.xlsx` (for Agent 4)
- Supported formats: `.xlsx`, `.csv`, `.txt`, `.docx`, `.pdf`

---

## Troubleshooting

### Unresolved Import Warnings in VS Code
- Make sure you have selected the correct Python interpreter (the one in your `venv`)
- Reload VS Code window after installing packages
- Activate your virtual environment in the terminal

### File Not Found Errors
- Ensure your input files are named and placed exactly as expected in the `Inputs/` directory
- Check file permissions if running on Windows

### Port Already in Use
- If you see an error about port 5000, close other Flask instances or change the port in `app.py`

### Other Issues
- Check the terminal for error messages and stack traces
- Ensure all dependencies in `requirements.txt` are installed

---

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Recent UI/UX Updates

- The navigation bar is now fixed at the top of all pages for easier navigation.
- **Agent 3 (SYS.2 Review) Table Defaults:**
    - 'Is Verification Criteria Okay?' column always displays **'Yes'**
    - 'Testable?' column always displays **'Yes'**
    - 'Unambiguity' column always displays **'No'**
    - 'IREB/ASPICE Compliant?' column always displays **'Yes'**
    - The column previously labeled 'IREB Compliant?' is now **'IREB/ASPICE Compliant?'**
- **Note:** These values are UI display defaults for demonstration and do not reflect backend compliance logic. 