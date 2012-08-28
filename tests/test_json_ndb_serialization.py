import json
import unittest

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb
from restler.serializers import ModelStrategy, to_json, SKIP

from tests.models import NdbModel1, NdbModel2


def flip(*args, **kwargs):
    return json.loads(to_json(*args, **kwargs))


class TestJsonSerialization(unittest.TestCase):

    def setUp(self):
        for e in NdbModel1.query():
            e.key.delete()
        for e in NdbModel2.query():
            e.key.delete()
        ref = NdbModel1()
        ref.put()
        m = NdbModel1()
        m2 = NdbModel2()
        m2.put()
        m.string = "string"
        m.boolean = True
        m.integer = 123
        m.float_ = 22.0
        m.datetime = datetime.now()
        m.date = datetime.now().date()
        m.time = datetime.now().time()
        m.stringlist = ["one", "two", "three"]
        m.integerlist = [1, 2, 3]
        m.user = users.get_current_user()
        m.blob = "binary data"  # Todo
        m.text = "text"
        m.geopt = ndb.GeoPt("1.0, 2.0")
        m.put()

    def tearDown(self):
        for e in NdbModel1.query():
            e.key.delete()
        for e in NdbModel2.query():
            e.key.delete()

    def test_nomodel(self):
        self.assertEqual(flip({'success': True}), {"success": True})

    def test_simple(self):
        ss = ModelStrategy(NdbModel1) + [{"the_text": "text"}]
        sj = json.loads(to_json(NdbModel1.query(), ss))
        self.assertEqual(sj[1], {u'the_text': u'text'})

    def test_simple_property(self):
        ss = ModelStrategy(NdbModel1) + [{"the_text": lambda o: o.text}]
        sj = json.loads(to_json(NdbModel1.query(), ss))
        self.assertEqual(sj[1], {u'the_text': u'text'})

    def test_exclude_fields(self):
        ss = ModelStrategy(NdbModel1, include_all_fields=True) - ["date", "time", "datetime"]
        sj = json.loads(to_json(NdbModel1.query(), ss))
        self.assertEqual(sj[1],
            {
                u'string': u'string',
                u'stringlist': [u'one', u'two', u'three'],
                u'text': u'text',
                u'float_': 22.0, u'blob': u'binary data',
                u'geopt': u'1.0 2.0', u'boolean': True,
                u'integer': 123,
                u'integerlist': [1, 2, 3],
                u'user': None
            }
        )

    def test_valid_serialization(self):
        ss = ModelStrategy(NdbModel1, include_all_fields=True) - ["date", "time", "datetime"]
        q = NdbModel1.query()
        dict_data = {'foo': 'foo', 'models': q}
        sj = json.loads(to_json(dict_data, ss))
        self.assertEqual(sj['models'][1],
            {
                u'string': u'string',
                u'stringlist': [u'one', u'two', u'three'],
                u'text': u'text',
                u'float_': 22.0, u'blob': u'binary data',
                u'geopt': u'1.0 2.0', u'boolean': True,
                u'integer': 123,
                u'integerlist': [1, 2, 3],
                u'user': None
            }
        )

    def test_alias_field(self):
        self.assertEqual(flip(NdbModel2(), ModelStrategy(NdbModel2) + [{"my_method": "my_method"}]),
            {"my_method": "I say blah!"})

    def test_alias_field2(self):
        self.assertEqual(flip(NdbModel2(), ModelStrategy(NdbModel2) + ["my_method"]),
            {"my_method": "I say blah!"})

    def test_alias_field3(self):
        self.assertEqual(flip(NdbModel2(), ModelStrategy(NdbModel2)
            + [{"my_method": lambda obj, context: context["foo"]}], context={"foo": "woohoo"}),
            {"my_method": "woohoo"})

    def test_alias_field4(self):
        self.assertEqual(flip(NdbModel2(), ModelStrategy(NdbModel2) + [{"yes": lambda o: "yes"}, {"no": lambda o: SKIP}]),
            {"yes": "yes"})