import json

def get_config():
	f = open("./config/config.json",'rb')
	config_json = json.load(f)
	return config_json

def get_db_config(config_json):
	db_config = "mysql"
	if config_json['mysql_actuation'] == "mysql-python":
		db_config = db_config + "://"
	else:
		db_config = db_config + str(config_json['mysql_actuation']) + "://"

	if config_json["mysql_pass"] == "":
		db_config = db_config + str(config_json["mysql_user"])+"@" + str(config_json["mysql_host"]) + ":" + str(config_json["mysql_port"]) + "/" + str(config_json["mysql_dbname"])
 	else:
 		db_config = db_config + str(config_json["mysql_user"]) + ":" + str(config_json["mysql_pass"]) +  "@" + str(config_json["mysql_host"]) + ":" + str(config_json["mysql_port"]) + "/" + str(config_json["mysql_dbname"])
 	return db_config


#'mysql://root@localhost:3306/facepath'
config_json = get_config()

PORT = config_json['port']
LISTEN = str(config_json['listen'])

DB_CONFIG = get_db_config(config_json)
DB_TABLE = str(config_json["mysql_dbtable"])

UPLOAD_FOLDER = 'pictures'
API_KEY = 'pre_key'
TOKEN_LIFE = 30 * 24 * 3600
MAX_PATH_LENGTH = 128
SECRET_KEY = 'never ever'