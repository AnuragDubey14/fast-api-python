from sqlalchemy import create_engine,MetaData

engine=create_engine("sqlite:///mydb.db")
meta=MetaData()
conn=engine.connect()
