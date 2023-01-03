import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_table
from sql_requests import SqlRequests
from sql_user_info import login, password


if __name__ == '__main__':

    DSN = f'postgresql://{login}:{password}@localhost:5432/orm_db'

    engine = sqlalchemy.create_engine(DSN)
    create_table(engine=engine)

    sql = SqlRequests(engine=engine)

    sql.add_publisher(table_name="Publisher", name="Gogol")
    # print(request1)
    sql.add_publisher(table_name="Publisher", name="Art")
    sql.add_publisher(table_name="Publisher", name="publisher1")
