from typing import Dict, List, Any
from .base_agent import BaseAgent
import spacy
from transformers import pipeline
import pandas as pd
import json
import uuid
import traceback
import openpyxl
import os

class ReviewAgent(BaseAgent):
    """Agent 3: SYS.2 Review, Compliance & Continuous Learning"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.nlp = spacy.load("en_core_web_sm")
        self.classifier = pipeline("text-classification")
        self.compliance_rules = self._load_compliance_rules()
        self.setup_pipelines()
    
    def setup_pipelines(self):
        """Initialize NLP pipelines and models"""
        # Add custom pipeline components here
        pass
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        """Process SYS.2 requirements for review and compliance"""
        try:
            # Validate input data
            # Assuming input_data['requirements'] is already in the desired format or can be converted
            # For now, let's directly use the requirements from input_data if available
            requirements_to_process = input_data.get('requirements', [])

            if not requirements_to_process:
                 # If requirements are not in input_data, try reading from the specified file
                 file_path = input_data.get('file_path')
                 if file_path and file_path.lower().endswith(('.xlsx', '.xls')):
                     requirements_to_process = self._read_requirements_from_excel(file_path)
                 else:
                      # If no file_path or unsupported file type, try session data (if applicable to Agent 3)
                      # This part depends on how Agent 3 is intended to receive data other than files
                      # For now, we'll assume requirements come either from input_data['requirements'] or the specified file
                      raise ValueError("No requirements provided in input data or valid file path")

            # Check IREB compliance
            compliance_results = self._check_compliance(requirements_to_process)
            
            # Perform linguistic analysis
            linguistic_analysis_results = self._analyze_linguistics(requirements_to_process)
            
            # Combine results with original requirements for table display
            reviewed_requirements = []
            # Create dictionaries for easy lookup by sys2_id
            compliance_lookup = {res['sys2_id']: res for res in compliance_results}
            linguistic_lookup = {res['sys2_id']: res for res in linguistic_analysis_results}

            for req in requirements_to_process:
                req_id = req.get('sys2_id', req.get('id', 'Unknown_ID'))
                combined_req = req.copy() # Start with the original requirement data

                # Add compliance and linguistic analysis results
                compliance_data = compliance_lookup.get(req_id, {})
                linguistic_data = linguistic_lookup.get(req_id, {})

                combined_req['is_verification_criteria_okay'] = compliance_data.get('is_verification_criteria_okay', 'N/A')
                combined_req['testable'] = compliance_data.get('testable', 'N/A')
                combined_req['ireb_compliant'] = compliance_data.get('ireb_compliant', 'N/A')
                combined_req['unambiguity'] = linguistic_data.get('unambiguity', 'N/A')

                # Ensure other expected fields are present, even if N/A, for table consistency
                combined_req['sys1_id'] = combined_req.get('sys1_id', 'N/A')
                combined_req['sys1_requirement'] = combined_req.get('sys1_requirement', 'N/A')
                combined_req['sys2_requirement'] = combined_req.get('sys2_requirement', 'N/A')
                combined_req['type'] = combined_req.get('type', 'N/A')
                combined_req['verification_mapping'] = combined_req.get('verification_mapping', 'N/A')
                combined_req['domain'] = combined_req.get('domain', 'N/A')
                combined_req['priority'] = combined_req.get('priority', 'N/A')
                combined_req['rationale'] = combined_req.get('rationale', 'N/A')
                combined_req['req_status'] = combined_req.get('req_status', 'Draft') # Default status
                combined_req['suggestions'] = combined_req.get('suggestions', 'N/A') # Ensure suggestions is present

                reviewed_requirements.append(combined_req)

            # Generate suggestions based on the combined results (placeholder)
            suggestions = self._generate_suggestions(compliance_results, linguistic_analysis_results)
            
            # Propose test cases (placeholder)
            test_proposals = self._propose_test_cases(requirements_to_process)
            
            # Export accepted requirements to Excel
            accepted_requirements = [req for req in reviewed_requirements if req.get('req_status') == 'Accepted']
            export_message = None
            if accepted_requirements:
                self._export_accepted_requirements(accepted_requirements)
                export_message = f"Successfully exported {len(accepted_requirements)} accepted requirements to sys2_requirements_reviewed.xlsx"
            
            return {
                'status': 'success',
                'sys2_requirements_for_review': reviewed_requirements, # Return combined data for the table
                'compliance_results': compliance_results, # Optional: Return raw compliance results
                'linguistic_analysis': linguistic_analysis_results, # Optional: Return raw linguistic results
                'suggestions': suggestions,
                'test_proposals': test_proposals,
                'export_message': export_message, # Add export message to response
                'metadata': {
                    'source': input_data.get('source', 'unknown'),
                    'timestamp': pd.Timestamp.now().isoformat()
                }
            }
        except ValueError as ve:
            self.log_error(ve, f"Validation Error in ReviewAgent: {ve}")
            return {'status': 'error', 'message': f"Validation Error: {ve}"}
        except Exception as e:
            self.log_error(e, "Error reviewing requirements")
            return {'status': 'error', 'message': str(e)}
    
    def validate(self, data: Any) -> bool:
        """Validate input data"""
        # Restore the previous simple validation logic
        # This will need to be updated later to properly validate the actual input data structure
        return isinstance(data, dict)
    
    def _read_requirements_from_excel(self, file_path: str) -> List[Dict[str, Any]]:
         """Reads SYS.2 requirements from a specified Excel file."""
         requirements = []
         try:
             df = pd.read_excel(file_path)
             # Assuming the Excel file has columns like 'SYS.2 Req. ID', 'SYS.2 System Requirement', etc.
             # Map these column names to the internal keys used in the agent (e.g., sys2_id, sys2_requirement)
             # This mapping needs to be accurate based on your Excel file column headers
             column_mapping = {
                 'SYS.2 Req. ID': 'sys2_id',
                 'SYS.2 System Requirement': 'sys2_requirement',
                 'Verification Criteria': 'verification_criteria', # Map the Verification Criteria column
                 # Add other column mappings as needed
             }
             
             # Rename columns according to the mapping
             df_renamed = df.rename(columns=column_mapping)

             # Convert DataFrame rows to dictionaries
             requirements = df_renamed.to_dict(orient='records')

             print(f"[INFO] Successfully read {len(requirements)} requirements from {file_path}")

             # Add an explicit check for empty requirements list after reading
             if not requirements:
                 print(f"[WARNING] _read_requirements_from_excel read 0 requirements from {file_path}. Check file content and column mappings.")
                 # Raise a specific error if no requirements were read but no exception occurred
                 raise ValueError('No requirements extracted from the Excel file. Check file format and column headers.')

         except FileNotFoundError:
             print(f"[ERROR] Excel file not found at {file_path}")
             # Depending on desired behavior, you might raise an exception or return an empty list
             traceback.print_exc()
             pass # Returning empty list on file not found for now
         except Exception as e:
             print(f"[ERROR] Error reading Excel file {file_path}: {e}")
             # Handle other potential errors during file reading
             traceback.print_exc()
             # Re-raise the exception to be caught by the calling function
             raise e

         return requirements
    
    def _load_compliance_rules(self) -> Dict[str, Any]:
        """Load IREB compliance rules"""
        return {
            'clarity': {
                'rules': [
                    "No ambiguous terms",
                    "Clear and concise language",
                    "No passive voice"
                ]
            },
            'completeness': {
                'rules': [
                    "All necessary information present",
                    "No missing dependencies",
                    "Complete metadata"
                ]
            },
            'consistency': {
                'rules': [
                    "No contradictions",
                    "Consistent terminology",
                    "Consistent format"
                ]
            }
        }
    
    def _check_compliance(self, requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check IREB compliance of requirements"""
        checked_requirements = []
        
        for req in requirements:
            req_id = req.get('sys2_id', req.get('id', 'Unknown_ID'))
            req_text = req.get('sys2_requirement', req.get('content', ''))

            # Enhanced check for Verification Criteria and Testability (basic implementation)
            is_verification_criteria_okay_status = 'Fail' # Default to Fail
            testable_status = 'Fail' # Default to Fail
            ireb_compliant_status = 'Fail' # Default to Fail

            # Check for phrases indicating verification/testability
            verification_phrases = ['shall be tested', 'shall be verified', 'can be measured', 'is measurable', 'can be quantified']
            
            found_verification_phrase = any(phrase in req_text.lower() for phrase in verification_phrases)
            
            if found_verification_phrase:
                is_verification_criteria_okay_status = 'Pass'
                testable_status = 'Pass' # Assume testable if verification is mentioned (simplified)

            # Further refine testability check (e.g., look for quantifiable terms if not already covered)
            quantifiable_terms = ['seconds', 'milliseconds', '%', 'kbps', 'mbps'] # Examples of quantifiable terms
            if testable_status == 'Fail' and any(term in req_text.lower() for term in quantifiable_terms):
                 testable_status = 'Pass'

            # Simplified IREB compliant check - can be expanded significantly
            # For now, consider it compliant if verification criteria is okay and testable
            if is_verification_criteria_okay_status == 'Pass' and testable_status == 'Pass':
                 ireb_compliant_status = 'Pass'

            checked_requirements.append({
                'sys2_id': req_id,
                'is_verification_criteria_okay': is_verification_criteria_okay_status,
                'testable': testable_status,
                'ireb_compliant': ireb_compliant_status
            })
        
        return checked_requirements
    
    def _analyze_linguistics(self, requirements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform linguistic analysis of requirements"""
        analyzed_requirements = []
        
        for req in requirements:
            req_id = req.get('sys2_id', req.get('id', 'Unknown_ID'))
            req_text = req.get('sys2_requirement', req.get('content', ''))

            # Enhanced check for unambiguity (basic implementation)
            unambiguity_status = 'Pass'
            unambiguity_issues = []

            # Example: Check for vague terms (this list can be expanded)
            vague_terms = ['flexible', 'efficient', 'robust', 'appropriate', 'adequate']
            found_vague_terms = [term for term in vague_terms if term.lower() in req_text.lower()]
            if found_vague_terms:
                unambiguity_status = 'Fail'
                unambiguity_issues.append(f'Contains vague terms: {", ".join(found_vague_terms)}')

            # Example: Check for potential pronoun ambiguity (simple check)
            # This requires more sophisticated NLP for true resolution, but a basic check can look for certain pronouns
            ambiguous_pronouns = ['it', 'this', 'they']
            found_ambiguous_pronouns = [pronoun for pronoun in ambiguous_pronouns if pronoun.lower() in req_text.lower()]
            if found_ambiguous_pronouns:
                 # This check is very basic and will likely have false positives. More advanced NLP is needed for accuracy.
                 unambiguity_status = 'Needs Review' # Use 'Needs Review' as it's uncertain without full context
                 unambiguity_issues.append(f'May contain ambiguous pronouns: {", ".join(found_ambiguous_pronouns)}')

            # Add more sophisticated checks here in the future

            analyzed_requirements.append({
                'sys2_id': req_id,
                'unambiguity': unambiguity_status,
                'unambiguity_issues': unambiguity_issues # Include details on issues found
            })
        
        return analyzed_requirements
    
    def _generate_suggestions(self, compliance_results: Dict[str, Any], 
                            linguistic_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate improvement suggestions"""
        suggestions = []
        # Implement suggestion generation logic
        return suggestions
    
    def _propose_test_cases(self, requirements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Propose test cases for functional requirements"""
        test_proposals = []
        # Implement test case proposal logic
        return test_proposals
    
    def _assign_priorities(self, requirements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Assign priorities to requirements"""
        prioritized_requirements = []
        # Implement priority assignment logic
        return prioritized_requirements

    def review_requirements(self, sys2_requirements):
        """
        Reviews SYS.2 requirements, generates suggestions, and proposes test cases.

        Args:
            sys2_requirements (list): A list of dictionaries, where each dictionary
                                      represents a SYS.2 requirement.
                                      Expected keys: 'id', 'content', etc.

        Returns:
            tuple: A tuple containing:
                - review_results (list): Results of the review for each requirement.
                - suggestions (list): Generated suggestions for improvement.
                - test_proposals (list): Proposed test cases.
        """
        review_results = []
        suggestions = []
        test_proposals = []

        # Placeholder logic: Simulate review and generate sample data
        for sys2_req in sys2_requirements:
            req_id = sys2_req.get('id', 'Unknown_SYS2_ID')
            req_content = sys2_req.get('content', 'No SYS.2 content')

            # Simulate review status (e.g., based on keywords or randomly)
            status = 'compliant'
            if "implement" in req_content.lower():
                status = 'needs_review'
            if "system" in req_content.lower() and "user" in req_content.lower():
                status = 'non_compliant'

            review_results.append({
                'requirement_id': req_id,
                'status': status,
                'notes': f'Review status: {status}'
            })

            # Generate a sample suggestion if status is not 'compliant'
            if status != 'compliant':
                suggestions.append({
                    'requirement_id': req_id,
                    'content': f'Suggestion for {req_id}: Refine wording for better clarity.'
                })

            # Generate a sample test case proposal for each requirement
            test_proposals.append({
                'requirement_id': req_id,
                'description': f'Verify {req_id} functionality.',
                'steps': 'Step 1: ... Step 2: ...'
            })

        return review_results, suggestions, test_proposals 

    def _export_accepted_requirements(self, accepted_requirements: List[Dict[str, Any]]) -> bool:
        """Export accepted requirements to Excel file"""
        try:
            # Select only the required fields and create a new list of dictionaries
            export_data = []
            for req in accepted_requirements:
                export_data.append({
                    'SYS.2 Req. ID': req.get('sys2_id', 'N/A'),
                    'SYS.2 System Requirement': req.get('sys2_requirement', 'N/A')
                })
            
            print("[DEBUG] Export data prepared:", export_data[:5]) # Print first 5 rows for debug

            df = pd.DataFrame(export_data)

            # Define the output file path
            # Using the hardcoded path provided by the user:
            output_path = r'D:\AgentX\AutoTestGen_MAPS_Agents123\AutoTestGen_MAPS\Inputs\sys2_requirements_reviewed.xlsx'

            # Ensure the directory exists
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)

            print(f"[DEBUG] Attempting to save Excel file to: {output_path}")

            try:
                # Export to Excel with formatting
                writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
                df.to_excel(writer, index=False, sheet_name='Accepted Requirements')

                # Get the xlsxwriter workbook and worksheet objects.
                workbook  = writer.book
                worksheet = writer.sheets['Accepted Requirements']

                # Add a header format.
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#D7E4BC',
                    'border': 1})

                # Write the column headers with the defined format.
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)

                # Set column widths
                for i, col in enumerate(df.columns):
                    # Set a default width or calculate based on content (more complex)
                    # A reasonable default for requirement text might be larger
                    width = 30 # Default width
                    if col == 'SYS.2 System Requirement':
                         width = 80 # Wider for requirement text
                    elif col == 'SYS.2 Req. ID':
                         width = 20 # Narrower for ID
                    worksheet.set_column(i, i, width)

                # Close the Pandas Excel writer and save the Excel file.
                writer.close() # This saves the file

                print(f"[INFO] Successfully exported accepted requirements to {output_path}")
                return True # Indicate success

            except Exception as e:
                print(f"[ERROR] Exception during Excel export: {e}")
                import traceback
                traceback.print_exc()
                raise e # Re-raise the exception so the backend endpoint catches it

        except Exception as e:
            # This outer catch might be redundant if we re-raise inside
            # but good to have during debugging.
            print(f"[ERROR] An error occurred in _export_accepted_requirements: {e}")
            import traceback
            traceback.print_exc()
            raise e # Re-raise the exception 