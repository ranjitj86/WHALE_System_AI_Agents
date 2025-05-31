[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?repo=yourusername/your-repo)

# WHALE: Multi-Agent Requirement Engineering System

An AI-powered systems engineering co-pilot for the Automotive Industry.

## Features

- **SYS.1 Elicitation:** Upload and process raw inputs to extract and draft initial requirements.
- **SYS.2 Analysis:** Analyze and structure the drafted requirements.
- **SYS.2 Review:** Review requirements against standards and guidelines.
- **SYS.5 Testcase Generation:** Generate test cases based on requirements.

## Setup

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Create a virtual environment and activate it:**
   ```
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python AutoTestGen_MAPS/app.py
   ```

## Notes

- All file paths are now cross-platform and relative to the project directory.
- Store sensitive data and machine-specific paths in a `.env` file (not committed to git).
- For development, ensure the `Inputs/` and `uploads/` directories exist or will be created by the app.

## License

[MIT](LICENSE) 