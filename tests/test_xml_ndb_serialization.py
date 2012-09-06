
import unittest

from datetime import datetime
from xml.etree import ElementTree as ET

from google.appengine.api import users
from restler.serializers import ModelStrategy, to_xml

from tests.models import NdbModel1, NdbModel2


class TestXmlSerialization(unittest.TestCase):

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
        m.user = users.get_current_user()
        m.text = "text"
        m.put()

    def tearDown(self):
        for e in NdbModel1.query():
            e.key.delete()
        for e in NdbModel2.query():
            e.key.delete()

    def test_alias(self):
        ss = ModelStrategy(NdbModel1) + [{"the_text": "text"}]
        tree = ET.fromstring(to_xml(NdbModel1.query(), ss))
        self.assertEqual(len(tree.findall(".//ndbmodel1")), 2)
        self.assertEqual(len(tree.findall(".//the_text")), 2)
        self.assertEqual(tree.findall(".//the_text")[1].text, 'text')

    def test_change_output(self):
        ss = ModelStrategy(NdbModel1, output_name="person") + [{"the_text": lambda o: o.text}]
        tree = ET.fromstring(to_xml(NdbModel1.query(), ss))
        self.assertEqual(len(tree.findall(".//person")), 2)
        self.assertEqual(len(tree.findall(".//the_text")), 2)

    def test_property(self):
        ss = ModelStrategy(NdbModel1) + [{"text": lambda o: "the_text"}]
        tree = ET.fromstring(to_xml(NdbModel1.query(), ss))
        self.assertEqual(len(tree.findall(".//the_text")), 0)

    def test_cached_property(self):
        ss = ModelStrategy(NdbModel2).include('my_cached_property')
        tree = ET.fromstring(to_xml(NdbModel2.query(), ss))
        self.assertEqual(len(tree.findall(".//my_cached_property")), 1)
