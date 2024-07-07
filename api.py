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

from fastapi import FastAPI, Header
from model import FeatureVectorForUpdate, SingleFeatureVectorForSearch, FeatureVectorSearchResult, StatusInfo, SingleFeatureVectorForEasySearch, FeatureVectorIdentifier, TransversalState
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

import traceback
from WeaviateAccessor import WeaviateAccessor
from middleware import ErrorHandlingMiddleware
from typing import Optional
from utils import formatMessageForLogger

from logging import config
config.fileConfig('logging.conf')
import logging
LOG = logging.getLogger(__name__)


app = FastAPI(
    title="data-accessor-weaviate-web",
    version="0.5-SNAPSHOT"
)
app.add_middleware(ErrorHandlingMiddleware)
weaviateAccessor = WeaviateAccessor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



@app.post("/createSchema",
          summary='create a createSchema')
def createSchema(X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:            
        weaviateAccessor.createSchema()
        response = JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message="")))
        LOG.info(formatMessageForLogger("Creating Schema completed.", transversalState.username),extra={"tab":"\t"})
        return response
    except Exception as e:
        LOG.error(formatMessageForLogger(traceback.format_exc(), transversalState.username),extra={"tab":"\t"})
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))


@app.post("/insert",
            summary='Registration of feature vectors')
def insert(featureVectorForUpdate:FeatureVectorForUpdate, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:           
        weaviateAccessor.insert(featureVectorForUpdate)   
        response = JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message=""))) 
        LOG.info(formatMessageForLogger("Registration of feature vectors completed.", transversalState.username),extra={"tab":"\t"})   
        return response
    except Exception as e:
        LOG.error(formatMessageForLogger(traceback.format_exc(), transversalState.username),extra={"tab":"\t"})
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

@app.post("/upsert",
            summary='Registering and updating feature vectors')
def insert(featureVectorForUpdate:FeatureVectorForUpdate, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:                
        weaviateAccessor.upsert(featureVectorForUpdate.id,featureVectorForUpdate.vector)
        response = JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message="")))
        LOG.info(formatMessageForLogger("Registration of feature vectors completed.", transversalState.username),extra={"tab":"\t"})   
        return response
    except Exception as e:
        LOG.error(formatMessageForLogger(traceback.format_exc(), transversalState.username),extra={"tab":"\t"})
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

@app.post("/search",
            summary='Find Single Feature Vector')
def search(singleFeatureVectorForSearch:SingleFeatureVectorForSearch, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:        
        ids, similarities = weaviateAccessor.search(singleFeatureVectorForSearch.vector, singleFeatureVectorForSearch.num)
        response = JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids = ids, similarities = similarities, statusInfo=StatusInfo(status="OK", message=""))))        
        LOG.info(formatMessageForLogger("Searching Feature Vector completed.", transversalState.username),extra={"tab":"\t"})   
        return response
    except Exception as e:
        #Exception occurs when there is no search result for some reason
        LOG.error(formatMessageForLogger(traceback.format_exc(), transversalState.username),extra={"tab":"\t"})
        return JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids=[], similarities=[], statusInfo=StatusInfo(status="ERROR", message=traceback.format_exc()))))

@app.post("/easySearch",
            summary='Find Single Feature Vector')
def search(singleFeatureVectorForEasySearch:SingleFeatureVectorForEasySearch, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:        
        ids, similarities = weaviateAccessor.easySearch(singleFeatureVectorForEasySearch.vector, singleFeatureVectorForEasySearch.num, singleFeatureVectorForEasySearch.similarityThreshold)
        response = JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids = ids, similarities = similarities, statusInfo=StatusInfo(status="OK", message=""))))        
        LOG.info(formatMessageForLogger("Searching Feature Vector completed.", transversalState.username),extra={"tab":"\t"})   
        return response
    except Exception as e:
        #Exception occurs when there is no search result for some reason
        LOG.error(formatMessageForLogger(traceback.format_exc(), transversalState.username),extra={"tab":"\t"})
        return JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids=[], similarities=[], statusInfo=StatusInfo(status="ERROR", message=traceback.format_exc()))))

'''
@app.post("/multiSearch",
            summary='Find Multi Feature Vector')
def multiSearch(multiFeatureVectorForSearch:MultiFeatureVectorForSearch):
    try:
        ids, similarities  = weaviateAccessor.multiSearch(multiFeatureVectorForSearch.vectors, multiFeatureVectorForSearch.num)
        return JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids = ids, similarities = similarities, statusInfo=StatusInfo(status="OK", message=""))))        
    except Exception as e:
        #Exception occurs when there is no search result for some reason
        LOG.error(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids=[], similarities=[], statusInfo=StatusInfo(status="ERROR", message=traceback.format_exc()))))
'''

@app.post("/delete",
            summary='Delete a Feature Vector')
def delete(featureVectorIdentifier: FeatureVectorIdentifier, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:        
        weaviateAccessor.delete(featureVectorIdentifier)
        response = JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message="")))
        LOG.info(formatMessageForLogger("Removing Feature Vector completed.", transversalState.username),extra={"tab":"\t"})   
        return response
    except Exception as e:
        LOG.error(formatMessageForLogger(traceback.format_exc(), transversalState.username),extra={"tab":"\t"})
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

@app.post("/searchById",
            summary='Find a Feature Vector by Id')
def searchById(featureVectorIdentifier: FeatureVectorIdentifier, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:        
        ids, similarities = weaviateAccessor.searchById(featureVectorIdentifier)
        response = JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids = ids, similarities = similarities, statusInfo=StatusInfo(status="OK", message=""))))
        LOG.info(formatMessageForLogger("Searching By Id completed.", transversalState.username),extra={"tab":"\t"})   
        return response
    except Exception as e:
        LOG.error(formatMessageForLogger(traceback.format_exc(), transversalState.username),extra={"tab":"\t"})
        return JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids=[], similarities=[], statusInfo=StatusInfo(status="ERROR", message=traceback.format_exc()))))
