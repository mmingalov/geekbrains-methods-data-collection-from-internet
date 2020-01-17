from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import (
    Base,
    BlogPost,
    Writer,
    Tag
)

class BlogDb:
    def __init__(self, url, base=Base):
        engine = create_engine(url)
        base.metadata.create_all(engine)
        session_db = sessionmaker(bind=engine)
        self.__session = session_db()
    @property
    #защищает метод, превращая его в атрибут
    def session(self):
        return self.__session
    #Выдает ошибку и подчеркивает строку 19
    #     if __name__ == '__main__':
    #                              ^
    # IndentationError: unindent does not match any outer indentation level

 # if __name__ == '__main__':
 #     db_url = 'sqlite:///blogpost.sqlite'
 #     db = BlogDb(db_url)
 #     print(1)