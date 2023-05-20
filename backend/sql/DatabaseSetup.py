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


# # Add to Mapped Base object
# Base.metadata.create_all(engine)

# # Create session
# Session = sessionmaker(bind=engine)
# session = Session()

# # Menu for UrbanBurger
# insert_tbl_users = tbl_users(username="aidan102", password=123,
#                              created=datetime.datetime.now())

# # session.begin()
# session.add(insert_tbl_users)
# session.commit()
# # session.close()
