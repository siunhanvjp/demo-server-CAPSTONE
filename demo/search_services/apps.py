from django.apps import AppConfig
from sentence_transformers import SentenceTransformer
from .els_services.utils import NestedSetModel, hierarchical_data

class SearchServicesConfig(AppConfig):
    
    crime_terms = {'lây_lan dịch_bệnh', 'đe dọa giết người', 'đào_ngũ', 'trốn đi nước_ngoài', 'cướp', 'lây_truyền HIV', 'tội_phạm chức_vụ',
                   'sử_dụng ma túy', 'cướp_giật', 'ngược_đãi tù_binh', 'giam người trái pháp_luật', 'làm nhục', 'cản_trở đồng_đội', 'hình_sự',
                   'vô_ý gây thiệt_hại', 'hành_hạ', 'an_ninh quốc_gia', 'xâm_phạm hôn_nhân gia_đình', 'phá_hoại chính_sách', 'lừa_đảo',
                   'tổ_chức tảo_hôn', 'chiếm_đoạt người', 'chiếm_giữ trái_phép', 'xâm_phạm bí_mật', 'mua_bán người', 'trộm_cắp', 'tham_nhũng',
                   'gián_điệp', 'xâm_phạm con_người', 'cưỡng_ép kết_hôn', 'chống mệnh_lệnh', 'xúi_giục tự_sát', 'báo_cáo sai', 'khủng_bố',
                   'sai_lệch kết_quả bầu_cử', 'cố_ý gây thương_tích', 'xâm_phạm nhân_phẩm', 'xâm_phạm tính_mạng', 'vứt bỏ con', 'giết người',
                   'sa_thải trái pháp_luật', 'sai_lệch hồ_sơ', 'vu khống', 'cố_ý làm hư_hỏng', 'lạm_quyền', 'hối_lộ', 'xâm_phạm sức khỏe',
                   'gây ô_nhiễm', 'tội_phạm ma túy', 'hủy_hoại thủy_sản', 'xâm_phạm chỗ ở', 'bức tử', 'loạn luân', 'giới_hạn phòng_vệ', 'tham_ô',
                   'sử_dụng trái_phép', 'tàng_trữ ma túy', 'phản_bội Tổ_Quốc', 'nhục hình', 'vô_ý làm chết người', 'vận_chuyển ma túy', 'đảo nhiệm',
                   'ngược_đãi gia_đình', 'cưỡng_dâm', 'chất_thải nguy_hại', 'mua_bán ma túy', 'sản_xuất ma túy', 'lật_đổ chính_quyền', 'xâm_phạm quyền tự_do',
                   'đầu_hàng địch', 'hiếp_dâm', 'tội_phạm môi_trường', 'xâm_phạm sở_hữu', 'tống tiền', 'che_giấu tội_phạm', 'hủy_hoại rừng', 'bức cung',
                   'tội_phạm quân_đội', 'tội_phạm tư_pháp', 'cưỡng_đoạt'}
    
    legal_onto = NestedSetModel()
    legal_onto.convert_to_nested_set(hierarchical_data)
    

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search_services'
    model_embedding = SentenceTransformer('VoVanPhuc/sup-SimCSE-VietNamese-phobert-base')
    def ready(self):
        from elasticsearch import Elasticsearch
        from elasticsearch_dsl import connections

        # Initialize Elasticsearch client
        ELASTIC_PASSWORD = "OxN4F5Bwg1O7ZAtLXc5V"
        
        print("called")
        # Set the connection alias for Elasticsearch DSL
        connections.create_connection(alias='default', hosts=["http://localhost:9200"], basic_auth=("elastic", ELASTIC_PASSWORD))
        
        global_es_client = connections.get_connection(alias='default')