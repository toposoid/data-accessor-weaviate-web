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

from fastapi import FastAPI
from model import FeatureVectorForUpdate, SingleFeatureVectorForSearch, FeatureVectorSearchResult, StatusInfo, MultiFeatureVectorForSearch, FeatureVectorIdentifier
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

import os
from logging import config
config.fileConfig('logging.conf')
import logging
LOG = logging.getLogger(__name__)
import traceback
from WeaviateAccessor import WeaviateAccessor
from middleware import ErrorHandlingMiddleware

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
def createSchema():
    try:        
        weaviateAccessor.createSchema()
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message="")))
    except Exception as e:
        LOG.error(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))


@app.post("/insert",
            summary='Registration of feature vectors')
def insert(featureVectorForUpdate:FeatureVectorForUpdate):
    try:        
        weaviateAccessor.insert(featureVectorForUpdate)        
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message="")))
    except Exception as e:
        LOG.error(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

@app.post("/upsert",
            summary='Registering and updating feature vectors')
def insert(featureVectorForUpdate:FeatureVectorForUpdate):
    try:        
        weaviateAccessor.upsert(featureVectorForUpdate.id,featureVectorForUpdate.vector)
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message="")))
    except Exception as e:
        LOG.error(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

@app.post("/search",
            summary='Find Single Feature Vector')
def search(singleFeatureVectorForSearch:SingleFeatureVectorForSearch):
    try:
        ids, similarities = weaviateAccessor.search(singleFeatureVectorForSearch.vector, singleFeatureVectorForSearch.num)
        return JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids = ids, similarities = similarities, statusInfo=StatusInfo(status="OK", message=""))))        
    except Exception as e:
        #Exception occurs when there is no search result for some reason
        LOG.error(traceback.format_exc())
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
def delete(featureVectorIdentifier: FeatureVectorIdentifier):
    try:
        weaviateAccessor.delete(featureVectorIdentifier)
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message="")))
    except Exception as e:
        LOG.error(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

@app.post("/searchById",
            summary='Find a Feature Vector by Id')
def searchById(featureVectorIdentifier: FeatureVectorIdentifier):
    try:
        ids, similarities = weaviateAccessor.searchById(featureVectorIdentifier)
        return JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids = ids, similarities = similarities, statusInfo=StatusInfo(status="OK", message=""))))
    except Exception as e:
        LOG.error(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids=[], similarities=[], statusInfo=StatusInfo(status="ERROR", message=traceback.format_exc()))))
