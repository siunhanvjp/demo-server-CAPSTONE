from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Index, analyzer, Q, SF
import json
from search_services.apps import SearchServicesConfig
from underthesea import word_tokenize
from typing import Dict, List

# print(client.synonyms.get_synonym(id="test-synonyms-set"))

class QueryHandler:
    
    def __init__(self, payload):
        self.search_query = payload.original_query
        self.method = payload.method
        
        self.metadata = json.loads(payload.metadata)
        self.index_name = 'demo_index'
        
        self.keywords = self._combine_keywords(payload.broader, payload.related, payload.narrower)
        
        if payload.domain == "legal":
            self.terms = SearchServicesConfig.crime_terms
            self.ontology = SearchServicesConfig.legal_onto
        else:
            self.terms, self.ontology = None, None
            
    def _combine_keywords(self,dict1: Dict[str, List[str]], dict2: Dict[str, List[str]], dict3: Dict[str, List[str]]) -> Dict[str, List[str]]:
        combined_dict: Dict[str, List[str]] = {}

        # Combine values for each key
        for key in set(dict1.keys()).union(dict2.keys(), dict3.keys()):
            values = dict1.get(key, []) + dict2.get(key, []) + dict3.get(key, [])
            combined_dict[key] = values

        return combined_dict
        
    def _pretty_results(self, response):
        results = []

        for hit in response:
            
            doc = {"score": hit.meta.score, "metadata": []}
            
            
            id = hit.meta.id
            print(id)
            source = hit.to_dict()

            # Include all key-value pairs from the source
            for key, value in source.items():
                if key=="vector" or key == "title_vector":
                    continue
                if self.method=="semantic":
                    if key=="title":
                        doc["file_name"] = value
                if key=="filename":
                    doc["file_name"] = value
                else:
                    doc["metadata"].append({key: str(value)})
            results.append(doc)
        return results[:10]
    
    def _refine_query(self):
        refined_query = self.search_query
        
        for key, values in self.keywords.items():
            combined_values = ' OR '.join(values)
            refined_query = refined_query.replace(key, f"({key} OR {combined_values})")
            # combined_values = '"' + '" OR "'.join(values) + '"'
            # refined_query = refined_query.replace(key, f"(\"{key}\" OR {combined_values})")

        return refined_query
        
    def analyze_keywords(self):
        keywords_dict = {
            "broader":{},
            "related":{},
            "narrower": {}
        }
        
        if self.ontology is None:
            return keywords_dict
        
        tokenized_q = word_tokenize(self.search_query, format="text")
        
        found_keywords = [term for term in self.terms if term in tokenized_q]
        
        for keyword in found_keywords:
            keywords_dict["broader"][keyword.replace("_", " ")] = self.ontology.find_parent(keyword)
            keywords_dict["related"][keyword.replace("_", " ")] = self.ontology.find_relevant_nodes(keyword)
            keywords_dict["narrower"][keyword.replace("_", " ")] = self.ontology.find_children(keyword)
        
        
        print(keywords_dict)
        
        return keywords_dict
    
    @staticmethod
    def _build_filter_query(metadata_conditions): #return a list of terms
        # query = Q()
        query = list()
        for condition in metadata_conditions:
            if "$and" in condition:
                and_query = Q("bool", must=QueryHandler._build_filter_query(condition["$and"]))
                query.append(and_query)
            elif "$or" in condition:
                or_query = Q("bool", should=QueryHandler._build_filter_query(condition["$or"]), minimum_should_match=1)
                query.append(or_query)
            else:
                key = condition["key"]
                value = condition["value"]
                term_query = Q("match_phrase", **{key: value})
                query.append(term_query)

        return query
    
    def search_documents(self):
        search_obj = Search(index=self.index_name)
        filter_query = QueryHandler._build_filter_query(self.metadata)
        
        if self.method == "filename":
            search_query = Q('match_phrase', filename=self.search_query)
        elif self.method == "fulltext":
            if self.ontology is None:
                search_query = Q('multi_match', query=self.search_query, fields=[])
            else:
                refined_query = self._refine_query()
                search_query =Q('query_string', query=refined_query)
        elif self.method == "semantic":
            search_obj = Search(index="demo_simcse_colab")
            model_embedding = SearchServicesConfig.model_embedding
            query_vector = model_embedding.encode([word_tokenize(self.search_query, format="text")]).tolist()[0]
            search_query = Q(
                                "function_score", 
                                query=Q("match_all"),
                                functions=[
                                        SF("script_score", script={
                                            "source": "cosineSimilarity(params.query_vector, 'title_vector') + 1.0",
                                            "params": {"query_vector": query_vector}
                                        })
                                    ]
                            )
        if self.search_query:
            combined_query = Q('bool', must=[search_query], filter=filter_query)
        else:
            combined_query = Q('bool', filter=filter_query)
        print(combined_query.to_dict())
        query = search_obj.query(combined_query)
        response = query.execute()
        print(self._pretty_results(response))
        return self._pretty_results(response)
            
def pretty_response(response):
    result_string = f"Number of results: {len(response)}\n"
    if not response:
        result_string = 'Your search returned no results.'
    else:
        for hit in response:
            id = hit.meta.id
            score = hit.meta.score
            source = hit.to_dict()

            pretty_output = f"\nIndex: {hit.meta.index}\nID: {id}\nScore: {score}"

            # Include all key-value pairs from the source
            for key, value in source.items():
                if key=="title_vector":
                    continue
                pretty_output += f"\n{key.capitalize()}: {value}"

            result_string += pretty_output + '\n'
    return result_string
        
def build_filter_query(metadata_conditions):
    query = Q()

    for condition in metadata_conditions:
        if "$and" in condition:
            and_query = Q("bool", must=[build_filter_query(condition["$and"])])
            query &= and_query
        elif "$or" in condition:
            or_query = Q("bool", should=[build_filter_query(condition["$or"])], minimum_should_match=1)
            query &= or_query
        else:
            key = condition["key"]
            value = condition["value"]
            term_query = Q("term", **{key: value})
            query &= term_query

    return query


