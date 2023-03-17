import deepl
import googletrans
from os import getenv
from dotenv import load_dotenv
from google.cloud import translate
load_dotenv()

TRANSLATOR = getenv('TRANSLATOR', 'google_web')
DEEPL_AUTH_KEY = getenv('DEEPL_AUTH_KEY')
GOOGLE_PROJECT_ID = getenv('GOOGLE_PROJECT_ID')

class Translator:
    def __init__(self, text="Hello, world!",source="en",target="ja"):
        self.mode = TRANSLATOR
        self.text = text
        self.source = source
        self.target = target
        self.interpreter = None
        self.google_project_id=GOOGLE_PROJECT_ID
        self.deepl_auth_key=DEEPL_AUTH_KEY

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target
    
    def get_text(self):
        return self.text

    def get_mode(self):
        return self.mode

    def set_text(self, text):
        self.text = text

    def set_source(self, source):
        self.source = source
    
    def set_target(self, target):
        self.target = target
    
    def set_mode(self, mode):
        self.mode = mode

    def translate(self):
        match self.mode:
            case "deepl":
                if self.interpreter is None:
                    self.interpreter = deepl.Translator(self.deepl_auth_key)
                return self.translate_deepl()

            case "google_web":
                if self.interpreter is None:
                    self.interpreter = googletrans.Translator()
                return self.translate_google_web()

            case "google_api":
                return self.translate_google_api(project_id=self.google_project_id)
            case _:
                print("TRANSLATOR ENV is incorrect")
                return False

    def translate_deepl(self):
        resp_txt = self.interpreter.translate_text(self.text, source_lang=self.source, target_lang=self.target)
        return resp_txt
    
    def translate_google_web(self):
        resp_txt = self.interpreter.translate(self.text,src=self.source, dest=self.target).text
        return resp_txt

    def translate_google_api(self,project_id="project_id"):

        client = translate.TranslationServiceClient()
        location = "global"
        parent = f"projects/{project_id}/locations/{location}"
        
        response = client.translate_text(
            parent= parent,
            contents= [self.text],
            mime_type= "text/plain",
            source_language_code= self.source,
            target_language_code= self.target,
        )

        for translation in response.translations:
            return translation.translated_text