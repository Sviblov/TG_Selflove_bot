from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import User,supported_language
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        user_id: int,
        full_name: str,
        language: str,
        username: Optional[str] = None,
    ):
        """
        Creates or updates a new user in the database and returns the user object.
        :param user_id: The user's ID.
        :param full_name: The user's full name.
        :param language: The user's language.
        :param username: The user's username. It's an optional parameter.
        :return: User object, None if there was an error while making a transaction.
        """

        insert_stmt = (
            insert(User)
            .values(
                user_id=user_id,
                username=username,
                full_name=full_name,
                language=language,
            )
            .on_conflict_do_update(
                index_elements=[User.user_id],
                set_=dict(
                    username=username,
                    full_name=full_name,
                ),
            )
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()


    async def supported_language(
        self,
        language: str
    )-> bool:
        
        select_data = select(supported_language).where(supported_language.language==language)
        result = await self.session.execute(select_data)
        first_row = result.first()
        if first_row:
            return language
        else:
            # select_data=select(supported_language).where(supported_language.is_default==True)
            # result = await self.session.execute(select_data)
            # first_row: supported_language=result.first()
            # return first_row.language
            
            #In order not to overload DB:
            return 'en'
