import os.path

import peewee

from models import Goods, Sections, db


def fill_sections():
    Sections.create(name='Летняя резина')
    Sections.create(name='Зимняя резина')
    Sections.create(name='Диски')


def fill_goods():
    Goods.create(
        name='Летняя резина 1',
        price=2500.00,
        description='Недорогая летняя резина',
        image=os.path.abspath('images/summer_tires/sum_1.jpg'),
        section=Sections.get(Sections.name == 'Летняя резина'),
    )
    Goods.create(
        name='Летняя резина 2',
        price=3500.00,
        description='Летняя резина средней ценовой категории',
        image=os.path.abspath('images/summer_tires/sum_2.jpg'),
        section=Sections.get(Sections.name == 'Летняя резина'),
    )
    Goods.create(
        name='Летняя резина 3',
        price=5000.00,
        description='Отличная летняя резина',
        image=os.path.abspath('images/summer_tires/sum_3.jpg'),
        section=Sections.get(Sections.name == 'Летняя резина'),
    )
    Goods.create(
        name='Зимняя резина 1',
        price=3500.00,
        description='Недорогая зимняя резина',
        image=os.path.abspath('images/winter_tires/wint_1.jpg'),
        section=Sections.get(Sections.name == 'Зимняя резина'),
    )
    Goods.create(
        name='Зимняя резина 2',
        price=5000.00,
        description='Хорошая зимняя резина',
        image=os.path.abspath('images/winter_tires/wint_2.jpg'),
        section=Sections.get(Sections.name == 'Зимняя резина'),
    )
    Goods.create(
        name='Зимняя резина 3',
        price=7000.00,
        description='Отличная зимняя резина',
        image=os.path.abspath('images/winter_tires/wint_3.jpg'),
        section=Sections.get(Sections.name == 'Зимняя резина'),
    )
    Goods.create(
        name='Диски 1',
        price=3000.00,
        description='Недорогие диски',
        image=os.path.abspath('images/disks/d_1.jpg'),
        section=Sections.get(Sections.name == 'Диски'),
    )
    Goods.create(
        name='Диски 2',
        price=4700.00,
        description='Хорошие диски',
        image=os.path.abspath('images/disks/d_2.webp'),
        section=Sections.get(Sections.name == 'Диски'),
    )
    Goods.create(
        name='Диски 3',
        price=6100.00,
        description='Отличные диски',
        image=os.path.abspath('images/disks/d_3.jpg'),
        section=Sections.get(Sections.name == 'Диски'),
    )



def fill_db():
    fill_sections()
    fill_goods()


if __name__ == '__main__':
    try:
        db.connect()
        Sections.create_table()
        Goods.create_table()
    except peewee.InternalError as px:
        print(str(px))
    fill_db()
