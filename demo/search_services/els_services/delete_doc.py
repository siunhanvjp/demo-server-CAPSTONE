from elasticsearch import Elasticsearch
ELASTIC_PASSWORD = "OxN4F5Bwg1O7ZAtLXc5V"
# Replace the following with your Elasticsearch server details
es = Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', ELASTIC_PASSWORD))

document_ids = [
    "zRu9_IwBA_LT_wLiz6wD",
    "5Bu9_IwBA_LT_wLiz6sC",
    "Yhu9_IwBA_LT_wLiz60D",
    "Axu9_IwBA_LT_wLiz67p",
    "ABu9_IwBA_LT_wLiy6p-"
]

# Delete documents by ID using the Delete API
for doc_id in document_ids:
    es.delete(index='demo_index', id=doc_id)