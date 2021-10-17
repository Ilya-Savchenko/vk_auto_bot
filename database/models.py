import peewee

db = peewee.SqliteDatabase('database/goods.sqlite3')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Section(BaseModel):
    name = peewee.CharField()

    class Meta:
        db_table = 'sections'

class Good(BaseModel):
    name = peewee.CharField()
    price = peewee.DecimalField()
    description = peewee.TextField()
    image = peewee.CharField()
    section = peewee.ForeignKeyField(model=Section, on_delete='CASCADE', related_name='goods')

    class Meta:
        db_table = 'goods'

class UserState(BaseModel):
    user_id = peewee.BigIntegerField()
    state = peewee.CharField(max_length=5)

    class Meta:
        db_table = 'userstates'
