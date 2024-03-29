from dataclasses import dataclass

from fastapi import APIRouter, Depends, responses
from pydantic import BaseModel

import app.exceptions as exc
import app.persistence.database as db
from app.middleware.headers import get_auth_token
from app.utils.security import encode_jwt, hash_password, verify_password

router = APIRouter(
    tags=['Account'],
    default_response_class=responses.JSONResponse,
    dependencies=[Depends(get_auth_token)],
)


class AddAccountInput(BaseModel):
    username: str
    password: str
    real_name: str
    student_id: str


@dataclass
class AddAccountOutput:
    id: int


@router.post('/account')
async def add_account(data: AddAccountInput) -> AddAccountOutput:
    account_id = await db.account.add(
        username=data.username,
        pass_hash=hash_password(data.password),
    )

    return AddAccountOutput(id=account_id)


class LoginInput(BaseModel):
    username: str
    password: str


@dataclass
class LoginOutput:
    account_id: int
    token: str


@router.post('/login')
async def login(data: LoginInput) -> LoginOutput:
    try:
        account_id, pass_hash, role = await db.account.read_by_username(data.username)
    except TypeError:
        raise exc.LoginFailed

    if not verify_password(data.password, pass_hash):
        raise exc.LoginFailed

    token = encode_jwt(account_id=account_id)
    return LoginOutput(account_id=account_id, token=token)
