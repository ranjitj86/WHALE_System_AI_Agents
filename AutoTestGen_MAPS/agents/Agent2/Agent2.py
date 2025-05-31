import pandas as pd
from win10toast import ToastNotifier
import os

def export_sys2_requirements():
    try:
        # Create DataFrame with only SYS.2 Req. ID and SYS.2 System Requirement columns
        df = pd.DataFrame({
            'SYS.2 Req. ID': ['SYS.2.1', 'SYS.2.2'],
            'SYS.2 System Requirement': ['Sample System Requirement 1', 'Sample System Requirement 2']
        })
        
        # Define the output path
        output_path = os.path.join('D:', 'AgentX', 'AutoTestGen_MAPS_Agents123', 'AutoTestGen_MAPS', 'Inputs', 'sys2_requirements.xlsx')
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Export to Excel
        df.to_excel(output_path, index=False)
        
        # Show toast notification
        toaster = ToastNotifier()
        toaster.show_toast(
            "SYS.2 requirements and data generated successfully",
            f"sys2_requirements.xlsx has been exported to {output_path}",
            duration=5,
            threaded=True
        )
        
        return True
    except Exception as e:
        # Show error notification
        toaster = ToastNotifier()
        toaster.show_toast(
            "Export Failed",
            f"Error exporting file: {str(e)}",
            duration=5,
            threaded=True
        )
        return False 