from sqlalchemy import Integer, Column
from db_session import SqlAlchemyBase


class Chats(SqlAlchemyBase):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    chat = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Chats> {self.id} {self.chat}'
