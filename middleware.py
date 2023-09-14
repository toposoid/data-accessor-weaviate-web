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

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback
from model import StatusInfo
from fastapi.encoders import jsonable_encoder
import logging
LOG = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response: Response = await call_next(request)
            if response.status_code != 200:
                LOG.error(traceback.format_exc())
                response = JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))
        except Exception as e:
            LOG.error(traceback.format_exc())
            response = JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

        return response
