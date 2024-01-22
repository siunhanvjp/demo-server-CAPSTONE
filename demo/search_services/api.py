from ninja_extra import api_controller, http_get, http_post, http_put, http_delete
from typing import List
from ninja import UploadedFile, File
import fitz
import re
from .schema.response import SearchResult, OCRRespone
from .schema.payload import SearchRequest, OCRRequest

from .els_services.connection import QueryHandler
from .ocr_template import ThongTuTemplate, QuyetDinhTemplate
from search_services.apps import SearchServicesConfig

from underthesea import word_tokenize

@api_controller('/search', tags=["Search"])
class SearchController:
    @http_post('', response=SearchResult)
    def search_docs(self, request, payload: SearchRequest):
        
        handler = QueryHandler(payload)
        
        documents = handler.search_documents()
        
        keywords = handler.analyze_keywords()
        
        search_result = {"documents": documents}
        search_result.update(keywords)
        
        return search_result
    
    
    
@api_controller('/ocr', tags=["OCR"])
class OCRController:
    
    
    
    @http_post('', response=OCRRespone)
    def ocr_docs(self, request, template_type:str, pdf_file: UploadedFile):
        pdf_document = fitz.open(stream=pdf_file.read())
        raw_text = pdf_document[0].get_text()
        cleaned_text = re.sub(r'[_-][_-]+', '', raw_text)
        template = ThongTuTemplate(cleaned_text)
        
        print(cleaned_text, "##########" ,raw_text)
        
        if template_type == "thongtu":
            pass
        elif template_type == "quyetdinh":
            template = QuyetDinhTemplate(cleaned_text)
        elif template_type == "congvan":
            pass
        
        metadata = (template.extract_metadata())
        print(metadata)
        return {'metadata': metadata}
