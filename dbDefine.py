# -*-coding:utf-8-*-
# @author xy
# @func a basic database interface declare

import sys
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtCore import *
from GLOBAL_DEFINE import *


class AnimeDataBase:
    def __init__(self, dbpath: str):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dbpath)
        if not self.db.open():
            raise DBFailedException
        # self.query=QSqlQuery(self.db)

    def __createDB__(self) -> bool:
        # manipulating current db file
        query = QSqlQuery(self.db)
        # make db as empty
        query.exec("SELECT * FROM nameTable;")
        if query.next():
            raise DBFailedException("WARNING:THE DB IS NOT EMPTY, EMERGENT THROW!")
            return False
        else:
            query.exec("select * from sqlite_master where type = 'table'; ")
            while(query.next()):
                query.exec("drop table "+query.value(0))
        # create an id-name Table for basic usage
        query.exec("create table nameTable("
                   "id int primary key,"
                   "name varchar(255) not null)")
        # create metadata table, for display usage
        query.exec("create table metadataTable"
                   "("
                   "id int primary key,"
                   "img blob,"
                   "info text,"
                   "AnimeDBid character(10)"
                   ")")
        # create download-related table, for downloader layer
        query.exec("create table downloadTable("
                   "id int primary key,"
                   "source text,"
                   "directory text"
                   "downloadway character(10)"
                   ")")
        # create subscription table, for subscription layer
        query.exec("create table subscriptionTable("
                   "id int primary key,"
                   "starttime text,"
                   "totalEpisodes int,"
                   "lastUpdateTime text,"
                   "lastUpdateEP int,"
                   "nextUpdateTime text,"
                   "nextUpdateEP int"
                   ")")
        # create category map, for displaying multiple categories
        ### NOTICE: This table need to be updated by specific functions. ###
        query.exec("create table categoryMap(id int primary key)")
        # check if table was created
        return self.isTableExists("nameTable") and self.isTableExists("metadataTable") and self.isTableExists(
            "downloadTable") and self.isTableExists("subscriptionTable") and self.isTableExists("categoryMap")

    def processingDB(self, sql: str):
        query = QSqlQuery(self.db)
        query.exec(sql)
        return query

    def isTableExists(self, tablename: str):
        query = QSqlQuery(self.db)
        query.exec("select * from sqlite_master where type = 'table' and name='%s'" % tablename)
        return query.next()

    def __del__(self):
        self.db.close()


class DBFailedException(Exception):
    def __init__(self, msg="Could not open the given db."):
        super(DBFailedException, self).__init__()
        self.msg = msg

    def __str__(self):
        return self.msg


if __name__ == "__main__":
    a = AnimeDataBase("./test.sqlite")
    print(a.__createDB__())
    print(a.isTableExists("nameTable"), a.isTableExists("metadataTable"), a.isTableExists(
        "downloadTable"), a.isTableExists("subscriptionTable"), a.isTableExists("categoryMap"))
