from base import do

from .util import PostgresQueryExecutor


async def add(s3_file: do.S3File) -> None:
    await PostgresQueryExecutor(
        sql=fr"INSERT INTO s3_file"
            fr"            (uuid, key, bucket)"
            fr"     VALUES (%(uuid)s, %(key)s, %(bucket)s)",
        uuid=s3_file.uuid, key=s3_file.key, bucket=s3_file.bucket, fetch=None,
    ).execute()
