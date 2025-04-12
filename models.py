from sqlalchemy import Column,Integer, String,create_engine, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship,sessionmaker

Base = declarative_base()
class Place_work(Base):
    __tablename__="place_work"
    id=Column(Integer,primary_key=True)
    title=Column(String)
    applicants=relationship("Applicant",back_populates="place_work")
class Address(Base):
    __tablename__="address"
    id=Column(Integer,primary_key=True)
    address=Column(String)
    applicants=relationship("Applicant",back_populates="address")
class Post(Base):
    __tablename__="post"
    id=Column(Integer,primary_key=True)
    title=Column(String)
    employees=relationship("Employee",back_populates="post")
    def __str__(self):
        return self.title
class Employee(Base):
    __tablename__="employee"
    id=Column(Integer,primary_key=True)
    full_name=Column(String)
    post_id=Column(Integer,ForeignKey("post.id")) 
    post=relationship("Post",back_populates="employees")
    appeals=relationship("Appeal",back_populates="employee")
class Applicant(Base):
    __tablename__="applicant"
    id=Column(Integer,primary_key=True)
    full_name=Column(String)
    place_work_id=Column(Integer,ForeignKey("place_work.id"))
    phone=Column(String)
    email=Column(String)
    address_id=Column(Integer,ForeignKey("address.id"))
    place_work=relationship("Place_work",back_populates="applicants")
    address=relationship("Address", back_populates="applicants")
    appeals=relationship("Appeal",back_populates="applicant")
class Category(Base):
    __tablename__="category"
    id=Column(Integer,primary_key=True)
    title=Column(String)
    appeals=relationship("Appeal",back_populates="category")
class Status(Base):
    __tablename__="status"
    id=Column(Integer,primary_key=True)
    title=Column(String)
    appeals=relationship("Appeal",back_populates="status")
class Answer(Base):
    __tablename__="answer"
    id=Column(Integer,primary_key=True)
    title=Column(String)
    appeals=relationship("Appeal",back_populates="result")
class Appeal(Base):
    __tablename__="appeal"
    id=Column(Integer,primary_key=True)
    reg_number=Column(String)
    applicant_id=Column(Integer,ForeignKey("applicant.id"))
    employee_id=Column(Integer,ForeignKey("employee.id"))
    description=Column(String)
    registration_date=Column(Date)
    answer_date=Column(Date)
    category_id=Column(Integer,ForeignKey("category.id"))
    status_id=Column(Integer,ForeignKey("status.id"))
    result_id=Column(Integer,ForeignKey("answer.id"))
    applicant=relationship("Applicant",back_populates="appeals")
    employee=relationship("Employee",back_populates="appeals")
    category=relationship("Category",back_populates="appeals")
    status=relationship("Status",back_populates="appeals")
    result=relationship("Answer",back_populates="appeals")

engine=create_engine("postgresql://postgres:Service@localhost:5432/pract")  
Session=sessionmaker(bind=engine)
Base.metadata.create_all(engine)
 