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

from fastapi import FastAPI, Header
#from model import FeatureVectorForUpdate, SingleFeatureVectorForSearch, FeatureVectorSearchResult, StatusInfo, SingleFeatureVectorForEasySearch, FeatureVectorIdentifier, TransversalState
from ToposoidCommon.model import FeatureVectorForUpdate, SingleFeatureVectorForSearch, FeatureVectorSearchResult, SingleFeatureVectorForEasySearch, FeatureVectorIdentifier, StatusInfo,  TransversalState
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
#import yaml
import traceback
from WeaviateAccessor import WeaviateAccessor
from middleware import ErrorHandlingMiddleware
#from typing import Optional
#from utils import formatMessageForLogger

#from logging import config
#config.dictConfig(yaml.load(open("logging.yml", encoding="utf-8").read(), Loader=yaml.SafeLoader))
#import logging

import ToposoidCommon as tc
from typing import Optional
LOG = tc.LogUtils(__name__)

app = FastAPI(
    title="data-accessor-weaviate-web",
    version="0.6-SNAPSHOT"
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
        LOG.info("Creating Schema completed.", transversalState)
        return response
    except Exception as e:
        LOG.error(traceback.format_exc(), transversalState)
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))


@app.post("/insert",
            summary='Registration of feature vectors')
def insert(featureVectorForUpdate:FeatureVectorForUpdate, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:           
        weaviateAccessor.insert(featureVectorForUpdate)   
        response = JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message=""))) 
        LOG.info("Registration of feature vectors completed.", transversalState)   
        return response
    except Exception as e:
        LOG.error(traceback.format_exc(), transversalState)
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

@app.post("/upsert",
            summary='Registering and updating feature vectors')
def insert(featureVectorForUpdate:FeatureVectorForUpdate, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:                
        weaviateAccessor.upsert(featureVectorForUpdate.id,featureVectorForUpdate.vector)
        response = JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message="")))
        LOG.info(f"Registration of feature vectors completed.", transversalState)   
        return response
    except Exception as e:
        LOG.error(traceback.format_exc(), transversalState)
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

@app.post("/search",
            summary='Find Single Feature Vector')
def search(singleFeatureVectorForSearch:SingleFeatureVectorForSearch, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:        
        ids, similarities = weaviateAccessor.search(singleFeatureVectorForSearch.vector, singleFeatureVectorForSearch.num)
        response = JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids = ids, similarities = similarities, statusInfo=StatusInfo(status="OK", message=""))))        
        featureIds = list(map(lambda x: x.featureId, ids))
        LOG.info("id:" + str(featureIds) + " similarity:" + str(similarities), transversalState)
        LOG.info("Searching Feature Vector completed.", transversalState)   
        return response
    except Exception as e:
        #Exception occurs when there is no search result for some reason
        LOG.error(traceback.format_exc(), transversalState)
        return JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids=[], similarities=[], statusInfo=StatusInfo(status="ERROR", message=traceback.format_exc()))))

@app.post("/easySearch",
            summary='Find Single Feature Vector')
def search(singleFeatureVectorForEasySearch:SingleFeatureVectorForEasySearch, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:        
        ids, similarities = weaviateAccessor.easySearch(singleFeatureVectorForEasySearch.vector, singleFeatureVectorForEasySearch.num, singleFeatureVectorForEasySearch.similarityThreshold)
        response = JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids = ids, similarities = similarities, statusInfo=StatusInfo(status="OK", message=""))))        
        featureIds = list(filter(lambda x: x.featureId, ids))
        LOG.info("id:" + str(featureIds) + " similarity:" + str(similarities), transversalState)
        LOG.info("Searching Feature Vector completed.", transversalState)   
        return response
    except Exception as e:
        #Exception occurs when there is no search result for some reason
        LOG.error(traceback.format_exc(), transversalState)
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
        weaviateAccessor.delete(featureVectorIdentifier, transversalState)
        response = JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message="")))
        LOG.info("Removing Feature Vector completed.", transversalState)   
        return response
    except Exception as e:
        LOG.error(traceback.format_exc(), transversalState)
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

@app.post("/searchById",
            summary='Find a Feature Vector by Id')
def searchById(featureVectorIdentifier: FeatureVectorIdentifier, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:        
        ids, similarities = weaviateAccessor.searchById(featureVectorIdentifier)
        response = JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids = ids, similarities = similarities, statusInfo=StatusInfo(status="OK", message=""))))
        LOG.info("Searching By Id completed.", transversalState)   
        return response
    except Exception as e:
        LOG.error(traceback.format_exc(), transversalState)
        return JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids=[], similarities=[], statusInfo=StatusInfo(status="ERROR", message=traceback.format_exc()))))


@app.post("/deleteBySuperiorId",
            summary='Delete a Feature Vector')
def deleteBySuperiorId(featureVectorIdentifier: FeatureVectorIdentifier, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:        
        weaviateAccessor.deleteBySuperiorId(featureVectorIdentifier, transversalState)
        response = JSONResponse(content=jsonable_encoder(StatusInfo(status="OK", message="")))
        LOG.info("Removing Feature Vector completed.", transversalState)   
        return response
    except Exception as e:
        LOG.error(traceback.format_exc(), transversalState)
        return JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

@app.post("/searchBySuperiorId",
            summary='Find a Feature Vector by Id')
def searchByBySuperiorId(featureVectorIdentifier: FeatureVectorIdentifier, X_TOPOSOID_TRANSVERSAL_STATE: Optional[str] = Header(None, convert_underscores=False)):
    transversalState = TransversalState.parse_raw(X_TOPOSOID_TRANSVERSAL_STATE.replace("'", "\""))
    try:        
        ids, similarities = weaviateAccessor.searchBySuperiorId(featureVectorIdentifier)
        response = JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids = ids, similarities = similarities, statusInfo=StatusInfo(status="OK", message=""))))
        LOG.info("Searching By Id completed.", transversalState)   
        return response
    except Exception as e:
        LOG.error(traceback.format_exc(), transversalState)
        return JSONResponse(content=jsonable_encoder(FeatureVectorSearchResult(ids=[], similarities=[], statusInfo=StatusInfo(status="ERROR", message=traceback.format_exc()))))

