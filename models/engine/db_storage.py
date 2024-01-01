#!/usr/bin/python3
"""DBStorage class definition"""
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base

class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST", default="localhost")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, password, host, database),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session (self.__session)"""
        objs_list = []
        if cls:
            if isinstance(cls, str):
                try:
                    cls = globals()[cls]
                except KeyError:
                    pass
            if issubclass(cls, Base):
                objs_list = self.__session.query(cls).all()
        else:
            for subclass in Base.__subclasses__():
                obj_list.extend(self.__session.query(subclass).all())
        result = {}
        for obj in objs_list:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            result[key] = obj
        return result

    def new(self, obj):
        """Add the object to the current database session (self.__session)"""
        if obj:
            self.__session.add(obj)
            self.__session.commit()

    def save(self):
        """Commit all changes of the current database session (self.__session)"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create a new session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the current session"""
        if self.__session:
            self.__session.close()
