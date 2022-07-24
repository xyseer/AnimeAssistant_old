from GLOBAL_DEFINE import *
from schedule_work import ScheduleWork


def main():
    try:
        app_init()
    except Exception as e:
        print(e)
        exit(-1)
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


if __name__ == "__main__":
    main()

