from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from app import db


class tbl_users(db.Model):
    '''
    class for tbl_users table
    '''

    __tablename__ = 'tbl_users'

    username = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    created = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"test(id={self.username!r}, name={self.password!r}, fullname={self.created!r})"
