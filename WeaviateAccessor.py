
'''
  Copyright (C) 2025  Linked Ideal LLC.[https://linked-ideal.com/]
 
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Affero General Public License as
  published by the Free Software Foundation, version 3.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Affero General Public License for more details.
 
  You should have received a copy of the GNU Affero General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import weaviate
from weaviate.exceptions import ObjectAlreadyExistsError
import os
import time
from ToposoidCommon.model import FeatureVectorForUpdate, FeatureVectorIdentifier, FeatureVectorSearchResult, TransversalState
import ToposoidCommon as tc
LOG = tc.LogUtils(__name__)

class WeaviateAccessor():
    client = None

    
    def __init__(self) :
        self.client = weaviate.Client("http://" + os.environ["TOPOSOID_WEAVIATE_HOST"] + ":" + os.environ["TOPOSOID_WEAVIATE_PORT"])

    def createSchema(self):
        self.client.schema.delete_all()
        class_obj = {
            "class": "ToposoidFeature",
            "vectorizer": "none", # we are providing the vectors ourselves through our SBERT model, so this field is none
            "properties": [
                {
                    "name": "superiorId",
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
                {
                    "name": "superiorType",
                    "dataType": ["int"],            
                },
                {
                    "name": "nonSentenceType",
                    "dataType": ["int"],            
                },
                {
                    "name": "caseGroupType",
                    "dataType": ["int"],            
                },                

            ]
        }
        self.client.schema.create_class(class_obj)

    def insert(self, featureVectorForUpdate: FeatureVectorForUpdate):

        if not self.client.schema.exists(class_name="ToposoidFeature"):
            self.createSchema()

        featureVectorIdentifier = featureVectorForUpdate.featureVectorIdentifier
        data_obj = {
            "superiorId": featureVectorIdentifier.superiorId,
            "featureId": featureVectorIdentifier.featureId,
            "sentenceType": featureVectorIdentifier.sentenceType,
            "lang": featureVectorIdentifier.lang,
            "superiorType": featureVectorIdentifier.superiorType, 
            "nonSentenceType": featureVectorIdentifier.nonSentenceType,
            "caseGroupType": featureVectorIdentifier.caseGroupType
        }
        identifer = featureVectorIdentifier.featureId
        #Try 5 times because ObjectAlreadyExistsError may occur with unregistered uuid
        for i in range(5):
            try:
                self.client.data_object.create(
                    data_obj,
                    "ToposoidFeature",
                    identifer,
                    vector = featureVectorForUpdate.vector,
                )
                break
            except ObjectAlreadyExistsError:
                if i > 5:
                    raise ObjectAlreadyExistsError
                else:
                    pass
                            
    def update(self, featureVectorForUpdate: FeatureVectorForUpdate):

        if not self.client.schema.exists(class_name="ToposoidFeature"):
            self.createSchema()

        featureVectorIdentifier = featureVectorForUpdate.featureVectorIdentifier
        identifer = featureVectorIdentifier.featureId
        self.client.data_object.update(
            #uuid=self.generateUuid("ToposoidFeature", identifer),            
            uuid=identifer,
            class_name='ToposoidFeature',
            data_object={
                "superiorId": featureVectorIdentifier.superiorId,
                "featureId": featureVectorIdentifier.featureId,
                "sentenceType": featureVectorIdentifier.sentenceType,
                "lang": featureVectorIdentifier.lang,
                "superiorType": featureVectorIdentifier.superiorType,
                "nonSentenceType": featureVectorIdentifier.nonSentenceType,
                "caseGroupType": featureVectorIdentifier.caseGroupType
            },
            vector=featureVectorForUpdate.vector,
        )

    def search(self, vector, num=20):
        nearVector = {"vector": vector}
        res = self.client.query.get("ToposoidFeature", ["superiorId", "featureId", "sentenceType", "lang", "superiorType", "nonSentenceType", "caseGroupType", "_additional {certainty}"]).with_limit(num).with_near_vector(nearVector).do()
        if len(res["data"]['Get']['ToposoidFeature']) == 0:
            return [],[]
        else:
            ids = []
            similarities = []
            for result in res["data"]['Get']['ToposoidFeature']:  
                similarity  = result['_additional']['certainty']
                if similarity > float(os.environ["TOPOSOID_WEAVIATE_SIMILARITY_THRESHOLD"]) :                  
                    ids.append(FeatureVectorIdentifier(superiorId = result['superiorId'], featureId = result['featureId'], sentenceType = result['sentenceType'], lang = result['lang'],  superiorType = result['superiorType'], nonSentenceType = result['nonSentenceType'], caseGroupType = result['caseGroupType']))
                    similarities.append(similarity)
            return ids, similarities

    def easySearch(self, vector, num=20, similarityThreshold=0.85):
        nearVector = {"vector": vector}
        res = self.client.query.get("ToposoidFeature", ["superiorId", "featureId", "sentenceType", "lang", "superiorType", "nonSentenceType", "caseGroupType", "_additional {certainty}"]).with_limit(num).with_near_vector(nearVector).do()
        if len(res["data"]['Get']['ToposoidFeature']) == 0:
            return [],[]
        else:
            ids = []
            similarities = []
            for result in res["data"]['Get']['ToposoidFeature']:  
                similarity  = result['_additional']['certainty']
                if similarity > similarityThreshold:                  
                    ids.append(FeatureVectorIdentifier(superiorId = result['superiorId'], featureId = result['featureId'], sentenceType = result['sentenceType'], lang = result['lang'], superiorType = result['superiorType'], nonSentenceType = result['nonSentenceType'], caseGroupType = result['caseGroupType']))
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
        #identifer = featureVectorIdentifier.superiorId + featureVectorIdentifier.featureId +str(featureVectorIdentifier.sentenceType) + featureVectorIdentifier.lang
        identifer = featureVectorIdentifier.featureId
        rawQuery = '''
                    {
                        Get{
                            ToposoidFeature(where: {
                                path: ["id"],
                                operator: ContainsAny,
                                valueText: ["%s"]
                            }){
                            superiorId,
                            featureId,
                            sentenceType,
                            lang,
                            superiorType,
                            nonSentenceType,
                            caseGroupType
                            }
                        }
                    }
                    '''
        #res = self.client.query.raw(rawQuery % (self.generateUuid("ToposoidFeature", identifer)))
        res = self.client.query.raw(rawQuery % (identifer))
        if len(res["data"]['Get']['ToposoidFeature']) == 0:
            return [], []
        else:
            return [featureVectorIdentifier], [1.0]


    def delete(self, featureVectorIdentifier: FeatureVectorIdentifier, transversalState: TransversalState):         
        i = 0
        while(len(self.searchById(featureVectorIdentifier)[0]) > 0):
            #identifer = featureVectorIdentifier.superiorId + featureVectorIdentifier.featureId +str(featureVectorIdentifier.sentenceType) + featureVectorIdentifier.lang
            try:
                identifer = featureVectorIdentifier.featureId
                #self.client.data_object.delete(self.generateUuid("ToposoidFeature", identifer), "ToposoidFeature",consistency_level="ONE")
                self.client.data_object.delete(identifer, "ToposoidFeature",consistency_level="ONE")
            except Exception as e:
                LOG.error(e, transversalState)
                pass        
            time.sleep(3)               
            if i > 3:
                break
            i += 1

    def searchBySuperiorId(self, featureVectorIdentifier: FeatureVectorIdentifier):
        #identifer = featureVectorIdentifier.superiorId + featureVectorIdentifier.featureId +str(featureVectorIdentifier.sentenceType) + featureVectorIdentifier.lang
        identifer = featureVectorIdentifier.superiorId
        rawQuery = '''
                    {
                        Get{
                            ToposoidFeature(where: {
                                path: ["superiorId"],
                                operator: ContainsAny,
                                valueText: ["%s"]
                            }){
                            superiorId,
                            featureId,
                            sentenceType,
                            lang,
                            superiorType,
                            nonSentenceType,
                            caseGroupType
                            }
                        }
                    }
                    '''
        #res = self.client.query.raw(rawQuery % (self.generateUuid("ToposoidFeature", identifer)))
        res = self.client.query.raw(rawQuery % (identifer))
        if len(res["data"]['Get']['ToposoidFeature']) == 0:
            return [], []
        else:
            ids = []
            dummySimilarities = []
            for rec in res["data"]['Get']['ToposoidFeature']:
                resFeatureVectorIdentifier = FeatureVectorIdentifier(
                    superiorId = rec["superiorId"],
                    featureId = rec["featureId"],
                    sentenceType = rec["sentenceType"],
                    lang = rec["lang"],
                    superiorType = rec["superiorType"],
                    nonSentenceType = rec["nonSentenceType"],
                    caseGroupType = rec["caseGroupType"]
                )
                ids.append(resFeatureVectorIdentifier)
                dummySimilarities.append(1.0)       
            return ids, dummySimilarities

    def deleteBySuperiorId(self, featureVectorIdentifier: FeatureVectorIdentifier, transversalState: TransversalState):         
        i = 0        
        while(len(self.searchBySuperiorId(featureVectorIdentifier)[0]) > 0):
            #identifer = featureVectorIdentifier.superiorId + featureVectorIdentifier.featureId +str(featureVectorIdentifier.sentenceType) + featureVectorIdentifier.lang
            try:
                identifer = featureVectorIdentifier.superiorId
                #self.client.data_object.delete(self.generateUuid("ToposoidFeature", identifer), "ToposoidFeature",consistency_level="ONE")
                self.client.batch.delete_objects(class_name="ToposoidFeature", where={
                            "path": ["superiorId"],
                            "operator": "Equal",
                            "valueText": identifer
                })
                #self.client.data_object.delete(identifer, "ToposoidFeature",consistency_level="ONE")
            except Exception as e:
                LOG.error(e, transversalState)
                pass        
            time.sleep(3)               
            if i > 3:
                break
            i += 1


    '''
    def generateUuid(self, class_name: str, identifier: str,
                    test: str = 'teststrong') -> str:
        """ Generate a uuid based on an identifier
        :param identifier: characters used to generate the uuid
        :type identifier: str, required
        :param class_name: classname of the object to create a uuid for
        :type class_name: str, required
        """
        test = 'overwritten'
        #id = uuid.uuid5(uuid.NAMESPACE_DNS, class_name + identifier)        
        #return str(id)
        return identifier
    '''
