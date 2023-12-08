import mysql.connector
from mysql.connector import errorcode
from ..utils.config import settings

config = {
	'host': settings.db_host,
	'user':settings.db_user,
	'password': settings.db_password,
	'database': settings.db_name,
	'client_flags': [mysql.connector.ClientFlag.SSL],
	'ssl_ca': './ssl/DigiCertGlobalRootCA.crt (2).pem'
}

try:
	conn = mysql.connector.connect(**config)
	print("Connection established")
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with the user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
else:
	cursor = conn.cursor()