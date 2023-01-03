from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale


class SqlRequests():

    def __init__(self, engine):

        self.engine = engine
        self.tables = {"Publisher": Publisher, "Book": Book, "Shop": Shop, "Stock": Stock, "Sale": Sale}

    def add_publisher(self, table_name: str, name: str):

        Session = sessionmaker(bind=self.engine)
        session = Session()
        table = self.tables[table_name.capitalize()]
        if name in [q.name for q in session.query(table).all()]:
            print(f'This publisher ({name}) already uploaded')
        else:
            new_data = table(name=name)
            session.add(new_data)
            session.commit()
            print('Data upload:', new_data)
            session.close()

    def get_data(self, table_name):

        pass


