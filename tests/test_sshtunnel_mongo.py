from remoteDBconnector import dbconn
import pandas


mytunnel=dbconn('myconfexample_mongo.cfg')
# a=pandas.read_sql('SHOW databases;',mytunnel.conn)

for coll in mytunnel.conn.list_databases():
    print(coll)
    
    
mytunnel.closeAll()
