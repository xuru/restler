

def ae_db_serializer(cls):
    @classmethod
    def restler_kind(cls, model):
        return model.kind().lower()

    @classmethod
    def restler_properties(cls, model):
        return list(model.properties().iterkeys())

    cls.restler_kind = restler_kind
    cls.restler_properties = restler_properties

    return cls


def ae_ndb_serializer(cls):
    @classmethod
    def restler_kind(cls, model):
        try:
            return model.__class__.__name__.lower()
        except:
            # When is this the case?
            return model.__name__.lower()

    @classmethod
    def restler_properties(cls, model):
        return list(model._properties.iterkeys())

    cls.restler_kind = restler_kind
    cls.restler_properties = restler_properties

    return cls
