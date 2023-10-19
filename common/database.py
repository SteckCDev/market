import os
import sqlite3
from typing import Any
from contextlib import closing


class DatabaseSQLite:
    def __init__(self, path: str):
        self.__path = path

    def check_existence(self):
        if not os.path.exists(self.__path):
            raise ValueError(f"По пути '{self.__path}' базы не найдено")

    def query(self, query: str, parameters=()) -> Any:
        commit_and_no_result = ("INSERT" in query) or ("UPDATE" in query) or ("DELETE" in query)

        with closing(sqlite3.connect(self.__path)) as connection:
            with closing(connection.cursor()) as cursor:
                if commit_and_no_result:
                    cursor.execute(query, parameters)
                    connection.commit()

                    result = True
                else:
                    result = cursor.execute(query, parameters).fetchall()

        return result
