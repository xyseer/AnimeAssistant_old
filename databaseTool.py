# -*-coding:utf-8-*-
# @author xy
# @func more detail functions for different application

from dbDefine import *
from PyQt5.QtSql import QSqlResult


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
        while (query.next()):
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
        result = []
        query = self.__searchInNameTable(name, table_id)
        # get results from query, change it into a list of dictionary
        while query.next():
            result.append({"id": int(query.value("id")),
                           "name": str(query.value("name"))})
        return result

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
            sql = "DELETE FROM nameTable WHERE id=" + str(table_id) + " ;"
            self.processingDB(sql)
            if not self.isInNameTable(table_id=table_id):
                return 1
            else:
                return 0
        else:
            return 0


if __name__ == "__main__":
    a = AnimeDataBase("./test.sqlite")
    b = ProcessingNameTable(a)
    print(b.writeDB("Slime"))
    print(b.getSearchResult("Slime"))
    # print(b.getLastValidID())
    input()
    print(b.deleteFromNameTableByResult(b.getSearchResult("Slime")))
    print(b.getResultFromQuery(b.processingDB("select * from nameTable")))
