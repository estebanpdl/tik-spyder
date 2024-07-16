# -*- coding: utf-8 -*-

# import modules
import os
import time
import json
import sqlite3

# SQL submodules
from sqlite3 import Error

# typing
from typing import List, Optional

# Database Manager utilities
from .utilities import sanitize_output_path, get_items_from_data


# SQLDatabaseManager class
class SQLDatabaseManager:
    '''
    SQLDatabaseManager

    This class provides an abstracted interface for interacting with a SQL
    database.
    '''
    def __init__(self, output: str) -> None:
        '''
        Initializes the SQLDatabaseManager with the given output path.

        :param output: The directory path where the database file will be
            created.
        '''
        self.output = sanitize_output_path(output)
        self.sql_database_file = f'{self.output}/database.sql'

        # create required SQL tables for data processing
        self.create_search_results_table()
    
    def create_sql_connection(self) -> Optional[sqlite3.Connection]:
        '''
        Creates a SQL connection.

        :return: A SQLite connection object or None if an error occurred
        '''
        try:
            conn = sqlite3.connect(self.sql_database_file)
            return conn
        except Error as e:
            print (f'An error occurred: {e}')
            return None
    
    def create_search_results_table(self) -> None:
        '''
        Creates the query_search_results table if it does not already exist.
        '''
        # set cursor
        conn = self.create_sql_connection()
        if conn is not None:
            cursor = conn.cursor()

            try:
                cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS query_search_results (
                        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        source TEXT,
                        title TEXT,
                        snippet TEXT,
                        link TEXT,
                        thumbnail TEXT,
                        video_link TEXT,
                        snippet_highlighted_words TEXT,
                        displayed_link TEXT
                    );
                    '''
                )

                # commit changes
                conn.commit()
            except Error as e:
                print (f'An error occurred: {e}')
            finally:
                conn.close()
        else:
            print ('Failed to create the database connection.')
    
    def insert_search_results(self, data: List) -> None:
        '''
        Inserts data into the query_search_results table.

        :param data: A list of dictionaries containing the data to insert.
        '''
        conn = self.create_sql_connection()
        if conn is not None:
            cursor = conn.cursor()

            try:
                for entry in data:
                    cursor.execute(
                        '''
                        INSERT INTO query_search_results (
                            source, title, snippet, link, thumbnail,
                            video_link, snippet_highlighted_words,
                            displayed_link
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''',
                        get_items_from_data(entry)
                    )

                    # commit changes
                    conn.commit()
                
                                
                
                # TEMP -> SAVE RESPONSE
                stamp = int(time.time())
                obj = json.dumps(data, ensure_ascii=False, indent=2)
                temp_path = 'D:/i/dfrlab/osint-tools/tikspyder-test-data'
                writer = open(
                    f'{temp_path}/d_{stamp}.json',
                    encoding='utf-8',
                    mode='w'
                )
                writer.write(obj)
                writer.close()

            

            except Error as e:
                print (f'An error occurred while inserting data: {e}')
            finally:
                conn.close()
        else:
            print ('Failed to create the database connection.')

