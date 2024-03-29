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
from fastapi.testclient import TestClient
from api import app
from model import StatusInfo, FeatureVectorSearchResult
import numpy as np
from time import sleep
import pytest
import uuid

class TestWeaviateAPI(object):

    client = TestClient(app)
    vector = list(np.random.rand(768))
    ids = {
        "test-ss1": "47ad6ccb-316f-4d68-a2f0-eb6f2a70a710", 
        "test-ms1": "523da3a7-f772-4b00-8c59-e7e27cfe77eb",
        "test-ms2": "7d771863-2fd2-47c1-8e5a-ff4a77d6e963",
        "test-ms3": "79b08eb8-4651-4203-a1e0-49bd0dbeb7da",
        "test-ms4": "26e48461-9bee-4b62-87b9-ace09ae57e80",
        "test-ms5": "d595119e-045e-49aa-ac82-fbb66e80516c",
        "test-empty": "14ccc264-51db-44e9-b331-c8118e9ca8be",
        "test1": "e947244a-b35d-4457-86cf-28b86fabb959"        
    }

    @classmethod
    def setup_class(cls):    

        response = cls.client.post("/createSchema",
                                   headers={"Content-Type": "application/json"})
        print(StatusInfo.parse_obj(response.json()))
        
        
        response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json"},
                        json={
                                "featureVectorIdentifier":{
                                    "propositionId": cls.ids["test-ss1"],
                                    "featureId": cls.ids["test-ss1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP"}, 
                                "vector": cls.vector
                            }
                        )    
        print(StatusInfo.parse_obj(response.json()))

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
                        headers={"Content-Type": "application/json"},
                        json={
                                 "featureVectorIdentifier":{
                                    "propositionId": cls.ids["test-ms1"],
                                    "featureId": cls.ids["test-ms1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP"}, 
                                "vector": changeVector1
                            }
                        )    
        assert response.status_code == 200
        response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json"},
                        json={
                                 "featureVectorIdentifier":{
                                    "propositionId": cls.ids["test-ms2"],
                                    "featureId": cls.ids["test-ms2"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP"}, 
                                "vector": changeVector2
                            }
                        )    
        assert response.status_code == 200
        response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json"},
                        json={
                                 "featureVectorIdentifier":{
                                    "propositionId": cls.ids["test-ms3"],
                                    "featureId": cls.ids["test-ms3"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP"}, 
                                "vector": changeVector3
                            }
                        )    
        assert response.status_code == 200
        response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json"},
                        json={
                                 "featureVectorIdentifier":{
                                    "propositionId": cls.ids["test-ms4"],
                                    "featureId": cls.ids["test-ms4"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP"}, 
                                "vector": changeVector3
                            }
                        )    
        assert response.status_code == 200
        response = cls.client.post("/insert",
                        headers={"Content-Type": "application/json"},
                        json={
                                 "featureVectorIdentifier":{
                                    "propositionId": cls.ids["test-ms5"],
                                    "featureId": cls.ids["test-ms5"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP"}, 
                                "vector": changeVector4
                            }
                        )                        
        assert response.status_code == 200
        
        sleep(5)
    

    def test_InsertEmptyVector(cls):    
        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={
                                 "featureVectorIdentifier":{
                                    "propositionId": cls.ids["test-empty"],
                                    "featureId": cls.ids["test-empty"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP"}, 
                                "vector": []
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"
        assert "new node has a vector with length 0" in statusInfo.message


    def test_InsertEmptyId(cls):    
        
        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={
                                 "featureVectorIdentifier":{
                                    "propositionId": "",
                                    "featureId": "hoge",
                                    "sentenceType": 1,
                                    "lang": "ja_JP"}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"

        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={
                                 "featureVectorIdentifier":{
                                    "propositionId": "hoge",
                                    "featureId": "",
                                    "sentenceType": 1,
                                    "lang": "ja_JP"}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"

        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={
                                 "featureVectorIdentifier":{
                                    "propositionId": "hoge",
                                    "featureId": "hoge",
                                    "sentenceType": 3,
                                    "lang": "ja_JP"}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"

        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={
                                 "featureVectorIdentifier":{
                                    "propositionId": "hoge",
                                    "featureId": "hoge",
                                    "sentenceType": "",
                                    "lang": "ja_JP"}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"

        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={
                                 "featureVectorIdentifier":{
                                    "propositionId": "hoge",
                                    "featureId": "hoge",
                                    "sentenceType": "",
                                    "lang": ""}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"

        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={
                                 "featureVectorIdentifier":{
                                    "propositionId": "hoge",
                                    "featureId": "hoge",
                                    "sentenceType": "",
                                    "lang": "fr_FR"}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"



    def test_InsertAndDelete(cls):  
        
        response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={
                                 "featureVectorIdentifier":{
                                    "propositionId": cls.ids["test1"],
                                    "featureId": cls.ids["test1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP"}, 
                                "vector": cls.vector
                            })
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "OK"
        assert "" in statusInfo.message
        
        response = cls.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={
                                    "propositionId": cls.ids["test1"],
                                    "featureId": cls.ids["test1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP"
                                })

        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "OK"
        assert "" in statusInfo.message

        response = cls.client.post("/searchById",
                            headers={"Content-Type": "application/json"},
                            json={
                                    "propositionId": cls.ids["test1"],
                                    "featureId": cls.ids["test1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP"
                                })                                
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert len(searchResult.ids) == 0




    def test_SingleSearch(cls):     

        response = cls.client.post("/search",
                            headers={"Content-Type": "application/json"},
                            json={"vector": cls.vector, "num":10})    
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert searchResult.ids[0].propositionId == cls.ids["test-ss1"]

    def test_SingleEasySearch(cls):     

        response = cls.client.post("/easySearch",
                            headers={"Content-Type": "application/json"},
                            json={"vector": cls.vector, "num":10, "similarityThreshold":0.5})    
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert searchResult.ids[0].propositionId == cls.ids["test-ss1"]


    def test_SingleSearchNoResponse(cls):     

        response = cls.client.post("/search",
                            headers={"Content-Type": "application/json"},
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
                            headers={"Content-Type": "application/json"},
                            json={"vectors": [{"vector":changeVector1}, {"vector":changeVector3}], "num":10})    
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        ids = list(set(list(map(lambda x: x.propositionId, searchResult.ids))))
        assert sorted(ids) == ['test-ms1', 'test-ms3', 'test-ms4', 'test-ms5']
    '''     

    def test_SearchById(cls):     

        response = cls.client.post("/searchById",
                            headers={"Content-Type": "application/json"},
                            json={
                                    "propositionId": cls.ids["test-ss1"],
                                    "featureId": cls.ids["test-ss1"],
                                    "sentenceType": 1,
                                    "lang": "ja_JP"
                                })                             
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert searchResult.ids[0].propositionId == cls.ids["test-ss1"]

    def test_ActualDataRemove(cls):     
        
        vector = list(np.random.rand(768))
        testIds = []
        import uuid
        for i in range(5):
            id = str(uuid.uuid1())
            testIds.append(id)
            response = cls.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={
                                 "featureVectorIdentifier":{
                                    "propositionId": id,
                                    "featureId": id,
                                    "sentenceType": 1,
                                    "lang": "ja_JP"}, 
                                "vector": vector
                            }) 
            assert response.status_code == 200
        sleep(5)
        for id in testIds:
            response = cls.client.post("/searchById",
                                headers={"Content-Type": "application/json"},
                                json={
                                    "propositionId": id,
                                    "featureId": id,
                                    "sentenceType": 1,
                                    "lang": "ja_JP"
                                })                             

            assert response.status_code == 200
            searchResult = FeatureVectorSearchResult.parse_obj(response.json())
            assert searchResult.statusInfo.status == "OK"
            assert "" in searchResult.statusInfo.message            
            assert searchResult.ids[0].propositionId == id

        for id in testIds:
            response = cls.client.post("/delete",
                                headers={"Content-Type": "application/json"},
                                json={
                                    "propositionId": id,
                                    "featureId": id,
                                    "sentenceType": 1,
                                    "lang": "ja_JP"
                                })                             
            assert response.status_code == 200
            statusInfo = StatusInfo.parse_obj(response.json())
            assert statusInfo.status == "OK"
            assert "" in statusInfo.message
        
        sleep(5)
        for id in testIds:
            response = cls.client.post("/searchById",
                                headers={"Content-Type": "application/json"},
                                json={
                                    "propositionId": id,
                                    "featureId": id,
                                    "sentenceType": 1,
                                    "lang": "ja_JP"
                                })    
            assert response.status_code == 200
            searchResult = FeatureVectorSearchResult.parse_obj(response.json())
            assert searchResult.statusInfo.status == "OK"
            assert "" in searchResult.statusInfo.message            
            assert len(searchResult.ids) == 0
