# *-encoding:utf8-*
import sys
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtCore import *
from GLOBAL_DEFINE import *


class AnimeDataBase:
    def __init__(self, dbpath: str, ):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(dbpath)
        if not self.db.open():
            raise DBFailedOpenException
        # self.query=QSqlQuery(self.db)

    def creatDB(self) -> bool:
        # manipulating current db file
        qurey = QSqlQuery(self.db)
        # make db as empty
        qurey.exec("drop table *")
        # create an id-name Table for basic usage
        qurey.exec("create table nameTable("
                   "id int primary key,"
                   "name varchar(255) not null)")
        # create metadata table, for display usage
        qurey.exec("create table metadataTable"
                   "("
                   "id int primary key,"
                   "img blob,"
                   "info text,"
                   "AnimeDBid character(10)"
                   ")")
        # create download-related table, for downloader layer
        qurey.exec("create table downloadTable("
                   "id primary key,"
                   "source text,"
                   "directory text"
                   "downloadway character(10)"
                   ")")
        # create subscription table, for subscription layer
        qurey.exec("create table subscriptionTable("
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
        qurey.exec("create table categoryMap(id int primary key)")
        # check if table was created
        return self.isTableExists("nameTable") and self.isTableExists("metadataTable") and self.isTableExists(
            "downloadTable") and self.isTableExists("subscriptionTable") and self.isTableExists("categoryMap")

    def searchDB(self, sql: str):
        query = QSqlQuery(self.db)
        query.exec(sql)

    def isTableExists(self, tablename: str):
        qurey = QSqlQuery(self.db)
        qurey.exec("select * from sqlite_master where type = 'table' and name='%s'" % tablename)
        return qurey.next()

    def __del__(self):
        self.db.close()


class DBFailedOpenException(Exception):
    def __init__(self, msg="Could not open the given db."):
        super(DBFailedOpenException, self).__init__()
        self.msg = msg

    def __str__(self):
        return self.msg


if __name__ == "__main__":
    a = AnimeDataBase("./test.sqlite")
    print(a.creatDB())
    print(a.isTableExists("nameTable"), a.isTableExists("metadataTable"), a.isTableExists(
        "downloadTable"), a.isTableExists("subscriptionTable"), a.isTableExists("categoryMap"))
