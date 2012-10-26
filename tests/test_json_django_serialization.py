from env_setup import setup_django; setup_django()
import json
import unittest

from django.db import connection
from django.db import models

from restler import decorators, UnsupportedTypeError
from restler.serializers import ModelStrategy, to_json


@decorators.django_serializer
class Model1(models.Model):
    # Simple fields
    # field1 = models.AutoField() # - This will be created automatically
    big_integer = models.BigIntegerField(null=True, default=1)
    boolean = models.BooleanField(default=False)
    char = models.CharField(max_length=10, null=True, default="CharField")
    comma_separated_int = models.CommaSeparatedIntegerField(max_length=20, default=[1, 2, 3])
    _date = models.DateField(null=True, auto_now=True)
    _datetime = models.DateTimeField(null=True, auto_now=True)
    decimal = models.DecimalField(max_digits=20, decimal_places=2, null=True, default="10.20")
    email = models.EmailField(null=True, default="test@test.com")
    _float = models.FloatField(null=True, default=10.2)
    integer = models.IntegerField(null=True, default=2)
    ip_address = models.IPAddressField(null=True, default="127.0.0.1")
    null_boolean = models.NullBooleanField(null=True)
    positive_int = models.PositiveIntegerField(null=True, default=2)
    positive_small_int = models.PositiveSmallIntegerField(null=True, default=2)
    slug = models.SlugField(null=True, default="Some combination of 1 23")
    small_int = models.SmallIntegerField(null=True, default=2)
    text = models.TextField(null=True, default="Some Text")
    _time = models.TimeField(null=True, auto_now=True)
    url = models.URLField(null=True, default="http://www.yahoo.com")

    # unsupported types
    _file = models.FileField(upload_to=".", null=True)
    file_path = models.FilePathField(null=True)
    image = models.ImageField(upload_to=".")

    # Relationship fields
    rel1 = models.ForeignKey("Model1", related_name="set1", null=True)
    rel2 = models.ManyToManyField("Model1", related_name="set2", null=True)
    rel3 = models.OneToOneField("Model1", null=True)

    class Meta:
        app_label = 'test'

    def __unicode__(self):
        return "Model1 -> %s, %s, %s" % (self.id, self.big_integer, self.char)


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
        connection.creation.create_test_db(0, autoclobber=True)
        install_model(Model1)
        self.model1 = Model1(
            big_integer=1,
            boolean=True,
            char="2"
        )
        self.model1.save()

    def test_simple(self):
        ss = ModelStrategy(Model1, include_all_fields=True).exclude('_file', 'file_path', 'image')
        sj = json.loads(to_json(Model1.objects.all(), ss))
        self.assertEqual(sj[0]['big_integer'], 1)
        self.assertEqual(sj[0]['char'], u'2')
        ss = ss.include(aggregate=lambda o: '%s, %s' % (o.big_integer, o.char))
        sj = json.loads(to_json(Model1.objects.all(), ss))
        self.assertEqual(sj[0]['aggregate'], u'1, 2')

    def test_file_field_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            ss = ModelStrategy(Model1, include_all_fields=False).include('_file')
            to_json(Model1.objects.all(), ss)

    def test_file_path_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            ss = ModelStrategy(Model1, include_all_fields=False).include('file_path')
            to_json(Model1.objects.all(), ss)

    def test_image_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            ss = ModelStrategy(Model1, include_all_fields=False).include('image')
            to_json(Model1.objects.all(), ss)

    def test_auto_field(self):
        ss = ModelStrategy(Model1, include_all_fields=False).include('id')
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), ss))
        self.assertEqual(sj.get('id'), self.model1.id)

    def test_big_integer_field(self):
        ss = ModelStrategy(Model1, include_all_fields=False).include('big_integer')
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), ss))
        self.assertEqual(sj.get('big_integer'), self.model1.big_integer)

    def test_boolean_field(self):
        ss = ModelStrategy(Model1, include_all_fields=False).include('boolean')
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), ss))
        self.assertEqual(sj.get('boolean'), self.model1.boolean)

    def test_char_field(self):
        ss = ModelStrategy(Model1, include_all_fields=False).include('char')
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), ss))
        self.assertEqual(sj.get('char'), self.model1.char)
