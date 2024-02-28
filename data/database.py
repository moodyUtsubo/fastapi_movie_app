from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#connect to a database
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# Đưa vào env
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/database"

#create a SQLalchemy engine
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

#a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


#Sao ko đặt hàm get db_session ở đây?

#Đưa file này ra 1 module riêng chứ e đặt tên module là data nghe nó ko đúng logic
