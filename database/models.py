import peewee

db = peewee.SqliteDatabase('database/goods.sqlite3')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Section(BaseModel):
    name = peewee.CharField(unique=True)

    class Meta:
        db_table = 'sections'

class Good(BaseModel):
    name = peewee.CharField(unique=True)
    price = peewee.DecimalField()
    description = peewee.TextField()
    image = peewee.CharField()
    section = peewee.ForeignKeyField(model=Section, on_delete='CASCADE', related_name='goods')

    class Meta:
        db_table = 'goods'

class UserState(BaseModel):
    user_id = peewee.BigIntegerField(unique=True)
    state = peewee.CharField(max_length=10)
    good_id = peewee.IntegerField(null=True)

    class Meta:
        db_table = 'userstates'
