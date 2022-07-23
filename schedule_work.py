import time
from GLOBAL_DEFINE import *
from multiprocessing import Pool, Process, Queue
from datetime import timedelta
from bind_jackett import get_result_from_jackett
from aria2_tools import send_download_info_to_aria2


class ScheduleWork:
    def __init__(self, core_nums):
        self.process_pool = Pool(core_nums)
        #self.thread_time = 0
        self.reset = True
        self.schedule_list = []
        # self.process_pool.map_async()

    def main_schedule(self):
        while True:
            now=datetime.now()
            if self.reset:
                db=AnimeDataBase(DB_PATH)
                db.processingDB("SELECT * FROM ")
                self.schedule_list = []
                self.reset = False
                break
            for item in self.schedule_list:
                if item.next_time>=now:
                    self.run_time_up_work((item,))
                    item.next_time=item.next_time+timedelta(hours=item.span)
                pass

    def run_time_up_work(self,args):
        if args[0].get("download_way","")=="way_aria2":
            journal_write(f"Executing Subscription:'{args[0].get('name')}'.")
            result_list=get_result_from_jackett()
            journal_write(f"Find {len(result_list)} matches of '{args[0].get('name')}' from jackett. Automatic Select best-matched one to download.")
            is_sent=send_download_info_to_aria2(result_list[0],args[0].get('directory',""))
            if is_sent:
                journal_write(f"Subscription '{args[0].get('name')}' has been successfully push to Aria2.")


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
