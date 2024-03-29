import os
from datetime import timedelta

from dotenv import dotenv_values

env_values = {
    **dotenv_values(".env"),
    **os.environ,
}


class PGConfig:
    host = env_values.get('PG_HOST')
    port = env_values.get('PG_PORT')
    username = env_values.get('PG_USERNAME')
    password = env_values.get('PG_PASSWORD')
    db_name = env_values.get('PG_DBNAME')
    max_pool_size = int(env_values.get('PG_MAX_POOL_SIZE') or 1)


class CHConfig:
    host = env_values.get('CH_HOST')
    port = env_values.get('CH_PORT')
    username = env_values.get('CH_USERNAME')
    password = env_values.get('CH_PASSWORD')
    db_name = env_values.get('CH_DBNAME')
    max_pool_size = int(env_values.get('CH_MAX_POOL_SIZE') or 1)


class AppConfig:
    title = env_values.get('APP_TITLE')
    docs_url = env_values.get('APP_DOCS_URL', None)
    redoc_url = env_values.get('APP_REDOC_URL', None)
    logger_name = env_values.get('APP_LOGGER_NAME', None)


class JWTConfig:
    jwt_secret = env_values.get('JWT_SECRET', 'aaa')
    jwt_encode_algorithm = env_values.get('JWT_ENCODE_ALGORITHM', 'HS256')
    login_expire = timedelta(days=float(env_values.get('LOGIN_EXPIRE', '7')))


class AMQPConfig:
    host = env_values.get('AMQP_HOST')
    port = env_values.get('AMQP_PORT')
    username = env_values.get('AMQP_USERNAME')
    password = env_values.get('AMQP_PASSWORD')


AMQP_PUBLISH_QUEUE = env_values.get('AMQP_PUBLISH_QUEUE')
AMQP_CONSUME_QUEUE = env_values.get('AMQP_CONSUME_QUEUE')


class S3Config:
    endpoint = env_values.get('S3_ENDPOINT')
    access_key = env_values.get('S3_ACCESS_KEY')
    secret_key = env_values.get('S3_SECRET_KEY')


pg_config = PGConfig()
ch_config = CHConfig()
app_config = AppConfig()
jwt_config = JWTConfig()
amqp_config = AMQPConfig()
s3_config = S3Config()
