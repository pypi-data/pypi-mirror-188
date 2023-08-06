from sqlalchemy import create_engine,dialects
import pandas as pd
import os
import logging

class PostgresConnection(object):

    def __init__(self,schema,user,password,host,port,db) -> None:
        self.__init_config_parser()
        #Create engine #dialect+driver:
        self.SCHEMAS = schema
        self.DATABASE = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
   
        #self.URL = f"postgresql+psycopg2:://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@server:port/database"

    def insert_df(self,data,table):
       
        try:
            #Insert data to table 
           data.to_sql(table, self.DATABASE, if_exists= 'append', index= False,chunksize=1000)
        except Exception as e:
            logging.error(e)
            return False
    
    # Read file configuration
    def __init_config_parser(self,user,password,host,port,db):
        self.POSTGRES_USER = user
        self.POSTGRES_PASSWORD = password
        self.POSTGRES_HOST = host
        self.POSTGRES_PORT = port
        self.POSTGRES_DB = db
