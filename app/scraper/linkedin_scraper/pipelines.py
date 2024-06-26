from sqlalchemy import create_engine
import sqlalchemy
import sys
import os
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker

from sql import PostgresFlaskConnectionClass
from sql.DatabaseSetup import *
# Put backend imports here

class LinkedinPipeline(PostgresFlaskConnectionClass):
    def __init__(self):
        super().__init__()
        return

    def __str__(self):
        # use this to print the
        return

    def process_item(self, item, spider):
        self.select(tbl_linkedin)
        return item


if __name__ == '__main__':
    pipeline = LinkedinPipeline()
    pipeline.process_item()
    print(pipeline)
