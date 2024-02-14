import os
import pandas as pd
import unittest
import json
from src.data_pipeline import json_to_dataframe
from src.constants import JSON_FILE_PATH

class TestJsonToDataFrame(unittest.TestCase):
    def setUp(self):
        self.json_file_path = JSON_FILE_PATH
        self.result_df = json_to_dataframe(self.json_file_path)
        
    def test_valid_json(self):
        # Test with valid JSON
        self.assertIsInstance(self.result_df, pd.DataFrame) # Check if the result is a DataFrame

    def test_invalid_json(self):
        invalid_json_data = '''
                "scheduleType": "SCHEDULE OF NOTICES OF LEASE",
                "scheduleEntry": [
                    {
                        "entryNumber": "1",
                        "entryDate": "",
                        "entryType": "Schedule of Notices of Leases",
                        "entryText": [
                            "21.11.1996      Transformer Site, Manor       16.09.1996      EGL352255  ",
                            "1               Road                          25 years from              ",
                            "16 September               ",
                            "1996                       ",
                            "NOTE 1: See entry in the Charges Register relating to the rights granted by this lease.",
                            "The lease also affects other land",
                            "NOTE 2: No copy of the Lease referred to is held by Land Registry."
                        ]
                    }
                ]
            }
        }]
        '''     
        test_json_file_path = 'temp_test_file.json'
        with open(test_json_file_path, 'w') as json_file:
            json.dump(invalid_json_data, json_file)  # Save JSON to a temporary file
        
        result_df_invalid = json_to_dataframe(test_json_file_path) # Run the function
        os.remove('temp_test_file.json')
        self.assertIsNone(result_df_invalid) # Check if the result is None

    
    def test_main_cols_match(self):
        expected_columns = ['registrationDate', 'propertyDescription', 'leaseDateTerm', 'lesseeTitle']
        actual_columns = self.result_df.columns.tolist()
        self.assertTrue(set(expected_columns).issubset(actual_columns))
        
    
        


if __name__ == '__main__':
    unittest.main()