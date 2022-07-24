import time
from datetime import timedelta
from multiprocessing import Pool
from time import sleep
from GLOBAL_DEFINE import *
from aria2_tools import send_download_info_to_aria2
from bind_jackett import get_result_from_jackett
from databaseTool import ProcessingNameTable, ProcessingSubscriptionTable, ProcessingDownloadTable


class SubscriptionItem:
    def __init__(self, sub_dict):
        self.nextTime = sub_dict.get("nextUpdateTime")
        self.span = sub_dict.get("span", 24)
        self.origin = sub_dict
        self.type = sub_dict.get("type")
        self.id = sub_dict.get("id", -1)


class ScheduleWork:
    def __init__(self, core_nums):
        self.process_pool = Pool(core_nums)
        # self.thread_time = 0
        self.reset = True
        self.schedule_list = []
        # self.process_pool.map_async()

    def main_schedule(self):
        while True:
            now = datetime.now()
            if self.reset:
                db = AnimeDataBase(DB_PATH)
                self.schedule_list = []
                for work in ProcessingSubscriptionTable(db).getSearchResult():
                    self.schedule_list.append(SubscriptionItem(work))
                self.reset = False
                break
            for item in self.schedule_list:
                if item.next_time <= now:
                    self.run_time_up_work(item)
            time.sleep(ERROR_RETRY_SPAN*3600)

    def run_time_up_work(self, item: SubscriptionItem):
        if item.type == "download":
            if item.origin.get("totalEpisodes", -1) < item.origin.get("nextUpdateEP", 0):
                return False
            db = AnimeDataBase(DB_PATH)
            name = ProcessingNameTable(db).getSearchResult(item.id)[0].get("name", "Unknown")
            download_info = ProcessingDownloadTable(db).getSearchResult(item.id)[0]
            db.__del__()
            if download_info.get("download_way", "") == "way_aria2":
                journal_write(f"Executing Subscription:'{name}'.")
                result_list = get_result_from_jackett(name, filter_dict=FILTER_DICTS.get(
                    download_info.get("filter", "default"),
                    {"episode": "0", "reject_rules": [], "including_rules": []}))
                journal_write(
                    f"Find {len(result_list)} matches of '{name}' from jackett. Automatic Select best-matched one to download.")
                is_sent = send_download_info_to_aria2(result_list[0], download_info.get('directory', ""))
                if is_sent:
                    journal_write(f"Subscription '{name}' has been successfully push to Aria2.")
                    db = AnimeDataBase(DB_PATH)
                    ProcessingSubscriptionTable(DB_PATH).update(item.id, lastUpdateTime=datetime.now(),
                                                                lastUpdateEP=item.origin.get("lastUpdateEP", -2) + 1,
                                                                nextUpdateTime=item.origin.get("lastUpdateTime",datetime.now()
                                                                                               + timedelta(hours=0 - item.span))
                                                                               + timedelta(hours=item.span),
                                                                nextUpdateEP=item.origin.get("lastUpdateEP", -3) + 2)
                    item.nextTime = item.nextTime + timedelta(hours=item.span)
                    db.__del__()
                    return True
                else:
                    journal_write(f"Subscription '{name}' failed. Retry after {ERROR_RETRY_SPAN} hours.")
                    item.nextTime = item.nextTime + timedelta(hours=ERROR_RETRY_SPAN)
                    return False

        pass

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
