import re

class ThongTuTemplate:
    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.so_vb_re = re.compile(r'\b(\d{2,3}/\d{4}/\S+)')
        self.date_re = re.compile(r'ngày (\d{1,2}) tháng (\d{1,2}) năm (\d{4})')
        self.don_vi_bh_re =  re.compile(r'(?<=\b)[^\n]+(?=\s*C[ỘOÒO]NG)', re.IGNORECASE)
        self.loai_vb = "THÔNG TƯ"
        
    def _find_nd_vb(self):
        try:
            pattern = re.compile(fr'{self.loai_vb}(.*?)(?=[Cc][ăâắằấầậẩẫ]n [Cc][ứỨựửữ]|_)', re.DOTALL)
            matches = pattern.findall(self.raw_text)
            if matches:
                # Split the string into words
                words = matches[0].split()

                # Join the words with a single space
                cleaned_string = ' '.join(words)
                return cleaned_string
            else:
                return None
        except:
            return None
        
    def handle_error(self, item, pos, return_type=None):
        if return_type == "list":
            try:
                return item[pos:]
            except:
                return None 
        
        if return_type == "date":
            try:
                return f"{item[pos][0]}/{item[pos][1]}/{item[pos][2]}"
            except:
                return None
        try:
            return item[pos]
        except:
            return None
        
    def extract_metadata(self):
        so_vb = self.so_vb_re.findall(self.raw_text)
        date = self.date_re.findall(self.raw_text)
        don_vi_bh = self.don_vi_bh_re.findall(self.raw_text)
        nd_vb = self._find_nd_vb()
        
        return [
            {"Cơ quan ban hành": f"{self.handle_error(don_vi_bh, 0)}"},
            {"Số hiệu": f"{self.handle_error(so_vb, 0)}"},
            {"Loại văn bản": f"{self.loai_vb}"},
            {"Ngày ban hành": f"{self.handle_error(date, 0, 'date')}"},
            {"title": f"{nd_vb}"},
            {"Văn bản liên quan": f"{self.handle_error(so_vb, 1, 'list')}"}
        ]

        
class QuyetDinhTemplate(ThongTuTemplate):
    def __init__(self, raw_text):
        super().__init__(raw_text)
        self.loai_vb = "QUYẾT ĐỊNH"