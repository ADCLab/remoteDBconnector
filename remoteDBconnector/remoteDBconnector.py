from sshtunnel import SSHTunnelForwarder
from configparser import ConfigParser
from pymysql import connect
from pymongo import MongoClient

class dbconn(object):
    def __init__(self,configFile=None):
        if configFile is not None:
            config = ConfigParser(allow_no_value=True)
            config.read(configFile)

            if bool(config['tunnel']['use'])==True:
                self.createTunnel(config['tunnel']['remoteAddress'], 
                                  config['tunnel']['remoteUser'],
                                  config['tunnel']['remotePassword'],
                                  int(config['tunnel']['localPort']),
                                  int(config['tunnel']['remotePort']))
            if config['DB']['type']=='mysql':
                self.createSQL(config['DB']['hostAddress'],
                               int(config['DB']['hostPort']),
                               config['DB']['db'],
                               config['DB']['username'],
                               config['DB']['password'],
                               )
            elif config['DB']['type']=='mongo':
                self.createMongo(config['DB']['hostAddress'],
                               int(config['DB']['hostPort']),
                               config['DB']['db'],
                               config['DB']['username'],
                               config['DB']['password'],
                               )                
            
        
        
    def createTunnel(self,remoteAddress,remoteUser,remotePassword,localPort=3333,remotePort=3306):
        self.tunnel = SSHTunnelForwarder(
        remoteAddress,
        ssh_username=remoteUser,
        ssh_password=remotePassword,
        local_bind_address=('127.0.0.1', localPort),
        remote_bind_address=('127.0.0.1', remotePort))   
        try:
            self.tunnel.start()
            return True
        except:
            print('Check if a tunnel is already running.')
            print('Check for internet access.')
            print('Check VPN status.')
            return -1
                    
    def createSQL(self, hostAddress='127.0.0.1',hostPort=3306,db=None,username=None,password=None):
        self.conn = connect(user=username,
                           password=password,
                           host=hostAddress,
                           db=db,
                           port=hostPort)

    def createMongo(self, hostAddress='127.0.0.1',hostPort=27017,db='Admin',username=None,password=None):
        self.conn = MongoClient(host=hostAddress,
                                              authSource=db,
                                              port=hostPort,
                                              username=username,
                                              password=password,
                                              authMechanism='SCRAM-SHA-256')
        
    def closeTunnel(self): 
        if hasattr(self,'tunnel') and  self.tunnel.is_active:
            self.tunnel.close()

    def closeDB(self): 
        if hasattr(self,'conn') and self.conn.open:
            self.conn.close()

    def closeAll(self): 
        self.closeDB()
        self.closeTunnel()
        
    def __del__(self):
        self.closeAll()
        print("deleted")
