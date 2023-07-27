import time

from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Form, Depends, File, UploadFile
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import \
    RedirectResponse, FileResponse, HTMLResponse, PlainTextResponse
from starlette.status import *

app = FastAPI()


@app.get('/')
def get(request: Request):
    kwargs = dict(request.query_params)
    print(kwargs, '1')
    return kwargs



if __name__ == '__main__':
    import uvicorn
    from uvicorn import logging

    uvicorn.run(app, host="0.0.0.0", port=8040)