
def wrap_method(cls, method):
    from copy import copy
    method_name = method.__func__.__name__
    method_param = method
    if hasattr(cls, method_name):
        orig_cls_method = getattr(cls, method_name)
        @classmethod
        def wrap(cls_):
            setattr(cls, method_name, method_param)
            method =  getattr(cls, method_name)
            aggregate = copy(orig_cls_method())
            if isinstance(aggregate, list): #_restler_types()
                aggregate = set(aggregate)
                aggregate.update(method())
                aggregate = list(aggregate)
            elif isinstance(aggregate, dict): #_restler_property_names
                aggregate.update(method())
            elif isinstance(aggregate, str):
                # Developer shouldn't really do this, but we'll try
                # to do the correct thing and use the most recently defined name
                aggregate = method() # _restler_serialization_name
            return aggregate
        setattr(cls, method_name, wrap)
    else:
        setattr(cls, method_name, method)


def ae_db_serializer(cls):
    """
    Restler class decorator for google.appengine.ext.db.Model for serialization
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
            db.Query : lambda query: [obj for obj in query],
            db.GeoPt : lambda obj: "%s %s" % (obj.lat, obj.lon),
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
    def _restler_property_names(cls):
        """
        List of model property names if *include_all_fields=True*
        Property must be from **google.appengine.ext.db.Property**
        """
        return list(cls.properties().iterkeys())

    wrap_method(cls, _restler_types)
    wrap_method(cls, _restler_property_names)
    cls._restler_serialization_name = _restler_serialization_name

    return cls


def ae_ndb_serializer(cls):
    """
    Restler class decorator for google.appengine.ext.ndb.Model for serialization
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
            ndb.query.Query : lambda query: [obj for obj in query],
            ndb.GeoPt : lambda obj: "%s %s" % (obj.lat, obj.lon),
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
    def _restler_property_names(cls):
        """
        List of model property names if *include_all_fields=True*
        Property must be from **google.appengine.ext.ndb.Property**
        """
        return list(cls._properties.iterkeys())

    wrap_method(cls, _restler_types)
    wrap_method(cls, _restler_property_names)
    cls._restler_serialization_name = _restler_serialization_name

    return cls
