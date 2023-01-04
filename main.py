import datetime
import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_table
from sql_requests import SqlRequests
from sql_user_info import login, password


if __name__ == '__main__':

    DSN = f'postgresql://{login}:{password}@localhost:5432/orm_db'

    engine = sqlalchemy.create_engine(DSN)

    Session = sessionmaker(bind=engine)
    session = Session()

    create_table(engine=engine)

    sql = SqlRequests(session=session)

    # publisher = sql.add_publisher(table_name="Publisher", name="Gogol")
    # book = sql.add_book(table_name="Book", title="Book 1", id_publisher=publisher)
    # shop = sql.add_shop(table_name="shop", name="Буквоед")
    # sql.add_book_to_shop(table_name="stock", title="Book 1", publisher="Gogol", shop="Буквоед", add_count=10)
    # sql.add_sale(table_name="Sale", title="Book 1", publisher="Gogol", shop="Буквоед", sold_count=3, price=250)

    # sql.get_sales(publisher="Gogol")

    request_commads = {
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
            if row['model'] == 'publisher':
                sql.add_publisher(table_name='publisher')
            elif row['model'] == 'book':
                pass
            elif row['model'] == 'shop':
                pass
            elif row['model'] == 'stock':
                pass
            elif row['model'] == 'sale':
                pass


    d = '2018-10-25T10:59:56.230Z'

    da = datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.%fZ')
    t = datetime.datetime.today()

    print(t)

    print(da)

    session.close()
