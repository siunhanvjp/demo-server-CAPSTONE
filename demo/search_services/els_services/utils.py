import time
from underthesea import word_tokenize

class NestedSetModel:
    def __init__(self):
        # Initialize the tree structure and index variables
        self.tree = []
        self.left_index = 1
        self.right_index = 2

    def convert_to_nested_set(self, hierarchy):
        # Reset tree and index variables before converting
        self.tree = []
        self.left_index = 1
        self.right_index = 2
        # Build the nested set model recursively
        self._build_nested_set(hierarchy)
        return self.tree

    def _build_nested_set(self, hierarchy, depth=0):
        # Recursively traverse the hierarchy and build the nested set
        for child_id, child_data in hierarchy.items():
            parent_index = len(self.tree)
            
            self.tree.append({
                'id': word_tokenize(child_id, format="text"),
                'left': self.left_index,
                'right': None,
                'depth': depth,
            })
            
            self.left_index += 1
            # Recursively call for children
            self._build_nested_set(child_data, depth + 1)
            # Update the right index after processing children
            self.tree[parent_index]['right'] = self.left_index
            self.left_index += 1

    def get_parent_child_relationships(self):
        # Create a dictionary to store parent-child relationships
        relationships = {}
        for node in self.tree:
            # Determine the parent of each node
            parent_id = None if node['depth'] == 0 else self._find_parent(node)
            relationships[node['id']] = parent_id
        return relationships

    def _find_parent(self, node):
        # Find the parent of a node by checking left and right indexes
        for parent_node in reversed(self.tree[:self.tree.index(node)]):
            if parent_node['depth'] == node['depth'] - 1 and parent_node['left'] < node['left'] and parent_node['right'] > node['right']:
                return parent_node['id']
        return None
    
    def find_parent(self, node_id):
        # Find and return the parent of a node with the given ID
        node_index = next((index for index, node in enumerate(self.tree) if node['id'] == node_id), None)
        if node_index is not None and self.tree[node_index]['depth'] > 0:
            node_depth = self.tree[node_index]['depth']
            node_left = self.tree[node_index]['left']
            node_right = self.tree[node_index]['right']
            return [next((node['id'].replace('_', ' ') for node in self.tree if node['depth'] == node_depth - 1 and node['left'] < node_left < node['right']), None)]
        return []
    
    def find_children(self, node_id):
        # Find and return the immediate children of a node with the given ID on the next depth level
        node_index = next((index for index, node in enumerate(self.tree) if node['id'] == node_id), None)
        if node_index is not None:
            node_depth = self.tree[node_index]['depth']
            node_left = self.tree[node_index]['left']
            node_right = self.tree[node_index]['right']
            return [node['id'].replace('_', ' ') for node in self.tree if node['depth'] == node_depth + 1 and node_left < node['left'] < node_right]
        return []

    def find_relevant_nodes(self, node_id):
        # Find and return nodes at the same depth with the same parent as the node with the given ID
        node_index = next((index for index, node in enumerate(self.tree) if node['id'] == node_id), None)
        if node_index is not None:
            node_depth = self.tree[node_index]['depth']
            node_parent_id = self._find_parent(self.tree[node_index])
            return [node['id'].replace('_', ' ') for node in self.tree if node['depth'] == node_depth and self._find_parent(node) == node_parent_id and node['id'] != node_id]
        return []
    

def measure_performance(hierarchy):
    start_time = time.time()
    
    nested_set_model = NestedSetModel()
    # Convert hierarchical data to nested set model
    nested_set_model.convert_to_nested_set(hierarchy)
    # Retrieve parent-child relationships
    parent_child_relationships = nested_set_model.get_parent_child_relationships()
    
    father_nodes = nested_set_model.find_parent("xâm_phạm tính_mạng")
    relevant_nodes = nested_set_model.find_relevant_nodes("xâm_phạm tính_mạng")
    child_nodes = nested_set_model.find_children("xâm_phạm tính_mạng")
    end_time = time.time()
    execution_time = end_time - start_time

    # Display results and performance metrics
    print("Nested Set Model:", nested_set_model.tree)
    print("Parent-Child Relationships:", parent_child_relationships)
    print("################################")
    print("find_parent:", father_nodes)
    print("find_children:", child_nodes)
    print("find_nodes_same_depth_same_parent Relationships:", relevant_nodes)
    print("Execution Time: {:.6f} seconds".format(execution_time))

# Example data:
hierarchical_data = {
    'hình sự': {
        'xâm phạm con người': {
            'xâm phạm nhân phẩm':{
                'vu khống':{},
                'làm nhục':{},
                },
            'xâm phạm quyền tự do':{
                'mua bán người':{},
                'chiếm đoạt người':{},
                'giam người trái pháp luật':{},
                'xâm phạm chỗ ở':{},
                'xâm phạm bí mật':{},
                'sa thải trái pháp luật':{},
                'sai lệch kết quả bầu cử':{},
                },
            'xâm phạm tính mạng':{
                'giết người':{},
                'giới hạn phòng vệ':{},
                'vứt bỏ con':{},
                'vô ý làm chết người':{},
                'bức tử':{},
                'xúi giục tự sát':{},
                'đe dọa giết người':{},
                },
            'xâm phạm sức khỏe':{
                'cố ý gây thương tích':{},
                'hành hạ':{},
                'hiếp dâm':{},
                'cưỡng dâm':{},
                'lây truyền HIV':{},
                'xúi giục tự sát':{},
                'đe dọa giết người':{},
                }
            },
        'tội phạm quân đội': {
            'chống mệnh lệnh':{},
            'đầu hàng địch':{},
            'cản trở đồng đội':{},
            'báo cáo sai':{},
            'đào ngũ':{},
            'ngược đãi tù binh':{},
            },
        'tội phạm chức vụ':{
            'tham nhũng':{},
            'tham ô':{},
            'hối lộ':{},
            'lạm quyền':{},
            'đảo nhiệm':{},
            },
        'xâm phạm sở hữu':{
            'cướp':{},
            'tống tiền':{},
            'cưỡng đoạt':{},
            'cướp giật':{},
            'trộm cắp':{},
            'lừa đảo':{},
            'chiếm giữ trái phép':{},
            'sử dụng trái phép':{},
            'cố ý làm hư hỏng':{},
            'vô ý gây thiệt hại':{},
            },
        'tội phạm ma túy':{
            'sản xuất ma túy':{},
            'tàng trữ ma túy':{},
            'vận chuyển ma túy':{},
            'mua bán ma túy':{},
            'sử dụng ma túy':{},
            },
        'an ninh quốc gia':{
            'phản bội Tổ Quốc':{},
            'lật đổ chính quyền':{},
            'gián điệp':{},
            'khủng bố':{},
            'phá hoại chính sách':{},
            'trốn đi nước ngoài':{},
            },
        'tội phạm tư pháp':{
            'nhục hình':{},
            'bức cung':{},
            'sai lệch hồ sơ':{},
            'che giấu tội phạm':{},
            },
        'xâm phạm hôn nhân gia đình':{
            'cưỡng ép kết hôn':{},
            'tổ chức tảo hôn':{},
            'loạn luân':{},
            'ngược đãi gia đình':{},
            },
        'tội phạm môi trường':{
            'gây ô nhiễm':{},
            'chất thải nguy hại':{},
            'lây lan dịch bệnh':{},
            'hủy hoại thủy sản':{},
            'hủy hoại rừng':{},
            },
    }
}

#measure_performance(hierarchical_data)

#['hình sự', 'xâm phạm con người', 'xâm phạm nhân phẩm', 'vu khống', 'làm nhục', 'xâm phạm quyền tự do', 'mua bán người', 'chiếm đoạt người', 'giam người trái pháp luật', 'xâm phạm chỗ ở', 'xâm phạm bí mật', 'sa thải trái pháp luật', 'sai lệch kết quả bầu cử', 'xâm phạm tính mạng', 'giết người', 'giới hạn phòng vệ', 'vứt bỏ con', 'vô ý làm chết người', 'bức tử', 'xúi giục tự sát', 'đe dọa giết người', 'xâm phạm sức khỏe', 'cố ý gây thương tích', 'hành hạ', 'hiếp dâm', 'cưỡng dâm', 'lây truyền HIV', 'xúi giục tự sát', 'đe dọa giết người', 'tội phạm quân đội', 'chống mệnh lệnh', 'đầu hàng địch', 'cản trở đồng đội', 'báo cáo sai', 'đào ngũ', 'ngược đãi tù binh', 'tội phạm chức vụ', 'tham nhũng', 'tham ô', 'hối lộ', 'lạm quyền', 'đảo nhiệm', 'xâm phạm sở hữu', 'cướp', 'tống tiền', 'cưỡng đoạt', 'cướp giật', 'trộm cắp', 'lừa đảo', 'chiếm giữ trái phép', 'sử dụng trái phép', 'cố ý làm hư hỏng', 'vô ý gây thiệt hại', 'tội phạm ma túy', 'sản xuất ma túy', 'tàng trữ ma túy', 'vận chuyển ma túy', 'mua bán ma túy', 'sử dụng ma túy', 'an ninh quốc gia', 'phản bội Tổ Quốc', 'lật đổ chính quyền', 'gián điệp', 'khủng bố', 'phá hoại chính sách', 'trốn đi nước ngoài', 'tội phạm tư pháp', 'nhục hình', 'bức cung', 'sai lệch hồ sơ', 'che giấu tội phạm', 'xâm phạm hôn nhân gia đình', 'cưỡng ép kết hôn', 'tổ chức tảo hôn', 'loạn luân', 'ngược đãi gia đình', 'tội phạm môi trường', 'gây ô nhiễm', 'chất thải nguy hại', 'lây lan dịch bệnh', 'hủy hoại thủy sản', 'hủy hoại rừng']

# Given list of terms
# crime_terms = {'hình sự', 'xâm phạm con người', 'xâm phạm nhân phẩm', 'vu khống', 'làm nhục', 'xâm phạm quyền tự do', 'mua bán người', 'chiếm đoạt người', 'giam người trái pháp luật', 'xâm phạm chỗ ở', 'xâm phạm bí mật', 'sa thải trái pháp luật', 'sai lệch kết quả bầu cử', 'xâm phạm tính mạng', 'giết người', 'giới hạn phòng vệ', 'vứt bỏ con', 'vô ý làm chết người', 'bức tử', 'xúi giục tự sát', 'đe dọa giết người', 'xâm phạm sức khỏe', 'cố ý gây thương tích', 'hành hạ', 'hiếp dâm', 'cưỡng dâm', 'lây truyền HIV', 'xúi giục tự sát', 'đe dọa giết người', 'tội phạm quân đội', 'chống mệnh lệnh', 'đầu hàng địch', 'cản trở đồng đội', 'báo cáo sai', 'đào ngũ', 'ngược đãi tù binh', 'tội phạm chức vụ', 'tham nhũng', 'tham ô', 'hối lộ', 'lạm quyền', 'đảo nhiệm', 'xâm phạm sở hữu', 'cướp', 'tống tiền', 'cưỡng đoạt', 'cướp giật', 'trộm cắp', 'lừa đảo', 'chiếm giữ trái phép', 'sử dụng trái phép', 'cố ý làm hư hỏng', 'vô ý gây thiệt hại', 'tội phạm ma túy', 'sản xuất ma túy', 'tàng trữ ma túy', 'vận chuyển ma túy', 'mua bán ma túy', 'sử dụng ma túy', 'an ninh quốc gia', 'phản bội Tổ Quốc', 'lật đổ chính quyền', 'gián điệp', 'khủng bố', 'phá hoại chính sách', 'trốn đi nước ngoài', 'tội phạm tư pháp', 'nhục hình', 'bức cung', 'sai lệch hồ sơ', 'che giấu tội phạm', 'xâm phạm hôn nhân gia đình', 'cưỡng ép kết hôn', 'tổ chức tảo hôn', 'loạn luân', 'ngược đãi gia đình', 'tội phạm môi trường', 'gây ô nhiễm', 'chất thải nguy hại', 'lây lan dịch bệnh', 'hủy hoại thủy sản', 'hủy hoại rừng'}
# # Lambda function to tokenize a given term
# tokenize_term = lambda term: word_tokenize(term, format="text")

# Apply the lambda function to each term in the list
# tokenized_terms = list(map(tokenize_term, crime_terms))
# User query
# start_time = time.time()
# user_query = word_tokenize("phạm nhân hình sự vi phạm tội xâm phạm nhân phẩm, có hành vi khủng bố", format="text")

# # Check for matching terms
# matching_terms = [term for term in tokenized_terms if term in user_query]
# end_time = time.time()

# # Print the matching terms
# if matching_terms:
#     print("Matching terms found:", matching_terms)
# else:
#     print("No matching terms found.")
# execution_time = end_time - start_time
# print("Execution Time: {:.6f} seconds".format(execution_time))
# print(tokenized_terms)

