from env_setup import setup_django; setup_django()
import json
import unittest

from django.db import connection
from django.db import models

from restler import decorators
from restler.serializers import ModelStrategy, to_json


@decorators.django_serializer
class Model1(models.Model):
    # Simple fields
    # field1 = models.AutoField() # - This will be created automatically
    field2 = models.BigIntegerField(null=True, default=1)
    field3 = models.BooleanField(default=False)
    field4 = models.CharField(max_length=10, null=True, default="CharField")
    field5 = models.CommaSeparatedIntegerField(max_length=20, default=[1, 2, 3])
    field6 = models.DateField(null=True, auto_now=True)
    field7 = models.DateTimeField(null=True, auto_now=True)
    field8 = models.DateTimeField(null=True, auto_now=True)
    field9 = models.DecimalField(max_digits=20, decimal_places=2, null=True, default="10.20")
    field10 = models.EmailField(null=True, default="test@test.com")
    # field11 = models.FileField(upload_to=".", null=True)  # UnsupportedTypeError
    # field12 = models.FilePathField(null=True)  # UnsupportedTypeError
    field13 = models.FloatField(null=True, default=10.2)
    # field14 = models.ImageField(upload_to=".")   # UnsupportedTypeError
    field15 = models.IntegerField(null=True, default=2)
    field16 = models.IPAddressField(null=True, default="127.0.0.1")
    field17 = models.NullBooleanField(null=True)
    field18 = models.PositiveIntegerField(null=True, default=2)
    field18 = models.PositiveSmallIntegerField(null=True, default=2)
    field19 = models.SlugField(null=True, default="Some combination of 1 23")
    field20 = models.SmallIntegerField(null=True, default=2)
    field21 = models.TextField(null=True, default="Some Text")
    field22 = models.TimeField(null=True, auto_now=True)
    field23 = models.URLField(null=True, default="http://www.yahoo.com")

    # Relationship fields
    rel1 = models.ForeignKey("Model1", related_name="set1", null=True)
    rel2 = models.ManyToManyField("Model1", related_name="set2", null=True)
    rel3 = models.OneToOneField("Model1", null=True)

    class Meta:
        app_label = 'test'

    def __unicode__(self):
        return "Model1 -> %s, %s, %s" % (self.id, self.field2, self.field4)


def install_model(model):
    from django.core.management import color

    # Standard syncdb expects models to be in reliable locations,
    # so dynamic models need to bypass django.core.management.syncdb.
    # On the plus side, this allows individual models to be installed
    # without installing the entire project structure.
    # On the other hand, this means that things like relationships and
    # indexes will have to be handled manually.
    # This installs only the basic table definition.

    # disable terminal colors in the sql statements
    style = color.no_style()

    cursor = connection.cursor()
    statements, pending = connection.creation.sql_create_model(model, style)
    for stmt in statements:
        cursor.execute(stmt)


def flip(*args, **kwargs):
    return json.loads(to_json(*args, **kwargs))


class TestJsonSerialization(unittest.TestCase):
    def setUp(self):
        connection.creation.create_test_db(2, autoclobber=True)
        install_model(Model1)
        self.model1 = Model1(field2=1, field4="2")
        self.model1.save()

    def test_simple(self):
        ss = ModelStrategy(Model1, include_all_fields=True)
        sj = json.loads(to_json(Model1.objects.all(), ss))
        self.assertEqual(sj[0]['field2'], 1)
        self.assertEqual(sj[0]['field4'], u'2')
        ss = ss.include(aggregate=lambda o: '%s, %s' % (o.field2, o.field4))
        sj = json.loads(to_json(Model1.objects.all(), ss))
        self.assertEqual(sj[0]['aggregate'], u'1, 2')


"""
<Insert Brian's Tests Here/>
"""
