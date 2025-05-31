from .base_agent import BaseAgent
from typing import Dict, List, Any, Optional
import pandas as pd
import os

class TestGenAgent(BaseAgent):
    """Agent 4: SYS.2 to SYS.5 Test Case Generator"""
    
    # Define the expected column names for SYS.2 requirements
    REQUIRED_COLUMNS = {
        'SYS.2 Req. ID': str,
        'SYS.2 System Requirement': str,
        # Add other relevant SYS.2 columns here if necessary for test generation
    }

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        # Basic initialization for Agent 4
        self.agent_name = "Agent 4"
        self.agent_description = "SYS.2 to SYS.5 Test Case Generator"
        
        # Define the default input path
        self.default_input_path = os.path.join(
            os.path.expanduser("~"),
            "Desktop",
            "AutoTestGen_Project",
            "AutoTestGen_MAPS",
            "Inputs",
            "sys2_requirements_reviewed.xlsx"
        )

    def load_requirements(self, file_path: str) -> List[Dict[str, Any]]:
        """Load SYS.2 requirements from a specified Excel file."""
        print(f"[{self.agent_name}] Attempting to load requirements from: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Input file not found: {file_path}")

        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            
            # Convert relevant columns to list of dictionaries
            # Use the defined REQUIRED_COLUMNS to select and potentially rename columns
            loaded_data = []
            for index, row in df.iterrows():
                req_data = {}
                missing_columns = []
                for col, dtype in self.REQUIRED_COLUMNS.items():
                    if col in df.columns:
                        # Safely convert data, handle potential NaN/None if necessary
                        value = row[col]
                        # Simple handling for float NaNs in string columns
                        if pd.isna(value) and dtype == str:
                            req_data[col] = ""
                        else:
                             req_data[col] = str(value) if dtype == str else value # Ensure correct type or keep original
                    else:
                        missing_columns.append(col)
                        req_data[col] = "" # Provide a default empty string for missing expected columns

                if missing_columns:
                    print(f"[{self.agent_name}] Warning: Missing expected columns in {file_path}: {', '.join(missing_columns)}")
                
                # Only include rows that have at least an ID or a requirement text
                if req_data.get('SYS.2 Req. ID') or req_data.get('SYS.2 System Requirement'):
                     loaded_data.append(req_data)

            print(f"[{self.agent_name}] Successfully loaded {len(loaded_data)} requirements.")
            return loaded_data
            
        except Exception as e:
            print(f"[{self.agent_name}] Error loading file {file_path}: {e}")
            raise IOError(f"Error reading Excel file {file_path}: {e}")

    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Basic process method for Agent 4."""
        print(f"[{self.agent_name}] Processing data: {data}")
        
        # Placeholder for test case generation logic
        generated_test_cases = []
        # In a real implementation, you would process input data (e.g., requirements)
        # and generate test cases.
        
        # For now, just return a success status and placeholder data
        return {
            'status': 'success',
            'message': f'{self.agent_name} processed data.',
            'test_cases': generated_test_cases
        }

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Basic validation method for Agent 4."""
        print(f"[{self.agent_name}] Validating data: {data}")
        # In a real implementation, you would validate the input data.
        # For now, just return a success status.
        return {
            'status': 'success',
            'message': f'{self.agent_name} data validated successfully.'
        }

    def generate_test_cases(self, requirements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate SYS.5 test cases from SYS.2 requirements, including all required fields."""
        test_cases = []
        for idx, req in enumerate(requirements, 1):
            sys2_id = req.get('SYS.2 Req. ID', f'SYS2-{idx}')
            sys2_req = req.get('SYS.2 System Requirement', '')
            test_case = {
                'SYS.2 Req. ID': sys2_id,
                'SYS.2 System Requirement': sys2_req,
                'Test Case ID': f"TC-{sys2_id}",
                'Description': f"Validate: {sys2_req}",
                'Preconditions': "System is set up and ready for validation.",
                'Test Steps': "1. Review the requirement.\n2. Execute the system function as described.",
                'Expected Results': f"System meets the requirement: {sys2_req}",
                'Pass/Fail Criteria': "Test passes if the expected result is observed without deviation.",
                'Priority': req.get('Priority', 'Medium'),
            }
            test_cases.append(test_case)
        return test_cases 