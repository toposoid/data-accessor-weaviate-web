
'''
  Copyright 2021 Linked Ideal LLC.[https://linked-ideal.com/]
 
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
 
      http://www.apache.org/licenses/LICENSE-2.0
 
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
 '''

import weaviate
import os
import uuid
from model import FeatureVectorForUpdate, FeatureVectorIdentifier
from logging import config
config.fileConfig('logging.conf')
import logging
import time
LOG = logging.getLogger(__name__)


class WeaviateAccessor():
    client = None

    
    def __init__(self) :
        self.client = weaviate.Client("http://" + os.environ["TOPOSOID_WEAVIATE_HOST"] + ":" + os.environ["TOPOSOID_WEAVIATE_PORT"])


    def generateUuid(self, class_name: str, identifier: str,
                    test: str = 'teststrong') -> str:
        """ Generate a uuid based on an identifier
        :param identifier: characters used to generate the uuid
        :type identifier: str, required
        :param class_name: classname of the object to create a uuid for
        :type class_name: str, required
        """
        test = 'overwritten'
        id = uuid.uuid5(uuid.NAMESPACE_DNS, class_name + identifier)
        return str(id)


    def createSchema(self):
        self.client.schema.delete_all()
        class_obj = {
            "class": "SentenceFeature",
            "vectorizer": "none", # we are providing the vectors ourselves through our SBERT model, so this field is none
            "properties": [
                {
                    "name": "propositionId",
                    "dataType": ["text"],            
                },
                {
                    "name": "featureId",
                    "dataType": ["text"],            
                },
                {
                    "name": "sentenceType",
                    "dataType": ["int"],            
                },
                {
                    "name": "lang",
                    "dataType": ["text"],            
                },
            ]
        }
        self.client.schema.create_class(class_obj)
    

    def insert(self, featureVectorForUpdate: FeatureVectorForUpdate):
        featureVectorIdentifier = featureVectorForUpdate.featureVectorIdentifier
        data_obj = {
            "propositionId": featureVectorIdentifier.propositionId,
            "featureId": featureVectorIdentifier.featureId,
            "sentenceType": featureVectorIdentifier.sentenceType,
            "lang": featureVectorIdentifier.lang
        }
        identifer = featureVectorIdentifier.featureId
        self.client.data_object.create(
            data_obj,
            "SentenceFeature",
            self.generateUuid("SentenceFeature", identifer),            
            vector = featureVectorForUpdate.vector,
        )
        
    
    def upsert(self, featureVectorForUpdate: FeatureVectorForUpdate):
        featureVectorIdentifier = featureVectorForUpdate.featureVectorIdentifier
        identifer = featureVectorIdentifier.featureId
        self.client.data_object.update(
            uuid=self.generateUuid("SentenceFeature", identifer),            
            class_name='SentenceFeature',
            data_object={
                "propositionId": featureVectorIdentifier.propositionId,
                "featureId": featureVectorIdentifier.featureId,
                "sentenceType": featureVectorIdentifier.sentenceType,
                "lang": featureVectorIdentifier.lang
            },
            vector=featureVectorForUpdate.vector,
        )

    def search(self, vector, num=20):
        nearVector = {"vector": vector}
        res = self.client.query.get("SentenceFeature", ["propositionId", "featureId", "sentenceType", "lang", "_additional {certainty}"]).with_limit(num).with_near_vector(nearVector).do()
        if len(res["data"]['Get']['SentenceFeature']) == 0:
            return [],[]
        else:
            ids = []
            similarities = []
            for result in res["data"]['Get']['SentenceFeature']:  
                similarity  = result['_additional']['certainty']
                if similarity > float(os.environ["TOPOSOID_WEAVIATE_SIMILARITY_THRESHOLD"]) :                  
                    ids.append(FeatureVectorIdentifier(propositionId = result['propositionId'], featureId = result['featureId'], sentenceType = result['sentenceType'], lang = result['lang']))
                    similarities.append(similarity)
            return ids, similarities
    
    '''
    def multiSearch(self, vectors, num=20):
        ids = []
        similarities = []

        for vec in vectors:
            ids2, similarities2 = self.search(vec.vector, num)            
            ids += ids2                
            similarities += similarities2
        return ids, similarities
    '''

    def searchById(self, featureVectorIdentifier: FeatureVectorIdentifier):
        #identifer = featureVectorIdentifier.propositionId + featureVectorIdentifier.featureId +str(featureVectorIdentifier.sentenceType) + featureVectorIdentifier.lang
        identifer = featureVectorIdentifier.featureId
        rawQuery = '''
                    {
                        Get{
                            SentenceFeature(where: {
                                path: ["id"],
                                operator: ContainsAny,
                                valueText: ["%s"]
                            }){
                            propositionId,
                            featureId,
                            sentenceType,
                            lang
                            }
                        }
                    }
                    '''
        res = self.client.query.raw(rawQuery % (self.generateUuid("SentenceFeature", identifer)))
        if len(res["data"]['Get']['SentenceFeature']) == 0:
            return [], []
        else:
            return [featureVectorIdentifier], [1.0]


    def delete(self, featureVectorIdentifier: FeatureVectorIdentifier):         
        i = 0
        while(len(self.searchById(featureVectorIdentifier)[0]) > 0):
            #identifer = featureVectorIdentifier.propositionId + featureVectorIdentifier.featureId +str(featureVectorIdentifier.sentenceType) + featureVectorIdentifier.lang
            try:
                identifer = featureVectorIdentifier.featureId
                self.client.data_object.delete(self.generateUuid("SentenceFeature", identifer), "SentenceFeature",consistency_level="ONE")
            except Exception as e:
                LOG.error(e)
                pass        
            time.sleep(3)               
            if i > 3:
                break
            i += 1

