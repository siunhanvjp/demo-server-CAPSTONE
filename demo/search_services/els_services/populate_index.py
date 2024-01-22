from elasticsearch_dsl import Document, Index, Text, analyzer, connections, DenseVector, Keyword
from elasticsearch.helpers import bulk
import pandas as pd
import os
import random
from elasticsearch import Elasticsearch
# Initialize Elasticsearch client
ELASTIC_PASSWORD = "OxN4F5Bwg1O7ZAtLXc5V"
# test-synonyms-set
print("called")
# Set the connection alias for Elasticsearch DSL
connections.create_connection(alias='default', hosts=["http://localhost:9200"], basic_auth=("elastic", ELASTIC_PASSWORD))


# Define your document type with mappings
class LegalDocument(Document):
    id = Keyword()
    content  = Text(analyzer='my_custom_index_analyzer',search_analyzer='my_custom_search_analyzer')
    filename  = Text(analyzer='my_custom_index_analyzer',search_analyzer='my_custom_search_analyzer',fields={'keyword': Keyword(ignore_above=256)})
    vector = DenseVector(dims=768, index=True, similarity='cosine')

    class Index:
        name = 'demo_index'
        settings = {
            'analysis': {
                'analyzer': {
                    'my_custom_index_analyzer': {
                        'tokenizer': 'standard',
                        'filter': ['lowercase']
                    },
                    'my_custom_search_analyzer': {
                        'tokenizer': 'standard',
                        'filter': ['lowercase', 'my_synonym_filter']
                    }
                },
                'filter': {
                    'my_synonym_filter': {
                        'type': 'synonym_graph',
                        'synonyms_set': 'test-synonyms-set',
                        'updateable': True
                    }
                }
            }
        }


csv_file_path = os.path.join(os.getcwd(), 'raw.csv')  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file_path)

bulk_data = df.to_dict(orient='records')
es = Elasticsearch(['http://localhost:9200'], basic_auth=('elastic', ELASTIC_PASSWORD))
bulk(es, bulk_data, index='demo_index')