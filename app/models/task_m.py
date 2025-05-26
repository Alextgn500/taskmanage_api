from app.backend.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Tasks(Base):
    __tablename__ = 'tasks'
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    slug = Column(String, unique=True, index=True)

    user = relationship('Users', back_populates='tasks')

if __name__ == '__main__':
    from sqlalchemy.schema import CreateTable
    from app.models.user_m import Users
    print("\nSQL для создания таблицы задач:")
    print(CreateTable(Tasks.__table__))
