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

from fastapi.testclient import TestClient
from api import app
from ToposoidCommon.model import StatusInfo, FeatureVectorSearchResult, TransversalState
import numpy as np
from time import sleep
import pytest
import uuid
from fastapi.encoders import jsonable_encoder

class TestWeaviateAPI(object):

    client = TestClient(app)
    transversalState = str(jsonable_encoder(TransversalState(userId="test-user", username="guest", roleId=0, csrfToken = "")))
    vector = list(np.random.rand(768))
    ids = {
        "test-ss1": "47ad6ccb-316f-4d68-a2f0-eb6f2a70a710", 
        "test-ms1": "523da3a7-f772-4b00-8c59-e7e27cfe77eb",
        "test-ms2": "7d771863-2fd2-47c1-8e5a-ff4a77d6e963",
        "test-ms3": "79b08eb8-4651-4203-a1e0-49bd0dbeb7da",
        "test-ms4": "26e48461-9bee-4b62-87b9-ace09ae57e80",
        "test-ms5": "d595119e-045e-49aa-ac82-fbb66e80516c",
        "test-empty": "14ccc264-51db-44e9-b331-c8118e9ca8be",
        "test1": "e947244a-b35d-4457-86cf-28b86fabb959", 
        "test-search-by-superiorid": "c666e630-5e02-11f0-b397-eaf939273568", 
        "test-bulk-delete": "d5cadd24-b9c1-411f-ac2e-ffeb3bbeb91d"                
    }

    @classmethod
    def setup_class(cls):    

        response = cls.client.post("/createSchema",
                                   headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState})
        #print(StatusInfo.parse_obj(response.json()))
        
        
        response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                        json={
                                "featureVectorIdentifier":{
                                    "superiorId": cls.ids["test-ss1"],
                                    "featureId": cls.ids["test-ss1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": cls.vector
                            }
                        )    
        #print(StatusInfo.parse_obj(response.json()))

        change3 = cls.vector[3:]
        changeVector1 = [0.1, 0.2, 0.2]        
        changeVector1[len(changeVector1):len(changeVector1)] = change3
        
        changeVector2 = [0.1, 0.9, 0.3]
        changeVector2[len(changeVector2):len(changeVector2)] = change3

        changeVector3 = [0.1, 0.2, 0.4]        
        changeVector3[len(changeVector3):len(changeVector3)] = change3

        changeVector4 = [0.11,0.22,0.39]        
        changeVector4[len(changeVector4):len(changeVector4)] = change3

        response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                        json={
                                 "featureVectorIdentifier":{
                                    "superiorId": cls.ids["test-ms1"],
                                    "featureId": cls.ids["test-ms1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": changeVector1
                            }
                        )    
        assert response.status_code == 200
        response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                        json={
                                 "featureVectorIdentifier":{
                                    "superiorId": cls.ids["test-ms2"],
                                    "featureId": cls.ids["test-ms2"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": changeVector2
                            }
                        )    
        assert response.status_code == 200
        response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                        json={
                                 "featureVectorIdentifier":{
                                    "superiorId": cls.ids["test-ms3"],
                                    "featureId": cls.ids["test-ms3"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": changeVector3
                            }
                        )    
        assert response.status_code == 200
        response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                        json={
                                 "featureVectorIdentifier":{
                                    "superiorId": cls.ids["test-ms4"],
                                    "featureId": cls.ids["test-ms4"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": changeVector3
                            }
                        )    
        assert response.status_code == 200
        response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                        json={
                                 "featureVectorIdentifier":{
                                    "superiorId": cls.ids["test-ms5"],
                                    "featureId": cls.ids["test-ms5"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": changeVector4
                            }
                        )                        
        assert response.status_code == 200
            

    def test_InsertEmptyVector(cls):    
        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                 "featureVectorIdentifier":{
                                    "superiorId": cls.ids["test-empty"],
                                    "featureId": cls.ids["test-empty"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": []
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"
        assert "new node has a vector with length 0" in statusInfo.message




    def test_InsertEmptyId(cls):    
        
        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                 "featureVectorIdentifier":{
                                    "superiorId": "",
                                    "featureId": "hoge",
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"

        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                 "featureVectorIdentifier":{
                                    "superiorId": "hoge",
                                    "featureId": "",
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"

        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                 "featureVectorIdentifier":{
                                    "superiorId": "hoge",
                                    "featureId": "hoge",
                                    "sentenceType": 3,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"

        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                 "featureVectorIdentifier":{
                                    "superiorId": "hoge",
                                    "featureId": "hoge",
                                    "sentenceType": "",
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"

        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                 "featureVectorIdentifier":{
                                    "superiorId": "hoge",
                                    "featureId": "hoge",
                                    "sentenceType": "",
                                    "lang": "",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"

        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                 "featureVectorIdentifier":{
                                    "superiorId": "hoge",
                                    "featureId": "hoge",
                                    "sentenceType": "",
                                    "lang": "fr_FR",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"



    def test_InsertAndDelete(cls):  
        
        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                 "featureVectorIdentifier":{
                                    "superiorId": cls.ids["test1"],
                                    "featureId": cls.ids["test1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "OK"
        assert "" in statusInfo.message
        
        response = cls.client.post("/delete",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                    "superiorId": cls.ids["test1"],
                                    "featureId": cls.ids["test1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0
                                })

        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "OK"
        assert "" in statusInfo.message

        response = cls.client.post("/searchById",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                    "superiorId": cls.ids["test1"],
                                    "featureId": cls.ids["test1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0
                                })                                
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert len(searchResult.ids) == 0




    def test_SingleSearch(cls):     

        response = cls.client.post("/search",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={"vector": cls.vector, "num":10})    
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert searchResult.ids[0].superiorId == cls.ids["test-ss1"]

    def test_SingleEasySearch(cls):     

        response = cls.client.post("/easySearch",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={"vector": cls.vector, "num":10, "similarityThreshold":0.5})    
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert searchResult.ids[0].superiorId == cls.ids["test-ss1"]


    def test_SingleSearchNoResponse(cls):     

        response = cls.client.post("/search",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={"vector": list(np.random.rand(768)), "num":1})    
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert len(searchResult.ids) == 0

    '''
    def test_MultiSearch(cls):     

        change3 = cls.vector[3:]
        changeVector1 = [0.1, 0.2, 0.2]        
        changeVector1[len(changeVector1):len(changeVector1)] = change3

        changeVector3 = [0.1, 0.2, 0.4]        
        changeVector3[len(changeVector3):len(changeVector3)] = change3

        response = cls.client.post("/multiSearch",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={"vectors": [{"vector":changeVector1}, {"vector":changeVector3}], "num":10})    
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        ids = list(set(list(map(lambda x: x.superiorId, searchResult.ids))))
        assert sorted(ids) == ['test-ms1', 'test-ms3', 'test-ms4', 'test-ms5']
    '''     

    def test_SearchById(cls):     

        response = cls.client.post("/searchById",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                    "superiorId": cls.ids["test-ss1"],
                                    "featureId": cls.ids["test-ss1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0
                                })                             
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert searchResult.ids[0].superiorId == cls.ids["test-ss1"]

    def test_SearchBySuperiorId(cls):
        featureIds = []
        for i in range(3):
            featureId = str(uuid.uuid1())
            featureIds.append(featureId)
            response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                        json={
                                "featureVectorIdentifier":{
                                    "superiorId": cls.ids["test-search-by-superiorid"],
                                    "featureId": featureId,
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": cls.vector
                            }
                        )              
            assert response.status_code == 200
        sleep(5)

        response = cls.client.post("/searchBySuperiorId",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                "superiorId": cls.ids["test-search-by-superiorid"],
                                "featureId": "-",
                                "sentenceType": 1,
                                "lang": "ja_JP",
                                "superiorType": 0,
                                "nonSentenceType": 0
                            })                             
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message            
        assert len(list(filter(lambda x: x.superiorId == cls.ids["test-search-by-superiorid"], searchResult.ids))) == 3
        assert len(searchResult.ids) == 3


    def test_ActualDataRemove(cls):     
        
        vector = list(np.random.rand(768))
        testIds = []
        import uuid
        for i in range(5):
            id = str(uuid.uuid1())
            testIds.append(id)
            response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                 "featureVectorIdentifier":{
                                    "superiorId": id,
                                    "featureId": id,
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": vector
                            }) 
            assert response.status_code == 200
        sleep(5)
        for id in testIds:
            response = cls.client.post("/searchById",
                                headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                                json={
                                    "superiorId": id,
                                    "featureId": id,
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0
                                })                             

            assert response.status_code == 200
            searchResult = FeatureVectorSearchResult.parse_obj(response.json())
            assert searchResult.statusInfo.status == "OK"
            assert "" in searchResult.statusInfo.message            
            assert searchResult.ids[0].superiorId == id

        for id in testIds:
            response = cls.client.post("/delete",
                                headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                                json={
                                    "superiorId": id,
                                    "featureId": id,
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0
                                })                             
            assert response.status_code == 200
            statusInfo = StatusInfo.parse_obj(response.json())
            assert statusInfo.status == "OK"
            assert "" in statusInfo.message
        
        sleep(5)
        for id in testIds:
            response = cls.client.post("/searchById",
                                headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                                json={
                                    "superiorId": id,
                                    "featureId": id,
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0
                                })    
            assert response.status_code == 200
            searchResult = FeatureVectorSearchResult.parse_obj(response.json())
            assert searchResult.statusInfo.status == "OK"
            assert "" in searchResult.statusInfo.message            
            assert len(searchResult.ids) == 0


    def test_BlukDataRemove(cls):
        featureIds = []
        for i in range(3):
            featureId = str(uuid.uuid1())
            featureIds.append(featureId)
            response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                        json={
                                "featureVectorIdentifier":{
                                    "superiorId": cls.ids["test-bulk-delete"],
                                    "featureId": featureId,
                                    "sentenceType": 1,
                                    "lang": "ja_JP",
                                    "superiorType": 0,
                                    "nonSentenceType": 0}, 
                                "vector": cls.vector
                            }
                        )              
            assert response.status_code == 200
        sleep(5)

        response = cls.client.post("/deleteBySuperiorId",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                "superiorId": cls.ids["test-bulk-delete"],
                                "featureId": "-",
                                "sentenceType": 1,
                                "lang": "ja_JP",
                                "superiorType": 0,
                                "nonSentenceType": 0
                            })                             
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "OK"
        assert "" in statusInfo.message

        response = cls.client.post("/searchBySuperiorId",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                "superiorId": cls.ids["test-bulk-delete"],
                                "featureId": "-",
                                "sentenceType": 1,
                                "lang": "ja_JP",
                                "superiorType": 0,
                                "nonSentenceType": 0
                            })                             
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message            
        assert len(searchResult.ids) == 0


        response = cls.client.post("/searchById",
                            headers={"Content-Type": "application/json", "X_TOPOSOID_TRANSVERSAL_STATE": cls.transversalState},
                            json={
                                "superiorId": cls.ids["test-ss1"],
                                "featureId": cls.ids["test-ss1"],
                                "sentenceType": 1,
                                "lang": "ja_JP",
                                "superiorType": 0,
                                "nonSentenceType": 0
                            })    
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert len(searchResult.ids) > 0


