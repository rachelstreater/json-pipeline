from src.data_pipeline import json_to_dataframe
from src.constants import JSON_FILE_PATH, OUTPUT_FILE_PATH

def main():
    
    
    # Call the data pipeline function
    data_frame = json_to_dataframe(JSON_FILE_PATH)

    # Display the resulting DataFrame
    print(f"CSV can be found here: {OUTPUT_FILE_PATH}")
    print("Preview of DataFrame created from JSON file after preprocessing:")
    print(data_frame.head())

if __name__ == "__main__":
    main()