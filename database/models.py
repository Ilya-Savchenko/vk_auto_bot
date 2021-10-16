import peewee

db = peewee.SqliteDatabase('database/goods.sqlite3')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Sections(BaseModel):
    name = peewee.CharField()


class Goods(BaseModel):
    name = peewee.CharField()
    price = peewee.DecimalField()
    description = peewee.TextField()
    image = peewee.CharField()
    section = peewee.ForeignKeyField(model=Sections, on_delete='CASCADE', related_name='goods')
