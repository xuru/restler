

def wrap_method(cls, method):
    """ Helper function to help wrap _restler* methods when more
     than on decorator is used on a model.
    :param method: method to wrap
    """
    from copy import copy
    method_name = method.__func__.__name__
    method_param = method
    if hasattr(cls, method_name):
        orig_cls_method = getattr(cls, method_name)

        @classmethod
        def wrap(cls_):
            setattr(cls, method_name, method_param)
            method = getattr(cls, method_name)
            aggregate = copy(orig_cls_method())
            if isinstance(aggregate, list):  # _restler_types()
                aggregate = set(aggregate)
                aggregate.update(method())
                aggregate = list(aggregate)
            elif isinstance(aggregate, dict):  # _restler_property_map
                aggregate.update(method())
            elif isinstance(aggregate, str):
                # Developer shouldn't really do this, but we'll try
                # to do the correct thing and use the most recently defined name
                aggregate = method()  # _restler_serialization_name
            return aggregate
        setattr(cls, method_name, wrap)
    else:
        setattr(cls, method_name, method)


def ae_db_serializer(cls):
    """
    Restler serialization class decorator for google.appengine.ext.db.Model
    """
    from google.appengine.ext import blobstore, db

    @classmethod
    def _restler_types(cls):
        """
        A map of types types to callables that serialize those types.
        """
        from google.appengine.api import users
        from webapp2 import cached_property
        return {
            db.Query: lambda query: [obj for obj in query],
            db.GeoPt: lambda obj: "%s %s" % (obj.lat, obj.lon),
            db.IM: lambda obj: "%s %s" % (obj.protocol, obj.address),
            users.User: lambda obj: obj.user_id() or obj.email(),
            cached_property: lambda obj: cached_property,
            blobstore.BlobInfo: lambda obj: str(obj.key())  # TODO is this correct?
        }

    @classmethod
    def _restler_serialization_name(cls):
        """
        The lowercase model classname
        """
        return cls.kind().lower()

    @classmethod
    def _restler_property_map(cls):
        """
        List of model property names -> property types. The names are used in
        *include_all_fields=True* Property types must be from
        **google.appengine.ext.db.Property**
        """
        return cls.properties()

    wrap_method(cls, _restler_types)
    wrap_method(cls, _restler_property_map)
    cls._restler_serialization_name = _restler_serialization_name

    return cls


def ae_ndb_serializer(cls):
    """
    Restler serializationclass decorator for google.appengine.ext.ndb.Model
    """
    from google.appengine.ext import ndb

    @classmethod
    def _restler_types(cls):
        """
        A map of types types to callables that serialize those types.
        """
        from google.appengine.api import users
        from webapp2 import cached_property
        return {
            ndb.query.Query: lambda query: [obj for obj in query],
            ndb.GeoPt: lambda obj: "%s %s" % (obj.lat, obj.lon),
            users.User: lambda obj: obj.user_id() or obj.email(),
            cached_property: lambda obj: cached_property,
        }

    @classmethod
    def _restler_serialization_name(cls):
        """
        The lowercase model classname
        """
        return cls.__name__.lower()

    @classmethod
    def _restler_property_map(cls):
        """
        List of model property names if *include_all_fields=True*
        Property must be from **google.appengine.ext.ndb.Property**
        """
        return cls._properties

    wrap_method(cls, _restler_types)
    wrap_method(cls, _restler_property_map)
    cls._restler_serialization_name = _restler_serialization_name

    return cls


def django_serializer(cls):
    """
    Restler serialization class decorator for django.db.models
    """
    @classmethod
    def _restler_types(cls):
        """
        A map of types types to callables that serialize those types.
        """
        from django.db.models.query import QuerySet
        from django.db.models import CommaSeparatedIntegerField, FileField, FilePathField, ImageField
        import json
        return {
            QuerySet: lambda query: list(query),
            CommaSeparatedIntegerField: lambda value: json.loads(value),
            ImageField: lambda value: value,
            FileField: lambda value: value,
            FilePathField: lambda value: value
        }

    @classmethod
    def _restler_serialization_name(cls):
        """
        The lowercase model classname
        """
        return cls.__name__.lower()

    @classmethod
    def _restler_property_map(cls):
        """
        List of model property names -> property types. The names are used in
        *include_all_fields=True* Property must be from **django.models.fields**
        """
        from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField, RelatedObject
        # Relation fields (and their related objects) need to be handled specifically as there is no single way to
        # handle them -- they should be handled explicity through callables.
        excluded_types = {ForeignKey, ManyToManyField, OneToOneField, RelatedObject}
        name_map = cls._meta._name_map
        all_field_names = cls._meta.get_all_field_names()
        property_map = dict([(name, name_map[name][0].__class__)
                         for name in all_field_names if name_map[name][0].__class__ not in excluded_types])
        return property_map

    wrap_method(cls, _restler_types)
    wrap_method(cls, _restler_property_map)
    cls._restler_serialization_name = _restler_serialization_name

    return cls


def sqlalchemy_serializer(cls):
    """
    Restler serialization class decorator for SqlAlchemy models
    """
    @classmethod
    def _restler_types(cls):
        """
        A map of types types to callables that serialize those types.
        """
        from sqlalchemy.types import BinaryType, Interval, LargeBinary, PickleType
        from sqlalchemy.orm.query import Query
        import base64
        return {
            Query: lambda query: list(query),
            BinaryType : lambda value: base64.b64encode(value),
            Interval : lambda value: value, # TODO
            LargeBinary : lambda value: base64.b64encode(value),
            PickleType: lambda value: value, # TODO
        }

    @classmethod
    def _restler_serialization_name(cls):
        """
        The lowercase model classname
        """
        return cls.__name__.lower()

    @classmethod
    def _restler_property_map(cls):
        """
        List of model property names -> property types. The names are used in
        *include_all_fields=True* Property must be from **sqlalchemy.types**
        """
        columns = cls.__table__
        column_map = dict([(name, columns.get(name).type) for name in columns.keys()])
        return column_map

    wrap_method(cls, _restler_types)
    wrap_method(cls, _restler_property_map)
    cls._restler_serialization_name = _restler_serialization_name

    return cls

