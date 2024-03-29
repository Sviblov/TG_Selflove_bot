from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.repo.users import UserRepo
from infrastructure.database.repo.interface import InterfaceRepo
from infrastructure.database.repo.log_message import logMessageRepo
from infrastructure.database.repo.questions import QuestionRepo
from infrastructure.database.repo.poll_results import ResultsRepo
from infrastructure.database.repo.interventions import InterventionsRepo
from infrastructure.database.setup import create_engine


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations. This class holds all the repositories for the database models.

    You can add more repositories as properties to this class, so they will be easily accessible.
    """

    session: AsyncSession

    @property
    def users(self) -> UserRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return UserRepo(self.session)
    
    @property
    def interface(self) -> InterfaceRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return InterfaceRepo(self.session)
    

    @property
    def log_message(self) -> logMessageRepo:

        return logMessageRepo(self.session)

    @property
    def questions(self) -> QuestionRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return QuestionRepo(self.session)
    
    @property
    def results(self) -> ResultsRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return ResultsRepo(self.session)

    @property
    def interventions(self) -> InterventionsRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return InterventionsRepo(self.session)

if __name__ == "__main__":
    from infrastructure.database.setup import create_session_pool
    from tgbot.config import Config

    async def example_usage(config: Config):
        """
        Example usage function for the RequestsRepo class.
        Use this function as a guide to understand how to utilize RequestsRepo for managing user data.
        Pass the config object to this function for initializing the database resources.
        :param config: The config object loaded from your configuration.
        """
        engine = create_engine(config.db)
        session_pool = create_session_pool(engine)

        async with session_pool() as session:
            repo = RequestsRepo(session)

            # Replace user details with the actual values
            user = await repo.users.get_or_create_user(
                user_id=12356,
                full_name="John Doe",
                language="en",
                username="johndoe",
            )
