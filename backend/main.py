import logging
import uvicorn
import betterlogging as bl
import fastapi
# from aiogram import Bot
from fastapi import FastAPI
from starlette.responses import JSONResponse
from config import load_config

import hmac
import hashlib
from urllib.parse import unquote

from fastapi.security import HTTPBasic, HTTPBasicCredentials


# from tgbot.config import load_config, Config

app = FastAPI()

log_level = logging.INFO
bl.basic_colorized_config(level=log_level)
log = logging.getLogger('backend')

config = load_config("../.env")

security = HTTPBasic()
# config: Config = load_config()
# session_pool = create_session_pool(config.db)
# bot = Bot(token=config.tg_bot.token)


@app.post("/api")
async def webhook_endpoint(request: fastapi.Request):
    return JSONResponse(status_code=200, content={"status": "ok"})

@app.get("/test")
async def webhook_endpoint(request: fastapi.Request):
    return JSONResponse(status_code=200, content={"status": "ok"})

# @app.get("/validate")
# async def getVerification(request: fastapi.Request):

#     Authorization = request.headers.get("Authorization")
#     initData = request.query_params.get("initData")
#     hash = request.query_params.get("hash")
#     token = config.tg_bot.token
#     dataValidation = validate(hash, initData, token)
#     print(request.query_params)
#     return JSONResponse(status_code=200, content={"status": "validated"})


# def validate(hash_str, init_data, token, c_str="WebAppData"):
#     """
#     Validates the data received from the Telegram web app, using the
#     method documented here: 
#     https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

#     hash_str - the has string passed by the webapp
#     init_data - the query string passed by the webapp
#     token - Telegram bot's token
#     c_str - constant string (default = "WebAppData")
#     """

#     init_data = sorted([ chunk.split("=") 
#           for chunk in unquote(init_data).split("&") 
#             if chunk[:len("hash=")]!="hash="],
#         key=lambda x: x[0])
#     init_data = "\n".join([f"{rec[0]}={rec[1]}" for rec in init_data])

#     secret_key = hmac.new(c_str.encode(), token.encode(),
#         hashlib.sha256 ).digest()
#     data_check = hmac.new( secret_key, init_data.encode(),
#         hashlib.sha256)

#     return data_check.hexdigest() == hash_str