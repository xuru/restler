from env_setup import setup_django; setup_django()

import json

from datetime import datetime, time
from unittest import TestCase

from django.db import models, connection

from restler import decorators, UnsupportedTypeError
from restler.serializers import ModelStrategy, to_json


@decorators.django_serializer
class Model1(models.Model):
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


class TestDjangoUnsupportedFields(TestCase):
    def setUp(self):
        connection.creation.create_test_db(0, autoclobber=True)
        install_model(Model1)
        self.model1 = Model1()
        self.model1.save()
        self.strategy = ModelStrategy(Model1, include_all_fields=False)

    def test_file_field_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('_file')
            to_json(Model1.objects.all(), strategy)

    def test_file_path_field_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('file_path')
            to_json(Model1.objects.all(), strategy)

    def test_image_field_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('image')
            to_json(Model1.objects.all(), strategy)


class TestDjangoFieldJsonSerialization(TestCase):
    def setUp(self):
        connection.creation.create_test_db(0, autoclobber=True)
        install_model(Model1)
        self.model1 = Model1(
            big_integer=1,
            boolean=True,
            char="2",
            comma_separated_int=[2, 4, 6],
            decimal=9,
            email='test@domain.com',
            _float=9.5,
            integer=4,
            ip_address='8.8.1.1.',
            null_boolean=None,
            positive_int=100,
            positive_small_int=1,
            slug='Slug Field',
            small_int=1,
            text='More Text',
            url='www.google.com'
        )
        self.model1.save()
        self.strategy = ModelStrategy(Model1, include_all_fields=False)

    def test_auto_field(self):
        field = 'id'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_big_integer_field(self):
        field = 'big_integer'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_boolean_field(self):
        field = 'boolean'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_char_field(self):
        field = 'char'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_comma_separated_integer_field(self):
        field = 'comma_separated_int'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_date_field(self):
        field = '_date'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), datetime.strftime(getattr(self.model1, field), '%Y-%m-%d'))

    def test_datetime_field(self):
        field = '_datetime'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), datetime.strftime(getattr(self.model1, field), '%Y-%m-%d %H:%M:%S'))

    def test_decimal_field(self):
        field = 'decimal'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), str(getattr(self.model1, field)))

    def test_email_field(self):
        field = 'email'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_float_field(self):
        field = '_float'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_integer_field(self):
        field = 'integer'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_ip_address_field(self):
        field = 'ip_address'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_null_boolean_field(self):
        field = 'null_boolean'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_positive_integer_field(self):
        field = 'positive_int'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_positive_small_integer_field(self):
        field = 'positive_small_int'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_slug_field(self):
        field = 'slug'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_small_integer_field(self):
        field = 'small_int'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_text_field(self):
        field = 'text'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))

    def test_time_field(self):
        field = '_time'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), time.strftime(getattr(self.model1, field), '%H:%M:%S'))

    def test_url_field(self):
        field = 'url'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get(field), getattr(self.model1, field))


class TestLambdaJsonSerialization(TestCase):
    def setUp(self):
        connection.creation.create_test_db(0, autoclobber=True)
        install_model(Model1)
        self.model1 = Model1(
            big_integer=1,
            boolean=True,
            char="2",
            comma_separated_int=[2, 4, 6],
            decimal=9,
            email='test@domain.com',
            _float=9.5,
            integer=4,
            ip_address='8.8.1.1.',
            null_boolean=None,
            positive_int=100,
            positive_small_int=1,
            slug='Slug Field',
            small_int=1,
            text='More Text',
            url='www.google.com'
        )
        self.model1.save()
        self.strategy = ModelStrategy(Model1, include_all_fields=True).exclude('_file', 'file_path', 'image')

    def test_lambda(self):
        strategy = self.strategy.include(aggregate=lambda o: '%s, %s' % (o.big_integer, o.char))
        sj = json.loads(to_json(Model1.objects.get(pk=self.model1.id), strategy))
        self.assertEqual(sj.get('aggregate'), u'1, 2')
