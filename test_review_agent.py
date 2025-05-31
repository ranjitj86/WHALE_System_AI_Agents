from AutoTestGen_MAPS.agents.review_agent import ReviewAgent
import os

def main():
    # Initialize the ReviewAgent
    agent = ReviewAgent()
    
    # Path to the input file
    input_file = os.path.join('AutoTestGen_MAPS', 'Inputs', 'sys2_requirements.xlsx')
    
    # Prepare input data
    input_data = {
        'file_path': input_file,
        'source': 'automatic_file'
    }
    
    # Process the requirements
    result = agent.process(input_data)
    
    # Print results
    print("\nProcessing Results:")
    print("------------------")
    print(f"Status: {result.get('status', 'unknown')}")
    
    if result.get('status') == 'success':
        requirements = result.get('sys2_requirements_for_review', [])
        print(f"\nProcessed {len(requirements)} requirements")
        
        # Print first few requirements as example
        print("\nSample Requirements:")
        for req in requirements[:3]:
            print(f"\nID: {req.get('sys2_id', 'N/A')}")
            print(f"Requirement: {req.get('sys2_requirement', 'N/A')}")
            print(f"Verification Criteria: {req.get('is_verification_criteria_okay', 'N/A')}")
            print(f"Testable: {req.get('testable', 'N/A')}")
            print(f"IREB Compliant: {req.get('ireb_compliant', 'N/A')}")
            print(f"Unambiguity: {req.get('unambiguity', 'N/A')}")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    main() 