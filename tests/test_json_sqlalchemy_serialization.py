
import json
import pickle

from datetime import timedelta
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
            interval=timedelta(1),
            pickle_type=pickle.dumps([1, 2, 3])
        )
        self.session.add(self.model1)
        self.strategy = ModelStrategy(Model1, include_all_fields=False)

    def test_interval_unsupported(self):
        with self.assertRaises(UnsupportedTypeError):
            strategy = self.strategy.include('interval')
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
            interval=timedelta(1)
        )
        self.session.add(self.model1)
        self.strategy = ModelStrategy(Model1, include_all_fields=False)

    def test_simple(self):
        strategy = self.strategy.include('id', 'field2')
        sj = json.loads(to_json(self.session.query(Model1).all(), strategy))
        self.assertEqual(sj[0]['field2'], "some string")
        self.assertEqual(sj[0]['id'], 1)
        #ss = ss.include(aggregate=lambda o: '%s, %s' % (o.field2, o.field4))
        #sj = json.loads(to_json(Model1.objects.all(), ss))
        #self.assertEqual(sj[0]['aggregate'], u'1, 2')
