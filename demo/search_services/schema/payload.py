from ninja import Schema
from typing import List, Dict
from ninja.files import UploadedFile
from ninja import File

class OCRRequest(Schema):
    file: UploadedFile = File(...)
    
    
    

class SearchRequest(Schema):

    
    original_query: str
    
    broader: Dict[str, List[str]]
    narrower: Dict[str, List[str]]
    related: Dict[str, List[str]]
    
    metadata: str
    
    method: str
    domain: str = None
    search_scope: str =  None