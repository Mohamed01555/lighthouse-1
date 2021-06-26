from elasticsearch import Elasticsearch, RequestError
from deepface.basemodels import Facenet
from deepface.commons import functions

class Search:
    def __init__(self):
        
        self.es = Elasticsearch([{'host':'localhost', 'port':'9200'}])

        mapping = {"mappings": {"properties": {"title_vector":
                  {"type": "dense_vector","dims": 128},"title_name": {"type": "keyword"}}}}
        
        try:
            self.es.indices.create(index="final_face_recognition", body=mapping)
            
        except RequestError:
            print('Index already exists!!')
        
    def add_emb_to_idx(self, emb, index, image_name=None):
        doc = {"title_vector": emb, "title_name": image_name}
        self.es.create("final_face_recognition", id=index, body=doc)
        
    def delete_emb_from_index(self, index):
        self.es.delete(index="final_face_recognition",id=index)
        
    def search(self, emb, size):
        '''
        size : # nearest neighbours
        '''
        query = {
                "size": size,  #foe ex 5 nearest neighbours
                "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": "cosineSimilarity(params.queryVector, 'title_vector')+1",
                        #"source": "1 / (1 + l2norm(params.queryVector, 'title_vector'))", #euclidean distance
                        "params": {
                            "queryVector": list(emb)
                        }
                    }
                }
                }}
        
        res = self.es.search(index="final_face_recognition", body=query)
        return res
        
class Model:
    global model
    model = Facenet.loadModel()
    def __init__(self):
        self.target_size = (160, 160)
        self.embedding_size = 128
            
    def get_embedding(self, image):
        '''Takes an image with only the desired face'''
        try :
            preprocessed_face = functions.preprocess_face(image, target_size = self.target_size, detector_backend='mtcnn')
            return model.predict(preprocessed_face)[0]
        
        except ValueError:
            print('Please take another photo such that the desired person is more obvious')

