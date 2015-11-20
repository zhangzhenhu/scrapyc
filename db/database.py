# encoding=utf8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
# from . import SqlSession
# from .app import coreapp

# _db_file = coreapp.config.get("DATA_PATH", None)
# if _db_file:
#     _db_file = os.path.join(_db_file, "task.db")
# else:
#     _db_file = ':memory:'

# db_engine = create_engine('sqlite:///' + _db_file, echo=False)
# SqlSession = s
# SqlSession.configure(bind=db_engine)
SafeSession = scoped_session(sessionmaker(autocommit=False, autoflush=False))

Base = declarative_base()
# Base.query = SafeSession.query_property()
# 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
# 元数据上。否则你就必须在调用 init_db() 之前导入它们。
# import scrapyc.server.crawler.models



# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()

# coreapp.config.set("db_engine", db_engine)
