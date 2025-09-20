import json
import os

class DataReader:
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                    'data', 'additional_info.json')
        self.additional_info = self._load_data()

    def _load_data(self):
        """Load additional info from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Additional info file not found: {self.data_file}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in file: {self.data_file}")

    def get_additional_info(self):
        """Return the loaded additional info"""
        return self.additional_info
