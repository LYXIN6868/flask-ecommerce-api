import os

from dotenv import load_dotenv

load_dotenv()

mysqlConf = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "flask_shop"),
}

serverConf = {
    "host": os.getenv("SERVER_HOST", "127.0.0.1"),
    "port": int(os.getenv("SERVER_PORT", "8081")),
}

jwtConf = {
    "key": os.getenv("JWT_KEY", "please-change-this-key"),
    "timeout": int(os.getenv("JWT_TIMEOUT", "120")),
}
