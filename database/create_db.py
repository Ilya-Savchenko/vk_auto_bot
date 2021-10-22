import os.path

import peewee

from .models import Good, Section, UserState, db


def fill_sections():
    Section.get_or_create(name='Летняя резина')
    Section.get_or_create(name='Зимняя резина')
    Section.get_or_create(name='Диски')


def fill_goods():
    Good.get_or_create(
        name='Летняя резина 1',
        price=2500.00,
        description='Недорогая летняя резина',
        image=os.path.normpath('database/images/summer_tires/sum_1.jpg'),
        section=Section.get(Section.name == 'Летняя резина'),
    )
    Good.get_or_create(
        name='Летняя резина 2',
        price=3500.00,
        description='Летняя резина средней ценовой категории',
        image=os.path.normpath('database/images/summer_tires/sum_2.jpg'),
        section=Section.get(Section.name == 'Летняя резина'),
    )
    Good.get_or_create(
        name='Летняя резина 3',
        price=5000.00,
        description='Отличная летняя резина',
        image=os.path.normpath('database/images/summer_tires/sum_3.jpg'),
        section=Section.get(Section.name == 'Летняя резина'),
    )
    Good.get_or_create(
        name='Зимняя резина 1',
        price=3500.00,
        description='Недорогая зимняя резина',
        image=os.path.normpath('database/images/winter_tires/wint_1.jpg'),
        section=Section.get(Section.name == 'Зимняя резина'),
    )
    Good.get_or_create(
        name='Зимняя резина 2',
        price=5000.00,
        description='Хорошая зимняя резина',
        image=os.path.normpath('database/images/winter_tires/wint_2.jpg'),
        section=Section.get(Section.name == 'Зимняя резина'),
    )
    Good.get_or_create(
        name='Зимняя резина 3',
        price=7000.00,
        description='Отличная зимняя резина',
        image=os.path.normpath('database/images/winter_tires/wint_3.jpg'),
        section=Section.get(Section.name == 'Зимняя резина'),
    )
    Good.get_or_create(
        name='Диски 1',
        price=3000.00,
        description='Недорогие диски',
        image=os.path.normpath('database/images/disks/d_1.jpg'),
        section=Section.get(Section.name == 'Диски'),
    )
    Good.get_or_create(
        name='Диски 2',
        price=4700.00,
        description='Хорошие диски',
        image=os.path.normpath('database/images/disks/d_2.jpg'),
        section=Section.get(Section.name == 'Диски'),
    )
    Good.get_or_create(
        name='Диски 3',
        price=6100.00,
        description='Отличные диски',
        image=os.path.normpath('database/images/disks/d_3.jpg'),
        section=Section.get(Section.name == 'Диски'),
    )



def fill_db():
    fill_sections()
    fill_goods()


def connect_and_fill_db():
    try:
        db.connect()
        Section.create_table()
        Good.create_table()
        UserState.create_table()
    except peewee.InternalError as px:
        print(str(px))
    fill_db()
