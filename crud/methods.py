import traceback

from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from crud.models import Passwords, Keys


# from crypt_password import encrypt


# async def get_data(session: AsyncSession):
#     items = await session.execute(select(MyPasswords.app_name, MyPasswords.password))
#     data = items.fetchall()
#     return data

# class MyItem(BaseModel):
#     app_name: str
#     password: str
#     token: str


class GET:
    @staticmethod
    async def password(app_name, session: AsyncSession) -> list:

        passwords = await session.execute(select(Passwords).where(Passwords.app_name == app_name))
        data = passwords.scalars().all()

        if data:
            for row in data:
                key = await session.execute(select(Keys.key).where(Keys.password_id == row.id))
                key = key.scalars().one()

                data = [[row.app_name, row.password, key] for row in data]

        return data


    @staticmethod
    async def app_list(session: AsyncSession) ->list:

        lists = await session.execute(select(Passwords.app_name))
        data = lists.fetchall()

        if data:
            return [row[0] for row in data]
        return []



class POST:
    @staticmethod
    async def password(app_name, pswd, key, session: AsyncSession):
        try:
            # await session.execute(select(app_name=app_name, password=pswd).where(MyPasswords.token == token))

            password_id = await session.execute(
                insert(
                    Passwords
                ).values(
                    app_name=app_name, password=pswd
                ).returning(Passwords.id)
            )

            password_id = password_id.scalars().one()

            await session.execute(
                insert(
                    Keys
                ).values(
                    key=key, password_id=password_id
                )
            )

            await session.commit()

            return {"result": True}

        except IntegrityError:
            await session.rollback()
            return {"result": traceback.format_exc()}


class PUT:
    @staticmethod
    async def password(app_name, new_password, key, session: AsyncSession):
        password_id = await session.execute(select(Passwords.id).where(Passwords.app_name == app_name))
        password_id = password_id.scalars().one()

        await session.execute(delete(Keys).where(Keys.password_id == password_id))
        await session.execute(delete(Passwords).where(Passwords.id == password_id))
        await session.commit()

        result = await POST.password(app_name, new_password, key, session)

        return {"result": True}
