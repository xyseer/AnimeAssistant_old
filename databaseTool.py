# -*-coding:utf-8-*-
# @author xy
# @func more detail functions for different application

from dbDefine import *
from GLOBAL_DEFINE import datetime, DB_TIME_FORMAT


class ProcessingNameTable:
    def __init__(self, anime_db: AnimeDataBase):
        self.__anime_db__ = anime_db

    # Part 0: Common method

    def processingDB(self, sql: str) -> QSqlQuery:
        if not sql.endswith(";"):
            sql += ";"
        return self.__anime_db__.processingDB(sql)

    def getLastValidID(self) -> int:
        valid = 1
        query = self.processingDB("SELECT id FROM nameTable GROUP BY id HAVING MAX(id)")
        while query.next():
            valid = query.value(0) + 1
        return valid

    @staticmethod
    def getResultFromQuery(query: QSqlQuery) -> list:
        result = []
        # get results from query, change it into a list of dictionary
        while query.next():
            result.append({"id": int(query.value("id")),
                           "name": str(query.value("name"))})
        return result

    # Part 1: ADD

    def writeDB(self, name: str, table_id: int = -1) -> bool:
        if table_id <= 0:
            table_id = self.getLastValidID()
        sql = "INSERT INTO nameTable (id,name) " \
              "VALUES (" + str(table_id) + ",'" + name + "') ;"
        self.processingDB(sql)
        return self.isInNameTable(name)

    # Part 2: SEARCH

    def __searchInNameTable(self, name: str = "", table_id: int = -1) -> QSqlQuery:
        sql = "SELECT * " \
              "FROM nameTable " \
              "WHERE "
        if name != "":
            if table_id <= 0:
                sql += "name='" + name + "';"
            else:
                sql += "name='" + name + "' and id=" + str(table_id) + ";"
        else:
            if table_id <= 0:
                return QSqlQuery(None)
            else:
                sql += "id=" + str(table_id) + ";"
        return self.processingDB(sql)

    def isInNameTable(self, name: str = "", table_id: int = -1) -> bool:
        return self.__searchInNameTable(name, table_id).next()

    def getSearchResult(self, name: str = "", table_id: int = -1) -> list:
        # get results from query, change it into a list of dictionary
        return self.getResultFromQuery(self.__searchInNameTable(name, table_id))

    # Part 3: DELETE

    # multi-delete function
    def deleteFromNameTableByResult(self, result: list) -> int:
        count = 0
        for item in result:
            table_id = item.get("id", -1)
            if table_id > 0:
                count += self.deleteFromNameTableByID(table_id=table_id)
        return count

    # primary-delete
    '''
        Notice: It doesn't support delete by name in order to avoid more than one items 
        with the same name will be all deleted. If you are sure you need to do so, you
        can delete them by using the one for multi-deleting.
    '''

    def deleteFromNameTableByID(self, table_id: int = -1) -> int:
        if table_id > 0:
            isEmpty = False
            for table_name in self.__anime_db__.getAllTables():
                isEmpty = isEmpty and self.processingDB(
                    "SELECT * FROM %s WHERE id=%s;" % (table_name, str(table_id))).next()
            if isEmpty:
                sql = "DELETE FROM nameTable WHERE id=" + str(table_id) + " ;"
                self.processingDB(sql)
            if not self.isInNameTable(table_id=table_id):
                return 1
            else:
                return 0
        else:
            return 0

    # Part 4: UPDATE
    def update(self, table_id: int, new_name: str) -> bool:
        sql = "UPDATE nameTable set name='" + new_name + "' where id=" + str(table_id) + " ;"
        self.processingDB(sql)
        return self.isInNameTable(new_name, table_id)


class ProcessingMetaDataTable:
    def __init__(self, anime_db: AnimeDataBase):
        self.__anime_db__ = anime_db

    # Part 0: Common method

    def processingDB(self, sql: str) -> QSqlQuery:
        if not sql.endswith(";"):
            sql += ";"
        return self.__anime_db__.processingDB(sql)

    @staticmethod
    def getResultFromQuery(query: QSqlQuery) -> list:
        result = []
        # get results from query, change it into a list of dictionary
        while query.next():
            result.append({"id": int(query.value("id")),
                           "img": str(query.value("img")),
                           "info": str(query.value("info")),
                           "AnimeDBid": str(query.value("AnimeDBid"))})
        return result

    # Part 1: ADD

    def writeDB(self, table_id: int, img: str, info: str) -> bool:
        if table_id <= 0:
            return False
        sql = f"INSERT INTO metadataTable (id,img,info) " \
              f"VALUES ({table_id},'{img}','{info}') ;"
        self.processingDB(sql)
        return self.isInMetadataTable(table_id)

    # Part 2: SEARCH

    def __searchInMetadataTable(self, table_id: int = -1) -> QSqlQuery:
        sql = "SELECT * " \
              "FROM metadataTable "
        if table_id > 0:
            sql += f"WHERE id={table_id}"
        return self.processingDB(sql)

    def isInMetadataTable(self, table_id: int = -1) -> bool:
        return self.__searchInMetadataTable(table_id).next()

    def getSearchResult(self, table_id: int = -1) -> list:
        # get results from query, change it into a list of dictionary
        return self.getResultFromQuery(self.__searchInMetadataTable(table_id))

    # Part 3: DELETE

    # multi-delete function
    def deleteFromMetadataTableByResult(self, result: list) -> int:
        count = 0
        for item in result:
            table_id = item.get("id", -1)
            if table_id > 0:
                count += self.deleteFromMetadataTableByID(table_id=table_id)
        return count

    # primary-delete
    '''
        Notice: It doesn't support delete by name in order to avoid more than one items 
        with the same name will be all deleted. If you are sure you need to do so, you
        can delete them by using the one for multi-deleting.
    '''

    def deleteFromMetadataTableByID(self, table_id: int = -1) -> int:
        if table_id > 0:
            sql = "DELETE FROM metadataTable WHERE id=" + str(table_id) + " ;"
            self.processingDB(sql)
            if not self.isInMetadataTable(table_id=table_id):
                return 1
            else:
                return 0
        else:
            return 0

    # Part 4: UPDATE
    def update(self, table_id: int, img: str = "", info: str = "") -> bool:
        if img:
            sql = f"UPDATE metadataTable set img='{img}' where id={table_id} ;"
            self.processingDB(sql)
        if info:
            sql = f"UPDATE metadataTable set info='{info}' where id={table_id} ;"
            self.processingDB(sql)
        return self.isInMetadataTable(table_id)


class ProcessingDownloadTable:
    def __init__(self, anime_db: AnimeDataBase):
        self.__anime_db__ = anime_db

    # Part 0: Common method

    def processingDB(self, sql: str) -> QSqlQuery:
        if not sql.endswith(";"):
            sql += ";"
        return self.__anime_db__.processingDB(sql)

    @staticmethod
    def getResultFromQuery(query: QSqlQuery) -> list:
        result = []
        # get results from query, change it into a list of dictionary
        while query.next():
            result.append({"id": int(query.value("id")),
                           "source": str(query.value("source")),
                           "directory": str(query.value("directory")),
                           "downloadway": str(query.value("downloadway")),
                           "filter": str(query.value("filter"))
                           })
        return result

    # Part 1: ADD

    def writeDB(self, table_id: int, source: str, directory: str, downloadway: str, filter_name: str) -> bool:
        if table_id <= 0:
            return False
        sql = f"INSERT INTO downloadTable (id,source,directory,downloadway,filter) " \
              f"VALUES ({table_id},'{source}','{directory}','{downloadway}','{filter_name}') ;"
        self.processingDB(sql)
        return self.isInDownloadTable(table_id)

    # Part 2: SEARCH

    def __searchInDownloadTable(self, table_id: int = -1, downloadway: str = "") -> QSqlQuery:
        sql = "SELECT * " \
              "FROM downloadTable "
        if table_id > 0:
            sql += f"WHERE id={table_id}"
            if downloadway:
                sql += f" and downloadway='{downloadway}'"
        else:
            if downloadway:
                sql += f"WHERE downloadway='{downloadway}'"
        return self.processingDB(sql)

    def isInDownloadTable(self, table_id: int = -1) -> bool:
        return self.__searchInDownloadTable(table_id).next()

    def getSearchResult(self, table_id: int = -1) -> list:
        # get results from query, change it into a list of dictionary
        return self.getResultFromQuery(self.__searchInDownloadTable(table_id))

    # Part 3: DELETE

    # multi-delete function
    def deleteFromDownloadTableByResult(self, result: list) -> int:
        count = 0
        for item in result:
            table_id = item.get("id", -1)
            if table_id > 0:
                count += self.deleteFromDownloadTableByID(table_id=table_id)
        return count

    # primary-delete
    '''
        Notice: It doesn't support delete by name in order to avoid more than one items 
        with the same name will be all deleted. If you are sure you need to do so, you
        can delete them by using the one for multi-deleting.
    '''

    def deleteFromDownloadTableByID(self, table_id: int = -1) -> int:
        if table_id > 0:
            sql = "DELETE FROM downloadTable WHERE id=" + str(table_id) + " ;"
            self.processingDB(sql)
            if not self.isInDownloadTable(table_id=table_id):
                return 1
            else:
                return 0
        else:
            return 0

    # Part 4: UPDATE
    def update(self, table_id: int, source: str = "", directory: str = "", downloadway: str = "",
               filter_name: str = "") -> bool:
        if source:
            sql = f"UPDATE downloadTable set source='{source}' where id={table_id} ;"
            self.processingDB(sql)
        if directory:
            sql = f"UPDATE downloadTable set directory='{directory}' where id={table_id} ;"
            self.processingDB(sql)
        if downloadway:
            sql = f"UPDATE downloadTable set downloadway='{downloadway}' where id={table_id} ;"
            self.processingDB(sql)
        if filter_name:
            sql = f"UPDATE downloadTable set filter='{filter_name}' where id={table_id} ;"
            self.processingDB(sql)
        return self.isInDownloadTable(table_id)


class ProcessingSubscriptionTable:
    def __init__(self, anime_db: AnimeDataBase):
        self.__anime_db__ = anime_db

    # Part 0: Common method

    def processingDB(self, sql: str) -> QSqlQuery:
        if not sql.endswith(";"):
            sql += ";"
        return self.__anime_db__.processingDB(sql)

    @staticmethod
    def getResultFromQuery(query: QSqlQuery) -> list:
        result = []
        # get results from query, change it into a list of dictionary
        while query.next():
            result.append({"id": int(query.value("id")),
                           "starttime": datetime.strptime(str(query.value("starttime")), DB_TIME_FORMAT),
                           "totalEpisodes": int(query.value("totalEpisodes")),
                           "lastUpdateTime": datetime.strptime(str(query.value("lastUpdateTime")), DB_TIME_FORMAT),
                           "lastUpdateEP": int(query.value("lastUpdateEP")),
                           "nextUpdateTime": datetime.strptime(str(query.value("nextUpdateTime")), DB_TIME_FORMAT),
                           "nextUpdateEP": int(query.value("nextUpdateEP")),
                           "span": int(query.value("span")),
                           "type": str(query.value("type"))
                           })
        return result

    # Part 1: ADD

    def writeDB(self, table_id: int, starttime: datetime, totalEpisodes: int, lastUpdateTime: datetime,
                lastUpdateEP: int, nextUpdateTime: datetime, nextUpdateEP: int, span: int, type_name: str) -> bool:
        if table_id <= 0:
            return False
        sql = f"INSERT INTO subscriptionTable (id,starttime,totalEpisodes,lastUpdateTime,lastUpdateEP,nextUpdateTime," \
              f"nextUpdateEP,span,type) " \
              f"VALUES ({table_id},'{starttime.strftime(DB_TIME_FORMAT)}',{totalEpisodes}," \
              f"'{lastUpdateTime.strftime(DB_TIME_FORMAT)}',{lastUpdateEP},'{nextUpdateTime.strftime(DB_TIME_FORMAT)}'," \
              f"{nextUpdateEP},{span},'{type_name}') ; "
        self.processingDB(sql)
        return self.isInSubscriptionTable(table_id)

    # Part 2: SEARCH

    def __searchInSubscriptionTable(self, table_id: int = -1, nextUpdateTime: datetime = None) -> QSqlQuery:
        sql = "SELECT * " \
              "FROM subscriptionTable "
        if table_id > 0:
            sql += f"WHERE id={table_id}"
        else:
            if nextUpdateTime is not None:
                sql += f"WHERE nextUpdateTime='{nextUpdateTime.strftime(DB_TIME_FORMAT)}'"
        return self.processingDB(sql)

    def isInSubscriptionTable(self, table_id: int = -1) -> bool:
        return self.__searchInSubscriptionTable(table_id).next()

    def getSearchResult(self, table_id: int = -1) -> list:
        # get results from query, change it into a list of dictionary
        return self.getResultFromQuery(self.__searchInSubscriptionTable(table_id))

    # Part 3: DELETE

    # multi-delete function
    def deleteFromDownloadTableByResult(self, result: list) -> int:
        count = 0
        for item in result:
            table_id = item.get("id", -1)
            if table_id > 0:
                count += self.deleteFromDownloadTableByID(table_id=table_id)
        return count

    # primary-delete
    '''
        Notice: It doesn't support delete by name in order to avoid more than one items 
        with the same name will be all deleted. If you are sure you need to do so, you
        can delete them by using the one for multi-deleting.
    '''

    def deleteFromDownloadTableByID(self, table_id: int = -1) -> int:
        if table_id > 0:
            sql = "DELETE FROM subscriptionTable WHERE id=" + str(table_id) + " ;"
            self.processingDB(sql)
            if not self.isInSubscriptionTable(table_id=table_id):
                return 1
            else:
                return 0
        else:
            return 0

    # Part 4: UPDATE
    def update(self, table_id: int, starttime: datetime = None, totalEpisodes: int = -1,
               lastUpdateTime: datetime = None,
               lastUpdateEP: int = -1, nextUpdateTime: datetime = None, nextUpdateEP: int = -1, span: int = -1) -> bool:
        if starttime is not None:
            sql = f"UPDATE subscriptionTable set starttime='{starttime.strftime(DB_TIME_FORMAT)}' where id={table_id} ;"
            self.processingDB(sql)
        if totalEpisodes > 0:
            sql = f"UPDATE subscriptionTable set totalEpisodes={totalEpisodes} where id={table_id} ;"
            self.processingDB(sql)
        if lastUpdateTime is not None:
            sql = f"UPDATE subscriptionTable set lastUpdateTime='{lastUpdateTime.strftime(DB_TIME_FORMAT)}' where id={table_id} ;"
            self.processingDB(sql)
        if lastUpdateEP > 0:
            sql = f"UPDATE subscriptionTable set lastUpdateEP={lastUpdateEP} where id={table_id} ;"
            self.processingDB(sql)
        if nextUpdateTime is not None:
            sql = f"UPDATE subscriptionTable set nextUpdateTime='{nextUpdateTime.strftime(DB_TIME_FORMAT)}' where id={table_id} ;"
            self.processingDB(sql)
        if nextUpdateEP > 0:
            sql = f"UPDATE subscriptionTable set nextUpdateEP={nextUpdateEP} where id={table_id} ;"
            self.processingDB(sql)
        if span > 0:
            sql = f"UPDATE subscriptionTable set span={span} where id={table_id} ;"
            self.processingDB(sql)
        return self.isInSubscriptionTable(table_id)


class ProcessCategoryMap:
    def __init__(self, anime_db: AnimeDataBase):
        self.__anime_db__ = anime_db

    # Part 0: Common method

    def processingDB(self, sql: str) -> QSqlQuery:
        if not sql.endswith(";"):
            sql += ";"
        return self.__anime_db__.processingDB(sql)

    def add_cate(self, cate_name: str) -> bool:
        if cate_name in self.get_columns_name():
            return True
        else:
            self.processingDB(f"ALTER TABLE categoryMap ADD COLUMN {cate_name} Integer")
            self.processingDB(f"UPDATE categoryMap set {cate_name}=0")
            return True

    def get_columns_num(self):
        query = self.processingDB('pragma table_info("categoryMap")')
        amount = 0
        while query.next():
            amount += 1
        print(amount)
        return amount

    def get_columns_name(self):
        name_list = []
        query = self.processingDB('pragma table_info("categoryMap")')
        while query.next():
            name_list.append(str(query.value("name")))
        name_list.remove("id")
        return name_list

    def getSingleResultFromQuery(self, query: QSqlQuery) -> list:
        result = []
        if query.next():
            for name in self.get_columns_name():
                if int(query.value(name)) == 1:
                    result.append(name)
                else:
                    continue
        return result

    def writeDB(self, table_id: int, cate_list: list):
        for cate in cate_list:
            self.add_cate(cate)
        self.processingDB(f"INSERT INTO categoryMap(id) VALUES({table_id})")
        for name in self.get_columns_name():
            if name in cate_list:
                self.processingDB(f"UPDATE categoryMap set {name}={1} where id={table_id}")
            else:
                self.processingDB(f"UPDATE categoryMap set {name}={0} where id={table_id}")
        return self.isInCategoryMap(table_id)

    def __searchInCategoryMap(self, table_id: int):
        if table_id > 0:
            return self.processingDB(f"SELECT * FROM categoryMap WHERE id={table_id}")
        else:
            return self.processingDB(f"SELECT * FROM categoryMap")

    def isInCategoryMap(self, table_id: int):
        return self.__searchInCategoryMap(table_id).next()

    def getSearchResult(self, table_id: int = -1, cate_list: list = None):
        if cate_list is None:
            cate_list = []
        if table_id <= 0:
            if not cate_list:
                return self.get_columns_name()
        if not cate_list:
            return self.getSingleResultFromQuery(self.__searchInCategoryMap(table_id))
        sql = "select id from categoryMap where "
        if table_id > 0:
            sql += f"id={table_id} and "
        for name in cate_list:
            sql += f"{name}=1 and "
        result = []
        query = self.processingDB(sql[0:-4])
        while query.next():
            result.append(int(query.value("id")))
        return result

    def deleteFromCategoryMap(self, table_id: int = -1):
        if table_id > 0:
            self.processingDB(f"DELETE FROM categoryMap WHERE id={table_id}")
        if not self.isInCategoryMap(table_id):
            return 1
        else:
            return 0

    def updateMap(self, table_id: int = -1, cate_list: list = None):
        if cate_list is None:
            cate_list = []
        for cate in cate_list:
            self.add_cate(cate)
        if table_id > 0:
            for name in self.get_columns_name():
                if name in cate_list:
                    self.processingDB(f"UPDATE categoryMap set {name}={1} where id={table_id}")
                else:
                    self.processingDB(f"UPDATE categoryMap set {name}={0} where id={table_id}")
        return self.isInCategoryMap(table_id)


if __name__ == "__main__":
    pass
    # a = AnimeDataBase("./test.sqlite")
    # print(ProcessCategoryMap(a).get_columns_name())
    # b = ProcessingNameTable(a)
    # print(b.writeDB("Slime"))
    # print(b.writeDB("Slime"))
    # print(b.getSearchResult("Slime"))
    # # print(b.getLastValidID())
    # print("update", b.update(2, "aha"))
    # print(b.deleteFromNameTableByResult(b.getSearchResult("slime")))
    # for i in range(0,50):
    #     b.deleteFromNameTableByResult(b.getSearchResult(table_id=i))
    # for name in a.getAllTables():
    #     print(name + ":")
    #     print(b.getResultFromQuery(b.processingDB("select * from " + name)))
