from typing import Dict, List, Any
from .base_agent import BaseAgent
import spacy
from transformers import pipeline
import pandas as pd
import json
# Import uuid to generate unique IDs
import uuid

class ElicitationAgent(BaseAgent):
    """Agent 1: Requirement Elicitation and SYS.1 Drafting"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.nlp = spacy.load("en_core_web_sm")
        self.classifier = pipeline("text-classification")
        self.setup_pipelines()
    
    def setup_pipelines(self):
        """Initialize NLP pipelines and models"""
        # Add custom pipeline components here
        pass
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        """Process input data and generate SYS.1 requirements"""
        try:
            # Extract text from various input formats
            text_content = self._extract_text(input_data)
            
            # Process text with NLP
            doc = self.nlp(text_content)
            
            # Extract raw customer requirements
            customer_requirements = self._extract_customer_requirements(doc)
            
            # Generate SYS.1 requirements and establish traceability
            # This method will now generate multiple SYS.1 per customer requirement
            sys1_requirements = self._generate_sys1_requirements(customer_requirements)
            
            # Analyze feasibility (update to work with separate lists if needed)
            # feasibility_scores = self._analyze_feasibility(sys1_requirements) # Adjust if needed
            
            # Assign domain and priority to SYS.1 requirements
            for req in sys1_requirements:
                req['domain'] = self._classify_domain(req['sys1_requirement'])
                req['priority'] = self._assign_priority(req['sys1_requirement'])
                req['req_status'] = 'Draft' # Initial status for SYS.1
            
            # Return both customer and SYS.1 requirements, and the traceability links (implicit in SYS.1)
            return {
                'status': 'success',
                'customer_requirements': customer_requirements,
                'sys1_requirements': sys1_requirements,
                'metadata': {
                    'source': input_data.get('source', 'unknown'),
                    'timestamp': pd.Timestamp.now().isoformat()
                }
            }
        except Exception as e:
            self.log_error(e, "Error processing input data")
            return {'status': 'error', 'message': str(e)}
    
    def validate(self, data: Any) -> bool:
        """Validate input data"""
        required_fields = ['content', 'format']
        return all(field in data for field in required_fields)
    
    def _extract_text(self, input_data: Dict[str, Any]) -> str:
        """Extract text from various input formats"""
        # Implement format-specific extraction logic
        return input_data.get('content', '')
    
    def _extract_customer_requirements(self, doc) -> List[Dict[str, Any]]:
        """Extract raw customer requirements from text."""
        customer_requirements = []
        # Split by newlines for robust extraction of individual customer requirements
        lines = [line.strip() for line in doc.text.split('\n') if line.strip()]
        for i, line in enumerate(lines, 1):
            cust_id = f'CUST_REQ-{i:03d}'
            # Extract the requirement text, removing potential prefix
            customer_req_text = line
            if ':' in line:
                parts = line.split(':', 1)
                # If the part before colon looks like an ID (e.g., CUST_REQ-001)
                if parts[0].strip().upper().startswith('CUST_REQ-'):
                     customer_req_text = parts[1].strip()

            customer_requirements.append({
                'customer_id': cust_id,
                'customer_requirement': customer_req_text, # Use stripped text
                # Could add original line here if needed for context
            })
        # Pad to at least a certain number if needed, but maybe not necessary for just extraction
        return customer_requirements
    
    def _generate_sys1_requirements(self, customer_requirements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate SYS.1 requirements from customer requirements, potentially one-to-many."""
        sys1_requirements = []
        sys1_counter = 1

        for cust_req in customer_requirements:
            customer_id = cust_req.get('customer_id', '')
            customer_text = cust_req.get('customer_requirement', '')

            if customer_text:
                # --- One-to-Many Generation Logic (Placeholder) ---
                # This is where you would implement logic to generate multiple SYS.1s
                # For demonstration, let's generate 1-2 SYS.1s per customer requirement
                num_sys1 = 1 # Simple case: 1 SYS.1 per customer requirement
                # num_sys1 = 2 # Example: generate 2 SYS.1s per customer requirement

                for i in range(num_sys1):
                    sys1_id = f'SYS.1-{sys1_counter:03d}'
                    # Use spaCy to extract a more complete action phrase
                    doc = self.nlp(customer_text)
                    action_phrase_parts = []
                    root_verb = None

                    # Find the root verb
                    for token in doc:
                        if token.dep_ == "ROOT" and token.pos_ == "VERB":
                            root_verb = token
                            break

                    if root_verb:
                        # Start action phrase with the root verb
                        action_phrase_parts.append(root_verb.text)
                        # Add key dependents: direct objects, nominal objects, and relevant adverbs/prepositions
                        for child in root_verb.children:
                            if child.dep_ in ["dobj", "nobj", "advmod"] or (child.dep_ == "prep" and len(list(child.children)) > 0): # Include prep with children
                                action_phrase_parts.append(child.text)
                                # For prepositions, also try to include their objects
                                if child.dep_ == "prep":
                                    for grand_child in child.children:
                                        if grand_child.dep_ in ["pobj", "dobj", "nsubj", "attr", "compound"]:
                                            action_phrase_parts.append(grand_child.text)

                        # Join parts to form the action phrase
                        action_phrase = " ".join(action_phrase_parts)
                    else:
                        # Fallback if no root verb is found
                        action_phrase = f"implement the capability to {customer_text.lower()}"

                    # Construct the SYS.1 requirement text
                    # Keep the original customer text for context, but prioritize the extracted action
                    sys1_text = f"The system shall {action_phrase}. [Derived from: {customer_text} - Add specific behavior/conditions here]."

                    sys1_requirements.append({
                        'sys1_id': sys1_id,
                        'sys1_requirement': sys1_text,
                        'customer_trace_ids': [customer_id], # List of customer IDs this SYS.1 traces to
                        'domain': '', # Will be classified later
                        'priority': '', # Will be assigned later
                        'req_status': 'Draft', # Initial status
                        'rationale': f"Justification: This SYS.1 requirement is necessary to address the customer need for \"{customer_text}\".", # More descriptive rationale
                        'customer_id': customer_id, # Add customer ID
                        'customer_requirement': customer_text # Add customer requirement text
                    })
                    sys1_counter += 1

        # Pad SYS.1 requirements if necessary to meet a minimum count for the table
        min_sys1_count = 10 # Example minimum
        while len(sys1_requirements) < min_sys1_count:
             sys1_id = f'SYS.1-{sys1_counter:03d}'
             sys1_requirements.append({
                 'sys1_id': sys1_id,
                 'sys1_requirement': '',
                 'customer_trace_ids': [], # No trace for padded requirements
                 'domain': '',
                 'priority': '',
                 'req_status': 'Draft',
                 'rationale': ''
             })
             sys1_counter += 1


        return sys1_requirements
    
    def _analyze_feasibility(self, requirements: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze feasibility of requirements (currently a placeholder)."""
        feasibility_scores = {}
        # Implement feasibility analysis logic based on SYS.1 requirements
        return feasibility_scores
    
    def _classify_domain(self, requirement_text: str) -> str:
        """Classify the domain of a requirement based on keywords."""
        text = requirement_text.lower()
        # Simple keyword-based classification
        if any(keyword in text for keyword in ['software', 'code', 'algorithm', 'api', 'database', 'interface', 'ui', 'ux']):
            return 'Software'
        elif any(keyword in text for keyword in ['hardware', 'chip', 'processor', 'memory', 'board', 'electronic', 'circuit']):
            return 'Hardware'
        elif any(keyword in text for keyword in ['mechanical', 'chassis', 'structure', 'bolt', 'screw', 'material', 'assembly']):
            return 'Mechanical'
        else:
            return 'System' # Default domain
    
    def _assign_priority(self, requirement_text: str) -> str:
        """Assign a priority to a requirement based on keywords or analysis."""
        text = requirement_text.lower()
        # Simple keyword-based priority assignment (can be expanded)
        if any(keyword in text for keyword in ['must', 'shall', 'critical', 'safety']):
            return 'High'
        elif any(keyword in text for keyword in ['should', 'important']):
            return 'Medium'
        elif any(keyword in text for keyword in ['could', 'nice to have', 'optional']):
            return 'Low'
        else:
            return 'Medium' # Default priority 

    # This method is now redundant as status updates are handled in the Flask route on the session data
    # def update_requirement_status(self, requirement_id: str, new_status: str):
    #     """Updates the status of a specific requirement."""
    #     self.log_info(f"Attempting to update status for {requirement_id} to {new_status}")
    #     pass 