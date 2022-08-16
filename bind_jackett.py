import re
import xml.etree.ElementTree as ET

import requests

from GLOBAL_DEFINE import *


def get_result_from_jackett(keyword, filter_dict):
    CONFIG_PATH, DB_PATH, ARIA2_RPC_SERVER, ARIA2_JSONRPC_TOKEN, DEFAULT_CORE_QUANTITY, LOG_DIR, JACKETT_API_LINK_LIST, ERROR_RETRY_SPAN, FILTER_DICTS=app_init()
    result_list = []
    try:
        for api_url in JACKETT_API_LINK_LIST:
            api_request_url = api_url + keyword + "+" + filter_dict.get("episode", "0")
            r = requests.get(api_request_url).text
            jackett_result_xml = ET.fromstring(r)
            root = jackett_result_xml.iter("item")

            for child in root:
                title = ""
                link = ""
                for e in child.iter("title"):
                    title = e.text
                if resolve_regex_match(title, filter_dict):
                    for e in child.iter("link"):
                        link = e.text
                    if link.startswith("magnet"):
                        result_list.append({"title": title, "link": link})
    except Exception as e:
        journal_write(str(e))
    finally:
        return result_list


def resolve_regex_match(title, filter_dict):
    for reject_rule in filter_dict.get("reject_rules", []):
        if re.search(reject_rule, title, re.I):
            return False
    for including_rule in filter_dict.get("including_rules", []):
        if not re.search(including_rule, title, re.I):
            return False
    if not re.search(filter_dict.get("episode", "0"), title, re.I):
        return False
    return True


if __name__ == "__main__":
    for i in get_result_from_jackett("莉可丽丝", {"episode":"03","reject_rules":["繁体"],"including_rules":["喵萌","简|简体","1080"]}):
        print(i)
