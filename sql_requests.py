import datetime
from models import Publisher, Book, Shop, Stock, Sale


class SqlRequests:

    def __init__(self, session):

        self.session = session
        self.tables = {"Publisher": Publisher, "Book": Book, "Shop": Shop, "Stock": Stock, "Sale": Sale}

    def add_publisher(self, table_name: str, kwargs: dict):
        """

        :param table_name:
        :param kwargs: {'name': ...}
        """

        session = self.session
        table = self.tables[table_name.capitalize()]
        publishers = {q.name: q.id for q in session.query(table).all()}
        if kwargs['name'] in publishers:
            print(f'This publisher ({kwargs["name"]}) already exist')
            return publishers[kwargs['name']]
        else:
            new_data = table(name=kwargs['name'])
            session.add(new_data)
            session.commit()
            print(f'{new_data} uploaded to {table_name}')
            return new_data.id

    def add_book(self, table_name: str, kwargs: dict):
        """

        :param table_name:
        :param kwargs: {'title': ..., 'id_publisher': ...}
        :return:
        """

        session = self.session
        table = self.tables[table_name.capitalize()]
        if (kwargs['title'], kwargs['id_publisher']) in [(q.title, q.id_publisher) for q in session.query(table).all()]:
            print(f'This publisher ({kwargs["title"]}) already exist')
        else:
            new_data = table(title=kwargs['title'], id_publisher=kwargs['id_publisher'])
            session.add(new_data)
            session.commit()
            print(f'{new_data} uploaded to {table_name}')

    def add_shop(self, table_name: str, kwargs: dict):
        """

        :param table_name:
        :param kwargs: {'name': ...}
        :return:
        """

        res = self.add_publisher(table_name, kwargs)

        return res

    def add_book_to_shop(self, table_name: str, kwargs: dict):
        """

        :param table_name:
        :param kwargs: {'id_book': ..., 'id_shop': ..., 'count': ...}
        :return:
        """

        session = self.session
        table = self.tables[table_name.capitalize()]
        id_book, id_shop = kwargs['id_book'], kwargs['id_shop']
        count = session.query(table).filter(table.id_book == id_book, table.id_shop == id_shop).all()
        if not count:
            count = 0
            new_data = table(id_book=id_book, id_shop=id_shop, count=count + kwargs['count'])
            session.add(new_data)
        else:
            count = count[0].count
            session.query(table).filter(table.id_book == id_book, table.id_shop == id_shop)\
                .update({'count': count + kwargs['count']})
        session.commit()
        print(f'{kwargs["count"]} of {id_book} added to shop {id_shop}. Total count: {count + kwargs["count"]}')

    def add_sale(self, table_name: str, kwargs: dict):
        """

        :param table_name:
        :param kwargs: {'price': ..., 'count': ..., 'date_sale': ..., 'id_stock': ...}
        :return:
        """

        session = self.session
        table = self.tables[table_name.capitalize()]
        id_stock = session.query(Stock).filter(Stock.id == kwargs['id_stock']).all()
        if id_stock and id_stock[0].count > 0:
            if id_stock[0].count - kwargs['count'] > 0:
                date_sale = datetime.datetime.today() if kwargs['date_sale'] is None \
                    else datetime.datetime.strptime(kwargs['date_sale'], '%Y-%m-%dT%H:%M:%S.%fZ')
                new_data = table(price=float(kwargs['price']), date_sale=date_sale,
                                 id_stock=id_stock[0].id, count=kwargs['count'])
                session.add(new_data)
                session.query(Stock).filter(Stock.id == id_stock[0].id)\
                    .update({'count': id_stock[0].count - kwargs['count']})
                session.commit()
                print(f'{kwargs["count"]} from stock "{id_stock[0].id}" was sold {date_sale}')
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
