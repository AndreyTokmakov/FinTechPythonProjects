import json
from typing import Dict


class Utilities:

    @staticmethod
    def read_file(file_path: str) -> str:
        with open(file=file_path, mode='r') as file:
            return file.read().rstrip()

    @staticmethod
    def read_json_file(file_path: str) -> Dict:
        with open(file=file_path, mode='r') as file:
            return json.load(file)
