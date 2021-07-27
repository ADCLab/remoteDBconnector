from sshtunnel import SSHTunnelForwarder
from os.path import isfile
from configparser import ConfigParser
from pymysql import connect


class remoteDBconnector(object):
    def __init__(self,configFile=None):
        if configFile is not None:
            config = ConfigParser(configFile)
            if config['tunnel']['use']:
                self.createTunnel(config['tunnel']['remoteAddress'], 
                                  config['tunnel']['remoteUser'],
                                  config['tunnel']['remotePassword'],
                                  config['tunnel']['localPort'],
                                  config['tunnel']['remotePort'])
            if config['DB']['type']=='mysql':
                self.createSQL(config['DB']['hostAddress'],
                               config['DB']['hostPort'],
                               config['DB']['schema'],
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
            print('Tunnel is already running.')
            return -1
                

    def closeTunnel(self): 
        self.tunnel.close()
    
    
    def createSQL(self, hostAddress='127.0.0.1',hostPort=3306,schema=None,username=None,password=None):
        self.conn= connect(user=username,
                           password=password,
                           host=hostAddress,
                           db=schema,
                           port=hostPort)
        