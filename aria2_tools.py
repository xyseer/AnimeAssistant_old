from GLOBAL_DEFINE import *
import random
import string
import json
import requests


def send_download_info_to_aria2(result_item, save_dir):
    mission_id = "".join(random.sample(string.ascii_letters, 9))
    aria2_rpc_post_dict = {"id": mission_id,
                           "jsonrpc": "2.0",
                           "method": "aria2.addUri",
                           "params": [
                               f"token:{ARIA2_JSONRPC_TOKEN}",
                               [
                                   result_item.get("link", "")
                               ],
                               {
                                   "dir": save_dir
                               }
                           ]
                           }
    aria2_rpc_post = json.dumps(aria2_rpc_post_dict)
    try:
        response=requests.post(ARIA2_RPC_SERVER,aria2_rpc_post)
        response_json=json.loads(response.text)
        if response_json.get("error",""):
            journal_write(f"Aria2 jsonrpc server return an error when processing '{result_item.get('title','')}' :{str(response_json.get('error',''))}")
            return ""
        if response_json.get("result",""):
            return response_json.get("result","")
        return ""
    except Exception as e:
        journal_write(f"ERROR occured when executing '{result_item.get('title','')}' in send_download_info_to_aria2 :"+str(e))
        return ""


if __name__ == "__main__":
    print("NOT THE PROGRAM ENTRANCE,EXIT...")
    exit(0)
