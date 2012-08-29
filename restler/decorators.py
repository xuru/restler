

def ae_db_serializer(cls):
    from google.appengine.api import users
    from google.appengine.ext import blobstore, db

    @classmethod
    def restler_collection_types(cls, obj):
        if isinstance(obj, db.Query):
            return True
        else:
            return False

    @classmethod
    def restler_encoder(cls, obj):
        if isinstance(obj, db.GeoPt):
            return "%s %s" % (obj.lat, obj.lon)
        if isinstance(obj, db.IM):
            return "%s %s" % (obj.protocol, obj.address)
        if isinstance(obj, users.User):
            return obj.user_id() or obj.email()
        if isinstance(obj, blobstore.BlobInfo):
            return str(obj.key())  # TODO is this correct?

    @classmethod
    def restler_kind(cls, model):
        return model.kind().lower()

    @classmethod
    def restler_properties(cls, model):
        return list(model.properties().iterkeys())

    cls.restler_collection_types = restler_collection_types
    cls.restler_encoder = restler_encoder
    cls.restler_kind = restler_kind
    cls.restler_properties = restler_properties

    return cls


def ae_ndb_serializer(cls):
    from google.appengine.api import users
    from google.appengine.ext import ndb

    @classmethod
    def restler_collection_types(cls, obj):
        if isinstance(obj, ndb.query.Query):
            return True
        else:
            return False

    @classmethod
    def restler_encoder(cls, obj):
        if isinstance(obj, ndb.GeoPt):
            return "%s %s" % (obj.lat, obj.lon)
        if isinstance(obj, users.User):
            return obj.user_id() or obj.email()

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
    cls.restler_encoder = restler_encoder
    cls.restler_kind = restler_kind
    cls.restler_properties = restler_properties

    return cls
