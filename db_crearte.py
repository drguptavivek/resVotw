from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///posters.sqlite", echo = True)
meta = MetaData()

posters = Table(
   'posters', meta, 
   Column('id', Integer, primary_key = True), 
   Column('no', String), 
   Column('category', String),
   Column('name', String),
   Column('dept', String),
   Column('desig', String),
   Column('title', String),
   Column('auth', String),
   Column('email', String),

)
meta.create_all(engine)

Base = declarative_base()
class Poster(Base):
    __tablename__ = 'posters'
    id = Column(Integer, primary_key=True,  autoincrement=True)
    no = Column(String)
    category = Column(String)
    name = Column(String)
    dept = Column(String)
    desig = Column(String)
    title = Column(String)
    auth = Column(String)
    email = Column(String)
    
Session = sessionmaker(bind=engine)



import pyexcel as p
from itertools import product
sheet = p.get_sheet(file_name="2.xlsx")
sheet.name_columns_by_row(0) # first row has column names
print(sheet.row[0])
print(list(sheet.colnames))

def cleanse_func(v):
    v = str(v).replace("\n", ", ")
    v = str(v).replace("  ", " ")
    v = str(v).replace(", , ", ", ")
    v = v.rstrip().strip()
    return v


sheet.map(cleanse_func)

print(sheet.row[0])

sheet.save_to_database(session=Session(), table=Poster)




