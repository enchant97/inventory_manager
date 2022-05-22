from enum import Enum
from typing import AsyncGenerator

from tortoise.fields import (BooleanField, CharEnumField, CharField, DateField,
                             DatetimeField, ForeignKeyField,
                             ForeignKeyNullableRelation, ForeignKeyRelation,
                             IntField, ReverseRelation)
from tortoise.models import Model

MAX_RECURSION_LEVEL = 150


class ReportSortTypes(str, Enum):
    CREATION = "creation"
    CREATION_DESC = "creation_desc"
    EXPIRY = "expiry"
    EXPIRY_DESC = "expiry_desc"


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
    items: ReverseRelation["Item"]
    item_reports: ReverseRelation["ItemReport"]

    async def get_all_children(self, _level=0) -> AsyncGenerator["Location", None]:
        """
        yields all children and the children's
        children until either MAX_RECURSION_LEVEL or
        until there are no children left
        """
        async for child in self.children:
            yield child

            # prevent infinite loop
            if _level >= MAX_RECURSION_LEVEL:
                return

            async for sub_child in child.get_all_children(_level + 1):
                yield sub_child


class Category(CommonModel):
    name = CharField(64, unique=True)
    description = CharField(512, null=True)
    parent: ForeignKeyNullableRelation["Category"] = ForeignKeyField(
        "models.Category", "children", null=True)

    children: ReverseRelation["Category"]
    items: ReverseRelation["Item"]
    item_reports: ReverseRelation["ItemReport"]

    async def get_all_children(self, _level=0) -> AsyncGenerator["Category", None]:
        """
        yields all children and the children's
        children until either MAX_RECURSION_LEVEL or
        until there are no children left
        """
        async for child in self.children:
            yield child

            # prevent infinite loop
            if _level >= MAX_RECURSION_LEVEL:
                return

            async for sub_child in child.get_all_children(_level + 1):
                yield sub_child


class Item(CommonModel):
    name = CharField(64, unique=True)
    description = CharField(512, null=True)
    expires = DateField(null=True)
    quantity = IntField(default=1)
    location: ForeignKeyRelation["Location"] = ForeignKeyField(
        "models.Location", "items")
    category: ForeignKeyRelation["Category"] = ForeignKeyField(
        "models.Category", "items")


class ItemReport(CommonModel):
    name = CharField(64, unique=True)
    filter_location: ForeignKeyNullableRelation["Location"] = ForeignKeyField(
        "models.Location", "item_reports", null=True)
    filter_category: ForeignKeyNullableRelation["Category"] = ForeignKeyField(
        "models.Category", "item_reports", null=True)
    filter_expired_only = BooleanField(default=False)
    sort_mode = CharEnumField(ReportSortTypes, null=True)
    show_description = BooleanField(default=False)
    show_expiry = BooleanField(default=False)
    show_location = BooleanField(default=False)
    show_category = BooleanField(default=False)
    show_quick_actions = BooleanField(default=False)
