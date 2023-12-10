import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

TIMEZONE = os.environ.get("LOCAL_TIMEZONE")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TMP_UPLOAD_FILE_PATH = os.environ.get("TMP_UPLOAD_FILE_PATH")
PDF_TEXTS_LIST_PATH = os.environ.get("PDF_TEXTS_LIST")
ALLOWED_EXTENSIONS = os.environ.get("ALLOWED_EXTENSIONS")
ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS")