import toml


class Config:
    __PATH = None
    __JSON_PATH = None
    __TOKEN = None
    __PERIOD = None
    __TIMEZONE = None
    __ADMINS = None 

    def __init__(self, path):
        self.__PATH = path
        with open(path, 'r') as fp:
            cfg_dict = toml.load(fp)
        self.__JSON_PATH = cfg_dict['json_path']
        self.__TOKEN = cfg_dict['token']
        self.__PERIOD = cfg_dict['period']
        self.__TIMEZONE = cfg_dict['timezone']
        self.__ADMINS = cfg_dict['admins']

    @property
    def json_path(self):
        return self.__JSON_PATH
   
    @property
    def token(self):
        return self.__TOKEN

    @property
    def period(self):
        return self.__PERIOD

    @property
    def timezone(self):
        return self.__TIMEZONE
    
    @property
    def admins(self):
        return self.__ADMINS


config = Config('config.toml')
