import json

def get_config():
	f = open("./config/config.json",'rb')
	config_json = json.load(f)
	return config_json

def get_db_config(config_json):
	db_config = "mysql+pymysql://"
	if config_json["mysql_pass"] == "":
		db_config = db_config + config_json["mysql_user"]+"@" + config_json["mysql_host"] + ":" + str(config_json["mysql_port"]) + "/" + config_json["mysql_dbname"]
 	else:
 		db_config = db_config + config_json["mysql_user"] + ":" + config_json["mysql_pass"] +  "@" + config_json["mysql_host"] + ":" + str(config_json["mysql_port"]) + "/" + config_json["mysql_dbname"]
 	return db_config


#'mysql://root@localhost:3306/facepath'
config_json = get_config()

PORT = config_json['port']
LISTEN = config_json['listen']

DB_CONFIG = get_db_config(config_json)
DB_TABLE = "users"

UPLOAD_FOLDER = 'pictures'
API_KEY = config_json["api_key"]
TOKEN_LIFE = 30 * 24 * 3600
MAX_PATH_LENGTH = 128
SECRET_KEY = 'never ever'