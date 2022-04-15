from tortoise.fields import (CharField, DateField, DatetimeField,
                             ForeignKeyField, ForeignKeyNullableRelation,
                             ForeignKeyRelation, IntField, ReverseRelation)
from tortoise.models import Model


class CommonModel(Model):
    id = IntField(pk=True)
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)
    removed_at = DatetimeField(null=True)

    class Meta:
        abstract = True


class Location(CommonModel):
    name = CharField(64, unique=True)
    description = CharField(512, null=True)
    parent: ForeignKeyNullableRelation["Location"] = ForeignKeyField(
        "models.Location", "children", null=True)

    children: ReverseRelation["Location"]


class Category(CommonModel):
    name = CharField(64, unique=True)
    description = CharField(512, null=True)
    parent: ForeignKeyNullableRelation["Category"] = ForeignKeyField(
        "models.Category", "children", null=True)

    children: ReverseRelation["Category"]


class Item(CommonModel):
    name = CharField(64, unique=True)
    description = CharField(512, null=True)
    expires = DateField(null=True)
    quantity = IntField(default=1)
    location: ForeignKeyRelation["Location"] = ForeignKeyField(
        "models.Location")
    category: ForeignKeyRelation["Category"] = ForeignKeyField(
        "models.Category")
