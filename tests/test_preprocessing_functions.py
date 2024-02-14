import numpy as np
import unittest
from src.preprocessing_functions import read_json_file, _remove_nulls, _get_note_indexes, _split_notes_from_entryText, _get_clean_notes, _get_clean_dict
from src.constants import JSON_FILE_PATH

class TestPreProcessingFunctions(unittest.TestCase):
    def setUp(self):
        self.imported_json_file = read_json_file(JSON_FILE_PATH)
        self.entryText_simple = ['28.01.2009      Transformer Chamber (Ground   23.01.2009      EGL551039  ',
                                'tinted blue     Floor)                        99 years from              ',
                                '(part of)                                     23.1.2009']
        self.entryText_with_notes = ['21.11.1996      Transformer Site, Manor       16.09.1996      EGL352255  ',
                                    '1               Road                          25 years from              ',
                                    '16 September               ',
                                    '1996                       ',
                                    'NOTE 1: See entry in the Charges Register relating to the rights granted by this lease.',
                                    'The lease also affects other land',
                                    'NOTE 2: No copy of the Lease referred to is held by Land Registry.']
        
    
    def test_imported_file_type(self):
        self.assertIsInstance(self.imported_json_file, list)

    def test_remove_nulls(self):
        test_data = ['string1', 'string2', np.nan, 'string3', None]
        actual_output = _remove_nulls(test_data)
        expected_output = ['string1', 'string2', 'string3']
        self.assertEqual(actual_output, expected_output)
    
    def test_get_note_indexes_simple(self):
        expected_output = []
        self.assertEqual(_get_note_indexes(self.entryText_simple), expected_output)
    
    def test_get_note_indexes_with_notes(self):
        expected_output = [4, 6]
        self.assertEqual(_get_note_indexes(self.entryText_with_notes), expected_output)
        
    def test_split_notes_from_entryText_simple(self):
        expected_output = (['28.01.2009      Transformer Chamber (Ground   23.01.2009      EGL551039  ',
                            'tinted blue     Floor)                        99 years from              ',
                            '(part of)                                     23.1.2009'],
                            [])
        self.assertEqual(_split_notes_from_entryText(self.entryText_simple), expected_output)
        
    def test_split_notes_from_entryText_simple(self):
        expected_output = (['21.11.1996      Transformer Site, Manor       16.09.1996      EGL352255  ',
                            '1               Road                          25 years from              ',
                            '16 September               ',
                            '1996                       '],
                            ['NOTE 1: See entry in the Charges Register relating to the rights granted by this lease.',
                            'The lease also affects other land',
                            'NOTE 2: No copy of the Lease referred to is held by Land Registry.'])
        self.assertEqual(_split_notes_from_entryText(self.entryText_with_notes), expected_output)
        
    def test_get_clean_notes_simple(self):
        expected_output = None
        self.assertEqual((_get_clean_notes(self.entryText_simple)), expected_output)
    
    def test_get_clean_notes_with_notes(self):
        expected_output = {'NOTE 1': 'NOTE 1: See entry in the Charges Register relating to the rights granted by this lease. The lease also affects other land',
                            'NOTE 2': 'NOTE 2: No copy of the Lease referred to is held by Land Registry.'}
        self.assertEqual(_get_clean_notes(self.entryText_with_notes), expected_output) 
    
    def test_get_clean_dict_simple(self):
        expected_output = {'registrationDate': '28.01.2009 tinted blue (part of)',
                            'propertyDescription': 'Transformer Chamber (Ground Floor) ',
                            'leaseDateTerm': '23.01.2009 99 years from 23.1.2009',
                            'lesseeTitle': 'EGL551039  '}
        self.assertEqual(_get_clean_dict(self.entryText_simple), expected_output)
    
    def test_get_clean_dict_with_notes(self):
        expected_output = {'registrationDate': '21.11.1996 1 16 September 1996',
                            'propertyDescription': 'Transformer Site, Manor Road  ',
                            'leaseDateTerm': '16.09.1996 25 years from  ',
                            'lesseeTitle': 'EGL352255   ',
                            'NOTE 1': 'NOTE 1: See entry in the Charges Register relating to the rights granted by this lease. The lease also affects other land',
                            'NOTE 2': 'NOTE 2: No copy of the Lease referred to is held by Land Registry.'}
        self.assertEqual(_get_clean_dict(self.entryText_with_notes), expected_output)
        
if __name__ == '__main__':
    unittest.main()