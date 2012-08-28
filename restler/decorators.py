

def ae_db_serializer(cls):
    from google.appengine.ext import db

    @classmethod
    def restler_collection_types(cls, obj):
        if isinstance(obj, db.Query):
            return True
        else:
            return False

    @classmethod
    def restler_kind(cls, model):
        return model.kind().lower()

    @classmethod
    def restler_properties(cls, model):
        return list(model.properties().iterkeys())

    cls.restler_collection_types = restler_collection_types
    cls.restler_kind = restler_kind
    cls.restler_properties = restler_properties

    return cls


def ae_ndb_serializer(cls):
    from google.appengine.ext import ndb

    @classmethod
    def restler_collection_types(cls, obj):
        if isinstance(obj, ndb.query.Query):
            return True
        else:
            return False

    @classmethod
    def restler_kind(cls, model):
        try:
            return model.__class__.__name__.lower()
        except:
            # TODO When is this the case?
            return model.__name__.lower()

    @classmethod
    def restler_properties(cls, model):
        return list(model._properties.iterkeys())

    cls.restler_collection_types = restler_collection_types
    cls.restler_kind = restler_kind
    cls.restler_properties = restler_properties

    return cls
