from base import do
from base.enums import RoleType
from typing import Sequence
import exceptions as exc

import asyncpg

from .util import pyformat2psql, PostgresQueryExecutor
from . import pg_pool_handler


async def add(username: str, pass_hash: str) -> int:
    result = await PostgresQueryExecutor(
        sql=fr'INSERT INTO account'
            fr'            (username, pass_hash, role, real_name, student_id)'
            fr'     VALUES (%(username)s, %(pass_hash)s, %(role)s, %(real_name)s, LOWER(%(student_id)s))'
            fr'  RETURNING id',
        username=username, pass_hash=pass_hash, fetch=1,
    ).execute()

    try:
        id_, = result
    except asyncpg.exceptions.UniqueViolationError:
        raise exc.UniqueViolationError
    return id_


async def read(account_id: int) -> do.Account:
    result = await PostgresQueryExecutor(
        sql=fr"SELECT id, username, role, student_id, real_name"
            fr"  FROM account"
            fr" WHERE id = %(account_id)s",
        account_id=account_id, fetch=1,
    ).execute()
    try:
        id_, username, role, student_id, real_name = result
    except TypeError:
        raise exc.NotFound
    return do.Account(id=id_, username=username, role=RoleType(role),
                      student_id=student_id, real_name=real_name)


async def read_by_username(username: str) -> tuple[int, str, RoleType]:
    result = await PostgresQueryExecutor(
        sql=fr"SELECT id, pass_hash, role"
            fr"  FROM account"
            fr" WHERE username = %(username)s",
        username=username, fetch=1,
    ).execute()

    try:
        id_, pass_hash, role = result
    except TypeError:
        raise exc.NotFound
    return id_, pass_hash, RoleType(role)


async def is_duplicate_student_id(student_id: str) -> bool:
    count, = await PostgresQueryExecutor(
        sql=fr"SELECT COUNT(*) FROM account"
            fr" WHERE student_id = LOWER(%(student_id)s)",
        student_id=student_id, fetch=1,
    ).execute()
    return count > 0


async def delete(account_id: int) -> None:
    await PostgresQueryExecutor(
        sql=fr"DELETE FROM account"
            fr" WHERE id = %(account_id)s",
        account_id=account_id, fetch=None,
    ).execute()


async def browse_by_role(role: RoleType) -> Sequence[do.Account]:
    records = await PostgresQueryExecutor(
        sql=fr"SELECT id, username, role, student_id, real_name"
            fr"  FROM account"
            fr" WHERE role = %(role)s"
            fr" ORDER BY id ASC",
        role=role.value, fetch='all',
    ).execute()

    return [do.Account(id=id_, username=username, role=RoleType(role), real_name=real_name, student_id=student_id)
            for id_, username, role, real_name, student_id in records]
