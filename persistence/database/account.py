from .util import PostgresQueryExecutor


async def add(username: str, pass_hash: str) -> int:
    id_,  = await PostgresQueryExecutor(
        sql=fr'INSERT INTO account'
            fr'            (username, pass_hash, role, real_name, student_id)'
            fr'     VALUES (%(username)s, %(pass_hash)s, %(role)s, %(real_name)s, LOWER(%(student_id)s))'
            fr'  RETURNING id',
        username=username, pass_hash=pass_hash, role='role', real_name='real_name', student_id='student_id', fetch=1,
    ).execute()
    return id_
