import pandas as pd
from src.preprocessing_functions import read_json_file, preprocess_data
from src.constants import OUTPUT_FILE_PATH, JSON_FILE_PATH

def json_to_dataframe(JSON_FILE_PATH):
    try:
        # Read JSON file into a dictionary
        json_data = read_json_file(JSON_FILE_PATH)

        # Process the data
        preprocessed_data = preprocess_data(json_data)

        # Convert the preprocessed data to a DataFrame
        df = pd.DataFrame(preprocessed_data).T
        
        # Store the data in a CSV (could also be writen to a DB from here)
        df.to_csv(OUTPUT_FILE_PATH)
        
        return df
    
    except Exception as e:
        print(f"Error reading or preprocessing JSON file: {e}")
        return None