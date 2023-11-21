import os
from typing import Optional

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

import crypt
from crud.database import get_session
from crud import methods as crud_methods


import dotenv

dotenv.load_dotenv()

router = APIRouter()


@router.get("/get_password/")
async def get_password(app_name: Optional[str] = None, token: Optional[str] = None, session: AsyncSession = Depends(get_session)):

    if app_name is None:
        return None
    print(os.getenv("TOKEN"))

    if token == os.getenv("TOKEN"):
        passwords = await crud_methods.GET.password(app_name, session)

        result = []
        if passwords:
            for app_name, password, key in passwords:

                result.append((app_name, crypt.decrypt(password, key)))

        return result



@router.post("/post_password/")
async def post_password(app_name: Optional[str] = None, password: Optional[str] = None, token: Optional[str] = None, session: AsyncSession = Depends(get_session)):

    if token == os.getenv("TOKEN"):
        password, key = crypt.encrypt(password)
        result = await crud_methods.POST.password(app_name, password, key, session)
        return result






@router.put("/put_password/")
async def update_password(app_name: str, new_password: str, token: str, session: AsyncSession = Depends(get_session)) -> dict:
    if token != os.getenv("TOKEN"):
        return {"result": False}

    password, key = crypt.encrypt(new_password)
    result = await crud_methods.PUT.password(app_name, password, key, session)
    return result



