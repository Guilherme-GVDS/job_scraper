# config.py
import os
from dotenv import load_dotenv

load_dotenv()

MAX_JOBS = int(os.getenv('MAX_JOBS'))
