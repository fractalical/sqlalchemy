import datetime
from models import Publisher, Book, Shop, Stock, Sale


class SqlRequests():

    def __init__(self, session):

        self.session = session
        self.tables = {"Publisher": Publisher, "Book": Book, "Shop": Shop, "Stock": Stock, "Sale": Sale}

    def add_publisher(self, table_name: str, name: str):

        session = self.session
        table = self.tables[table_name.capitalize()]
        publishers = {q.name: q.id for q in session.query(table).all()}
        if name in publishers:
            print(f'This publisher ({name}) already exist')
            return publishers[name]
        else:
            new_data = table(name=name)
            session.add(new_data)
            session.commit()
            print(f'{new_data} uploaded to {table_name}')
            return new_data.id

    def add_book(self, table_name: str, title: str, id_publisher: int):

        session = self.session
        table = self.tables[table_name.capitalize()]
        if (title, id_publisher) in [(q.title, q.id_publisher) for q in session.query(table).all()]:
            print(f'This publisher ({title}) already exist')
        else:
            new_data = table(title=title, id_publisher=id_publisher)
            session.add(new_data)
            session.commit()
            print(f'{new_data} uploaded to {table_name}')

    def add_shop(self, table_name: str, name: str):

        res = self.add_publisher(table_name, name)

        return res

    def add_book_to_shop(self, table_name: str, title: str or int, shop: str or int, add_count: int, publisher=None):

        session = self.session
        table = self.tables[table_name.capitalize()]
        if isinstance(title, int) and isinstance(shop, int):
            id_book, id_shop = title, shop
        else:
            id_publisher = session.query(Publisher).filter(Publisher.name == publisher).all()[0].id
            id_book = session.query(Book).filter(Book.title == title, Book.id_publisher == id_publisher) \
                .all()[0].id
            id_shop = session.query(Shop).filter(Shop.name == shop) \
                .all()[0].id
        count = session.query(table).filter(table.id_book == id_book, table.id_shop == id_shop).all()
        if not count:
            count = 0
            new_data = table(id_book=id_book, id_shop=id_shop, count=count + add_count)
            session.add(new_data)
        else:
            count = count[0].count
            session.query(table).filter(table.id_book == id_book, table.id_shop == id_shop).update({'count': count + add_count})
        session.commit()
        print(f'{add_count} {title} added to {shop}. Total count: {count + add_count}')

    def add_sale(self, table_name: str, count: int, price: float,
                 title=None, publisher=None, shop=None, id_stock=None, date_sale=None):

        session = self.session
        table = self.tables[table_name.capitalize()]
        if id_stock is None:
            id_publisher = session.query(Publisher).filter(Publisher.name == publisher).all()[0].id
            id_book = session.query(Book).filter(Book.title == title, Book.id_publisher == id_publisher).all()[0].id
            id_shop = session.query(Shop).filter(Shop.name == shop).all()[0].id
            id_stock = session.query(Stock).filter(Stock.id_book == id_book, Stock.id_shop == id_shop).all()
        else:
            id_stock = session.query(Stock).filter(Stock.id == id_stock).all()
        if id_stock and id_stock[0].count > 0:
            if id_stock[0].count - count > 0:
                date_sale = datetime.datetime.today() if date_sale is None \
                    else datetime.datetime.strptime(date_sale, '%Y-%m-%dT%H:%M:%S.%fZ')
                new_data = table(price=price, date_sale=date_sale, id_stock=id_stock[0].id, count=count)
                session.add(new_data)
                session.query(Stock).filter(Stock.id == id_stock[0].id).update({'count': id_stock[0].count - count})
                session.commit()
                print(f'{count} "{title}" was sold {date_sale}')
            else:
                print(f'Not enough count. Available count = {id_stock[0].count}')
        else:
            print('Not enough count. Available count = 0')

    def get_sales(self, publisher: str):

        session = self.session
        id_publisher = session.query(Publisher).filter(Publisher.name == publisher).all()[0].id

        q1 = session.query(Publisher.name, Book.title, Book.id)\
            .join(Book.publisher).filter(Publisher.id == id_publisher).subquery()
        q2 = session.query(Stock.id_book, Shop.name, Stock.id)\
            .join(Stock.shops).subquery()
        q3 = session.query(q1.c.name, q1.c.title, q2.c.name.label("shop_name"), q2.c.id)\
            .join(q2, q1.c.id == q2.c.id_book).subquery()
        q4 = session.query(q3.c.name, q3.c.title, q3.c.shop_name, Sale.date_sale, Sale.price, Sale.count)\
            .join(q3, q3.c.id == Sale.id_stock).all()

        if q4:
            widh_title = max([len(q[1]) for q in q4])
            widh_shop = max([len(q[2]) for q in q4])
            widh_price = max([len(str(q[4] * q[5])) for q in q4])
            for q in q4:
                price = str(q[4] * q[5])
                title = q[1]
                shop = q[2]
                date = q[3].strftime('%d-%m-%Y')
                print(f'{title.ljust(widh_title)} | {shop.ljust(widh_shop)} | {price.ljust(widh_price)} | {date}')
        else:
            print('Publisher not find.')
