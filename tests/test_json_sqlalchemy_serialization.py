
import json
import pickle

from datetime import datetime, time, timedelta
from unittest import TestCase

from restler import UnsupportedTypeError
from restler.serializers import ModelStrategy, to_json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqla_models import Base, Model1


class TestUnsupportedTypes(TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.model1 = Model1(
            binary='\xff\xd8\xff\xe1A\xecExif',
            interval=timedelta(1),
            pickle_type=pickle.dumps([1, 2, 3])
        )
        self.session.add(self.model1)
        self.strategy = ModelStrategy(Model1, include_all_fields=False)

    def test_binary_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('binary')
            to_json(self.session.query(Model1).all(), strategy)

    def test_interval_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('interval')
            to_json(self.session.query(Model1).all(), strategy)

    def test_large_binary_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('large_binary')
            to_json(self.session.query(Model1).all(), strategy)

    def test_pickle_type_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('pickle_type')
            to_json(self.session.query(Model1).all(), strategy)


class TestTypes(TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=False)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.model1 = Model1(
            boolean=True,
            interval=timedelta(1),
            _float=5.5,
            string='A string',
            text='Some text'
        )
        self.session.add(self.model1)
        self.strategy = ModelStrategy(Model1, include_all_fields=False)

    def test_simple(self):
        strategy = self.strategy.include('id', 'string')
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0]['string'], "A string")
        self.assertEqual(sj[0]['id'], 1)
        #ss = ss.include(aggregate=lambda o: '%s, %s' % (o.string, o.field4))
        #sj = json.loads(to_json(Model1.objects.all(), ss))
        #self.assertEqual(sj[0]['aggregate'], u'1, 2')

    def test_integer_field(self):
        field = 'id'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), getattr(self.model1, field))

    def test_boolean_field(self):
        field = 'boolean'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), getattr(self.model1, field))

    def test_date_field(self):
        field = '_date'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), datetime.strftime(getattr(self.model1, field), '%Y-%m-%d'))

    def test_date_time_field(self):
        field = '_datetime'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), datetime.strftime(getattr(self.model1, field), '%Y-%m-%d %H:%M:%S'))

    def test_float_field(self):
        field = '_float'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), getattr(self.model1, field))

    def test_string_field(self):
        field = 'string'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), getattr(self.model1, field))

    def test_text_field(self):
        field = 'text'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), getattr(self.model1, field))

    def test_time_field(self):
        field = '_time'
        strategy = self.strategy.include(field)
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0].get(field), time.strftime(getattr(self.model1, field), '%H:%M:%S'))
