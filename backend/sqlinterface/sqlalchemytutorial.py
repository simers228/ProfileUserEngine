import sqlalchemy


class sqltutorial:
    def __init__(self):
        self.version = sqlalchemy.__version__

    def __repr__(self):
        print(f'SQL Alchemy version >> {self.version}')
        return


print("Running sqlalchemytutorial.py")
print("__name__ = ", __name__)
