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
        return f"tbl_users(id={self.username!r}, name={self.password!r}, fullname={self.created!r})"


class tbl_linkedin(db.Model):
    '''
    class for tbl_linkedin table
    '''

    __tablename__ = 'tbl_linkedin'

    profile = Column(String, primary_key=True)
    url = Column(String, nullable=False)
    about = Column(String, nullable=False)
    # location is a reserved word, changed to cvlocation
    cvlocation = Column(String, nullable=False)
    education = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)

    def __repr__(self):
        return f"tbl_linkedin(profile={self.profile}, url={self.url}, about={self.about}, cvlocation={self.cvlocation}, education={self.education}, firstname={self.firstname}, lastname={self.lastname})"


class tbl_linkedinusernames(db.Model):
    '''
    class for tbl_linkedinusernames table
    '''

    __tablename__ = 'tbl_linkedinusernames'

    usernames = Column(String, primary_key=True, nullable=False)

    def __repr__(self):
        return f"tbl_linkedin(usernames={self.usernames})"
