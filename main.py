import datetime
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_table
from sql_requests import SqlRequests
from sql_user_info import login, password


if __name__ == '__main__':

    db_name = 'orm_db'
    DSN = f'postgresql://{login}:{password}@localhost:5432/{db_name}'

    engine = sqlalchemy.create_engine(DSN)

    Session = sessionmaker(bind=engine)
    session = Session()

    create_table(engine=engine)

    sql = SqlRequests(session=session)

    sql.get_sales(publisher="Pearson")

    # Task 3
    request_commands = {
        'publisher': sql.add_publisher,
        'book': sql.add_book,
        'shop': sql.add_shop,
        'stock': sql.add_book_to_shop,
        'sale': sql.add_sale
    }

    with open("test_data.json", encoding='utf-8', mode='r') as file:
        data = json.load(file)
        for row in data:
            print(row)
            cmd = row['model']
            request_commands[cmd](table_name=cmd, kwargs=row['fields'])


    session.close()
