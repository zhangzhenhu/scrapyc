from sqlalchemy.orm import sessionmaker,scoped_session
SqlSession = sessionmaker(autocommit=True,autoflush=True)