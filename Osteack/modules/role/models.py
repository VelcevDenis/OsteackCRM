# from pydantic import BaseModel
# from database import Base
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship


# class RoleBase(BaseModel):
#     role_name = str

# class Role(Base):
#     __tablename__ = 'roles'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     role_name = Column(String(50), unique=True, nullable=False)


from pydantic import BaseModel
from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class RoleBase(BaseModel):
    role_name: str  # Correct annotation for the field

    class Config:
        from_attributes = True  # Updated to use 'from_attributes' in Pydantic v2

class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False)
