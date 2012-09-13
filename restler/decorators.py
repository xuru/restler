


def ae_db_serializer(cls):
    """
    Restler class decorator for google.appengine.ext.db.Model for serialization
    """
    from google.appengine.ext import blobstore, db

    @classmethod
    def restler_types(cls):
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
    def restler_serialization_name(cls):
        """
        The lowercase model classname
        """
        return cls.kind().lower()

    @classmethod
    def restler_property_names(cls):
        """
        List of model property names if *include_all_fields=True*
        Property must be from **google.appengine.ext.db.Property**
        """
        return list(cls.properties().iterkeys())

    cls._restler_types = restler_types
    cls._restler_serialization_name = restler_serialization_name
    cls._restler_property_names = restler_property_names

    return cls


def ae_ndb_serializer(cls):
    """
    Restler class decorator for google.appengine.ext.ndb.Model for serialization
    """
    from google.appengine.ext import ndb

    @classmethod
    def restler_types(cls):
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
    def restler_serialization_name(cls):
        """
        The lowercase model classname
        """
        return cls.__name__.lower()

    @classmethod
    def restler_property_names(cls):
        """
        List of model property names if *include_all_fields=True*
        Property must be from **google.appengine.ext.ndb.Property**
        """
        return list(cls._properties.iterkeys())

    cls._restler_types = restler_types
    cls._restler_serialization_name = restler_serialization_name
    cls._restler_property_names = restler_property_names

    return cls
