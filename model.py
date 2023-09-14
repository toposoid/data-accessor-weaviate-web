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

from pydantic import BaseModel, ValidationError, validator
from typing import List
import logging
LOG = logging.getLogger(__name__)

#For deleting feature vectors
class FeatureVectorIdentifier(BaseModel):
    propositionId:str
    featureId:str
    sentenceType:int
    lang:str

    @validator("propositionId", pre=True)
    def parsePropositionId(cls, v):
        if not isinstance(v, str):
            logging.error("propositionId is not StringType.") 
            raise ValidationError("propositionId is not StringType.")
        return v

    @validator("featureId", pre=True)
    def parseFeatureId(cls, v):
        if not isinstance(v, str):
            logging.error("featureId is not StringType.")
            raise ValidationError("featureId is not StringType.")
        return v

    @validator("sentenceType", pre=True)
    def parseSentenceType(cls, v):
        if not isinstance(v, int):
            logging.error("sentenceType is not IntType.")
            raise ValidationError("sentenceType is not IntType.")
        return v

    @validator("lang", pre=True)
    def parseLang(cls, v):
        if not isinstance(v, str):
            logging.error("lang is not StringType.")
            raise ValidationError("lang is not StringType.")
        return v


    @validator("propositionId")
    def isNotEmptyPropositionId(cls, v):
        if not v:
            logging.error("propositionId is empty.")
            raise ValidationError("propositionId is empty.")
        return v

    @validator("featureId")
    def isNotEmptyFeatureId(cls, v):
        if not v:
            logging.error("featureId is empty.")
            raise ValidationError("featureId is empty.")
        return v

    @validator("sentenceType")
    def isNotEmptySentenceType(cls, v):
        if v > 2 or v < 0:
            logging.error("sentenceType is invalid.")
            raise ValidationError("sentenceType is invalid.")
        return v

    @validator("lang")
    def isNotEmptyLang(cls, v):
        if not v:
            logging.error("lang is empty.")
            raise ValidationError("lang is empty.")
        if v not in ["ja_JP", "en_US"]:
            logging.error("lang is invalid.")
            raise ValidationError("lang is invalid.")
        return v


#For searching feature vectors.
class FeatureVectorForUpdate(BaseModel):
    featureVectorIdentifier: FeatureVectorIdentifier
    vector:List[float]

#For searching feature vectors.
class FeatureVectorForSearch(BaseModel):
    vector:List[float]

#For feature vector search requests
class SingleFeatureVectorForSearch(BaseModel):
    vector:List[float]
    num:int

#For feature vector search requests. Multiple vectors can be set.
class MultiFeatureVectorForSearch(BaseModel):
    vectors:List[FeatureVectorForSearch]
    num:int

#Status Information
class StatusInfo(BaseModel):
    status:str
    message:str

#For feature vector search results
class FeatureVectorSearchResult(BaseModel):
    ids:List[FeatureVectorIdentifier]
    similarities:List[float]
    statusInfo:StatusInfo