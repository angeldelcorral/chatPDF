import os 
import json
import pickle

from io import BytesIO
from flask import jsonify
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from langchain import base_language as lang

from langchain.utilities.anthropic import get_num_tokens_anthropic as get_num_tokens

from langdetect import detect

from .config import TMP_UPLOAD_FILE_PATH, PDF_TEXTS_LIST_PATH
from .config import OPENAI_API_KEY as API_KEY

SISTEM_PATH = os.path.abspath(os.path.dirname(__file__))

class ReturnJsonRequest:
    def __init__(self) -> None:
        self.object_return = {
            "code": "",
            "message": "",
            "data": {}
        }

    def json_return_format(self, code=int, message=str, data=None):
        self.object_return["code"] = code
        self.object_return["message"] = message
        self.object_return["data"] = data
        return jsonify(**self.object_return), 201



class ManagePDF:
    def __init__(self, request=None) -> None:
        SISTEM_PATH = os.path.abspath(os.path.dirname(__file__))
        self.text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len
        )
        self.file = request.files['file']
        self.filename = self.file.filename
        self.upload_filepath = f'{TMP_UPLOAD_FILE_PATH}{self.filename}'
        self.text_from_pdf = ""
        self.raw_text = ""
        self.tmp_path = ""
        self.json_texts_list_path = SISTEM_PATH + PDF_TEXTS_LIST_PATH + 'object_info.pickle'

    def save_temp_file(self):
        os.makedirs(SISTEM_PATH + TMP_UPLOAD_FILE_PATH, exist_ok=True)
        self.tmp_path = os.path.join(SISTEM_PATH + TMP_UPLOAD_FILE_PATH, self.filename)
 
        file_bytes_io = BytesIO(self.file.read())
        # with open(self.upload_filepath, 'wb') as f:
        with open(self.tmp_path, 'wb') as f:
            f.write(file_bytes_io.getbuffer())

    def reading_pdf(self):
        pdf = PdfReader(self.tmp_path)
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                self.raw_text += text
        self.texts_list = self.text_splitter.split_text(self.raw_text)
        self.embeddings = OpenAIEmbeddings()
        self.docsearch = FAISS.from_texts(self.texts_list, self.embeddings)

    def remove_temp_file(self):
        os.remove(self.tmp_path)

    def clean_json_file(self):
        os.remove(self.json_texts_list_path)

    def save_json_texts_list(self):
        os.makedirs(SISTEM_PATH + PDF_TEXTS_LIST_PATH, exist_ok=True)
        with open(self.json_texts_list_path, 'wb') as f:
            pickle.dump(self.docsearch, f)

        
        # with open(self.json_texts_list_path, 'a') as f:
        #     texts_list = self.text_splitter.split_text(self.raw_text)
        #     json_data = {"texts": texts_list}
        #     f.write(json.dumps(json_data))
        #     f.close()


class ChatPDFBot:
    def __init__(self) -> None:
        self.json_texts_list_path = SISTEM_PATH + PDF_TEXTS_LIST_PATH + 'object_info.pickle'
        # self.texts_list = json.loads(open(self.json_texts_list_path).read()).get('texts')
        # self.embeddings = OpenAIEmbeddings()
        # self.docsearch = FAISS.from_texts(self.texts_list, self.embeddings)
        self.get_docsearch()
        self.chain = None
        self.answers = "No encuentro una respuesta a tu pregunta."
        self.total_tokens = 0

    def get_chain(self, 
                  _model_name="text-davinci-003", 
                  _api_key=API_KEY, 
                  _max_tokens=1000, 
                  _temperature=0.5) -> None:
        
        result = OpenAI(
            model_name=_model_name,
            api_key=_api_key,
            max_tokens=_max_tokens,
            temperature=_temperature,
        )
        self.chain = load_qa_chain(result, chain_type="stuff")

    def get_docsearch(self):
        # self.docsearch = FAISS.from_texts(self.texts_list, self.embeddings)
        # return self.docsearch
        with open(self.json_texts_list_path, 'rb') as f:
            self.docsearch = pickle.load(f)
            f.close()
    
    def detect_language(self, _text):
        try:
            return detect(_text)
        except:
            return False
        
        # return self.docsearch
    def chat_pdf_bot(self, _question):
        context = "Eres un asistente virtual, debes responder las preguntas en español"
        results = self.docsearch.similarity_search(_question)
        conversation = _question
        try:
            self.get_chain(#_model_name="gpt-3.5-turbo",
                           _max_tokens=2000,
                           _temperature=0.3)
            resp = self.chain.run(input_documents=results, 
                                  question=_question,
                                  context=context)
            idiom = self.detect_language(resp)
            print(idiom)
            if resp and idiom != "en":
                self.answers = resp
            # self.answers = resp
            conversation = resp + _question
            self.total_tokens = get_num_tokens(conversation)

        except Exception as e:
            print(str(e))
            self.total_tokens = get_num_tokens(conversation)
        
        print("Total tokens: ", self.total_tokens)
