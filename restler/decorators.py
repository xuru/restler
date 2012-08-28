

def ae_db_serializer(cls):
    @classmethod
    def restler_properties(cls, model):
        return list(model.properties().iterkeys())

    @classmethod
    def restler_kind(cls, model):
        return model.kind()

    cls.restler_properties = restler_properties
    cls.restler_kind = restler_kind

    return cls


def ae_ndb_serializer(cls):
    @classmethod
    def restler_properties(cls, model):
        return list(model._properties.iterkeys())

    @classmethod
    def restler_kind(cls, model):
        try:
            return model.__class__.__name__
        except:
            # When is this the case?
            return model.__name__

    cls.restler_properties = restler_properties
    cls.restler_kind = restler_kind

    return cls
