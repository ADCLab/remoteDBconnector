from remoteDBconnector import dbconn
from configparser import ConfigParser
import pandas


config = ConfigParser()
config.read('myconfexample_mysql.cfg')
mytunnel=dbconn('myconfexample_mysql.cfg')
a=pandas.read_sql('SHOW databases;',mytunnel.conn)

