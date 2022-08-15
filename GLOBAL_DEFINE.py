# -*-coding:utf-8-*-
# @author xy
# @func declare all global constant
import json
import os
from datetime import datetime
from random import sample
import string

from dbDefine import AnimeDataBase

CONFIG_PATH = "/config/config.json"
DB_PATH = "./test.sqlite"#"/config/XNT.db"
ARIA2_RPC_SERVER = "http://192.168.5.146:6800/jsonrpc"
ARIA2_JSONRPC_TOKEN = "QQ2496873241xy"
DB_TIME_FORMAT = "%Y-%m-%d %H:%M"
UNIFIED_TIME_FORMAT = "%m-%d %H:%M:%S"
HTML_TIME_FORMAT = "%Y-%m-%d\n%H:%M"
HTML_INPUT_TIME_FORMAT = "%Y-%m-%dT%H:%M"
DEFAULT_CORE_QUANTITY = 4
LOG_DIR = "./config/logs/"
JACKETT_API_LINK_LIST = ["http://192.168.5.146:9117/api/v2.0/indexers/miobt/results/torznab/api?apikey=52zowbq26u5aoo3oun5u2kt78jiy5qx6&t=search&cat=&q=","http://192.168.5.146:9117/api/v2.0/indexers/mikan/results/torznab/api?apikey=52zowbq26u5aoo3oun5u2kt78jiy5qx6&t=search&cat=&q=",
    "http://192.168.5.146:9117/api/v2.0/indexers/comicat/results/torznab/api?apikey=52zowbq26u5aoo3oun5u2kt78jiy5qx6&t=search&cat=&q="]

ERROR_RETRY_SPAN = 12

FILTER_DICTS = {"default": {"episode": "0", "reject_rules": [], "including_rules": []}}


def app_init():
    global CONFIG_PATH, DB_PATH, ARIA2_JSONRPC_TOKEN, ARIA2_RPC_SERVER, DEFAULT_CORE_QUANTITY, LOG_DIR, JACKETT_API_LINK_LIST, ERROR_RETRY_SPAN,FILTER_DICTS
    paras_json = {}
    if not os.path.exists("/config"):
        os.mkdir("/config")
    if not os.path.exists(CONFIG_PATH):
        open(CONFIG_PATH, "w").close()
    with open(CONFIG_PATH, "r") as fp:
        paras_json = json.load(fp)
    if not paras_json:
        AnimeDataBase(DB_PATH).__createDB__()
        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)
        with open(CONFIG_PATH, "w") as fp:
            paras_json = {
                'CONFIG_PATH': CONFIG_PATH,
                'DB_PATH': DB_PATH,
                'ARIA2_RPC_SERVER': ARIA2_RPC_SERVER,
                'ARIA2_JSONRPC_TOKEN': ARIA2_JSONRPC_TOKEN,
                'DEFAULT_CORE_QUANTITY': DEFAULT_CORE_QUANTITY,
                'LOG_DIR': LOG_DIR,
                'JACKETT_API_LINK_LIST': JACKETT_API_LINK_LIST,
                'ERROR_RETRY_SPAN': ERROR_RETRY_SPAN,
                'FILTER_DICTs': FILTER_DICTS,
            }
            json.dump(paras_json, fp)
    else:
        CONFIG_PATH = paras_json.get('CONFIG_PATH', CONFIG_PATH)
        DB_PATH = paras_json.get('DB_PATH', DB_PATH)
        ARIA2_RPC_SERVER = paras_json.get('ARIA2_RPC_SERVER', ARIA2_RPC_SERVER)
        ARIA2_JSONRPC_TOKEN = paras_json.get('ARIA2_JSONRPC_TOKEN', ARIA2_JSONRPC_TOKEN)
        DEFAULT_CORE_QUANTITY = paras_json.get('DEFAULT_CORE_QUANTITY', DEFAULT_CORE_QUANTITY)
        LOG_DIR = paras_json.get('LOG_DIR', LOG_DIR)
        JACKETT_API_LINK_LIST = paras_json.get('JACKETT_API_LINK_LIST', JACKETT_API_LINK_LIST)
        ERROR_RETRY_SPAN = paras_json.get('ERROR_RETRY_SPAN', ERROR_RETRY_SPAN)
        FILTER_DICTS = paras_json.get('FILTER_DICTS', FILTER_DICTS)


def journal_write(msg):
    if os.path.exists(LOG_DIR + datetime.now().strftime("%y-%m-%d") + ".log"):
        with open(LOG_DIR + datetime.now().strftime("%y-%m-%d") + ".log", "a") as fp:
            fp.write(f"[{datetime.now().strftime('%H:%M:%S')}]:{msg}\n")
            fp.close()
    else:
        with open(LOG_DIR + datetime.now().strftime("%y-%m-%d") + ".log", "w") as fp:
            fp.write(f"[{datetime.now().strftime('%H:%M:%S')}]:{msg}\n")
            fp.close()
