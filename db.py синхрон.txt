from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.backend.base import Base

DATABASE_URL = "postgresql+psycopg2://postgres:000@localhost:5432/my_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def check_registered_models():
    print("Зарегистрированные таблицы в базе данных:")
    for table_name in Base.metadata.tables.keys():
        print(f"- {table_name}")

if __name__ == "__main__":
    check_registered_models()
    Base.metadata.create_all(bind=engine)