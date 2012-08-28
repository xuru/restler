from google.appengine.ext import blobstore, db, ndb


class Model2(db.Model):
    model2_prop = db.StringProperty()

    @property
    def my_method(self):
        return "I say blah!"


class Model1(db.Model):
    string = db.StringProperty()
    bytestring = db.ByteStringProperty()
    boolean = db.BooleanProperty()
    integer = db.IntegerProperty()
    float_ = db.FloatProperty()
    datetime = db.DateTimeProperty()
    date = db.DateProperty()
    time = db.TimeProperty()
    list_ = db.ListProperty(long)
    stringlist = db.StringListProperty()
    reference = db.ReferenceProperty(reference_class=Model2, collection_name="references")
    selfreference = db.SelfReferenceProperty(collection_name="models")
    blobreference = blobstore.BlobReferenceProperty()
    user = db.UserProperty()
    blob = db.BlobProperty()
    text = db.TextProperty()
    category = db.CategoryProperty()
    link = db.LinkProperty()
    email = db.EmailProperty()
    geopt = db.GeoPtProperty()
    im = db.IMProperty()
    phonenumber = db.PhoneNumberProperty()
    postaladdress = db.PostalAddressProperty()
    rating = db.RatingProperty()


class NdbModel2(ndb.Model):
    model2_prop = ndb.StringProperty()

    @property
    def my_method(self):
        return "I say blah!"


class NdbModel1(ndb.Model):
    string = ndb.StringProperty()
    boolean = ndb.BooleanProperty()
    integer = ndb.IntegerProperty()
    float_ = ndb.FloatProperty()
    datetime = ndb.DateTimeProperty()
    date = ndb.DateProperty()
    time = ndb.TimeProperty()
    user = ndb.UserProperty()
    blob = ndb.BlobProperty()
    text = ndb.TextProperty()
    geopt = ndb.GeoPtProperty()
    stringlist = ndb.StringProperty(repeated=True)
    integerlist = ndb.IntegerProperty(repeated=True)
    # blob_key = ndb.BlobKeyProperty()
    # structured = ndb.StructuredProperty()
    # local_structured = ndb.LocalStructuredProperty()
    # json_ = ndb.JsonProperty()
    # pickle_ = ndb.PickleProperty()
    # generic = ndb.GenericProperty()
    # computed = ndb.ComputedProperty()
