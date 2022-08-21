import time
from datetime import timedelta
from multiprocessing import Pool
from time import sleep
from GLOBAL_DEFINE import *
from aria2_tools import send_download_info_to_aria2
from bind_jackett import get_result_from_jackett
from databaseTool import ProcessingNameTable, ProcessingSubscriptionTable, ProcessingDownloadTable

CONFIG_PATH, DB_PATH, ARIA2_RPC_SERVER, ARIA2_JSONRPC_TOKEN, DEFAULT_CORE_QUANTITY, LOG_DIR, JACKETT_API_LINK_LIST, ERROR_RETRY_SPAN, FILTER_DICTS = app_init()


class SubscriptionItem:
    def __init__(self, sub_dict):
        self.nextTime = sub_dict.get("nextUpdateTime")
        self.span = sub_dict.get("span", 24)
        self.origin = sub_dict
        self.type = sub_dict.get("type")
        self.id = sub_dict.get("id", -1)


def run_time_up_work(item: SubscriptionItem):
    CONFIG_PATH, DB_PATH, ARIA2_RPC_SERVER, ARIA2_JSONRPC_TOKEN, DEFAULT_CORE_QUANTITY, LOG_DIR, JACKETT_API_LINK_LIST, ERROR_RETRY_SPAN, FILTER_DICTS=app_init()
    if item.type == "download":
        if item.origin.get("totalEpisodes", -1) < item.origin.get("nextUpdateEP", 0):
            return False
        db = AnimeDataBase(DB_PATH)
        name = ProcessingNameTable(db).getSearchResult(table_id=item.id)[0].get("name", "Unknown")
        download_info = ProcessingDownloadTable(db).getSearchResult(table_id=item.id)[0]
        db.__del__()
        if download_info.get("downloadway", "") == "way_jackett":
            journal_write(f"Executing Subscription:'{name}'.")
            reformat_filter=FILTER_DICTS.get(
                download_info.get("filter", "default"),
                {"episode": "0", "reject_rules": [], "including_rules": []})
            reformat_filter["episode"]=str(item.origin.get("nextUpdateEP", 0))
            result_list = get_result_from_jackett(name, filter_dict=reformat_filter)
            journal_write(
                f"Find {len(result_list)} matches of '{name}' from jackett. Automatic Select best-matched one to download.")
            if not result_list:
                return False
            is_sent = send_download_info_to_aria2(result_list[0], download_info.get('directory', ""))
            if is_sent:
                journal_write(f"Subscription '{name}' has been successfully push to Aria2.")
                db = AnimeDataBase(DB_PATH)
                ProcessingSubscriptionTable(db).update(item.id, lastUpdateTime=datetime.now(),
                                                            lastUpdateEP=item.origin.get("lastUpdateEP", -2) + 1,
                                                            nextUpdateTime=item.origin.get("nextUpdateTime",datetime.now())+ timedelta(hours=item.span),
                                                            nextUpdateEP=item.origin.get("lastUpdateEP", -3) + 2)
                item.nextTime = item.nextTime + timedelta(hours=item.span)
                db.__del__()
                return True
            else:
                journal_write(f"Subscription '{name}' failed. Retry after {ERROR_RETRY_SPAN} hours.")
                item.nextTime = item.nextTime + timedelta(hours=ERROR_RETRY_SPAN)
                return False

    return False


class ScheduleWork:
    def __init__(self, core_nums):
        self.process_pool = Pool(core_nums)
        # self.thread_time = 0
        self.reset = True
        self.schedule_list = []
        # self.process_pool.map_async()

    def main_schedule(self):
        global DB_PATH,ERROR_RETRY_SPAN
        while True:
            try:
                journal_write("Checking new contents...")
                print("Checking new contents...")
                now = datetime.now()
                if self.reset:
                    print("schedule_reset")
                    db = AnimeDataBase(DB_PATH)
                    self.schedule_list = []
                    for work in ProcessingSubscriptionTable(db).getSearchResult():
                        self.schedule_list.append(SubscriptionItem(work))
                    self.reset = False
                    continue
                for item in self.schedule_list:
                    if item.nextTime <= now:
                        run_time_up_work(item)
                journal_write("Check work Finished")
                sleep(ERROR_RETRY_SPAN*3600)
            except Exception as e:
                raise e
                journal_write(str(e))
                print(e)
        print("unexpected crash.")
        journal_write("unexpected crashed.")

    def __del__(self):
        self.process_pool.close()
        self.process_pool.terminate()


if __name__ == "__main__":
    ss = ScheduleWork(DEFAULT_CORE_QUANTITY)
    print(datetime.now())
    pass
    try:
        ss.main_schedule()
        journal_write("================MAIN PROCESS UNEXPECTED EXIT=================")
    except KeyboardInterrupt:
        journal_write("================MAIN PROCESS TERMINATE=================")
        pass
    except InterruptedError:
        journal_write("================MAIN PROCESS TERMINATE=================")
        pass
