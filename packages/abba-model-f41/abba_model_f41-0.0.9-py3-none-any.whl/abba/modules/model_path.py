import os
from pathlib import Path


F41_PATH="models/f41/f41.ftz"

def get_project_root() -> str: return os.path.dirname(__file__)
def get_model_path() -> str: return get_project_root() + '/models'
def get_f41_model_path() -> str: return get_model_path() + f"/{F41_PATH}"
