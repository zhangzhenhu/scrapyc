from scrapy.item import Field, Item, ItemMeta
from scrapy import optional_features


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, String
AlchemyBase = declarative_base()
from sqlalchemy.orm.attributes import InstrumentedAttribute
class AlchemyItemMeta(ItemMeta):

    def  __new__(mcs, class_name, bases, attrs):
        cls = super(AlchemyItemMeta, mcs).__new__(mcs, class_name, bases, attrs)
        #cls.fields = cls.fields.copy()
        if cls.alchemy_model:
            cls._model_fields = []
            #cls._model_meta = cls.sqlalchemy_model._meta
            for name,obj in vars(cls.alchemy_model).items():
                if isinstance(obj,InstrumentedAttribute):
                    if name not in cls.fields:
                        cls.fields[name] = Field()
                    cls._model_fields.append(name)
        return cls


class AlchemyItem(Item):

    __metaclass__ = AlchemyItemMeta

    alchemy_model = None

    def __init__(self, *args, **kwargs):
        super(AlchemyItem, self).__init__(*args, **kwargs)
        self._instance = None
        self._errors = None


    def is_valid(self, exclude=None):
        self._get_errors(exclude)
        return not bool(self._errors)

    def _get_errors(self, exclude=None):
        if self._errors is not None:
            return self._errors

        self._errors = {}
        if exclude is None:
            exclude = []

        try:
            self.instance.clean_fields(exclude=exclude)
        except ValidationError as e:
            self._errors = e.update_error_dict(self._errors)

        try:
            self.instance.clean()
        except ValidationError as e:
            self._errors = e.update_error_dict(self._errors)

        # uniqueness is not checked, because it is faster to check it when
        # saving object to database. Just beware, that failed save()
        # raises IntegrityError instead of ValidationError.

        return self._errors
    errors = property(_get_errors)

    @property
    def model(self):
        if self._instance is None:
            modelargs = dict((k, self.get(k)) for k in self._values
                             if k in self._model_fields)
            self._instance = self.alchemy_model(**modelargs)
        return self._instance
if __name__ == '__main__':
    import pdb
    pdb.set_trace()
