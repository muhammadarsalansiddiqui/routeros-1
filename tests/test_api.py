import unittest

from routeros.api import Query, Parser


class MockedAPI:
    def __call__(self, command, *words):
        return [command] + [word for word in words]


class TestQuery(unittest.TestCase):
    def setUp(self):
        self.api = MockedAPI()
        self.command = '/ip/pool/print'
        self.query = Query(self.api, self.command)

    def test_query(self):
        # We don't need the attributes in order.
        expected_equal = sorted([self.command, '?=foo=bar', '?=bar=foo'])
        self.assertEqual(self.query.equal(foo='bar', bar='foo')[0], self.command)
        self.assertEqual(sorted(self.query.equal(foo='bar', bar='foo')), expected_equal)

        expected_has = sorted([self.command, '?foo', '?bar'])
        self.assertEqual(self.query.equal(foo='bar', bar='foo')[0], self.command)
        self.assertEqual(sorted(self.query.has('foo', 'bar')), expected_has)

        expected_hasnot = sorted([self.command, '?-foo', '?-bar'])
        self.assertEqual(self.query.equal(foo='bar', bar='foo')[0], self.command)
        self.assertEqual(sorted(self.query.hasnot('foo', 'bar')), expected_hasnot)

        expected_lower = sorted([self.command, '?<foo=bar', '?<bar=foo'])
        self.assertEqual(self.query.equal(foo='bar', bar='foo')[0], self.command)
        self.assertEqual(sorted(self.query.lower(foo='bar', bar='foo')), expected_lower)

        expected_greater = sorted([self.command, '?>foo=bar', '?>bar=foo'])
        self.assertEqual(self.query.equal(foo='bar', bar='foo')[0], self.command)
        self.assertEqual(sorted(self.query.greater(foo='bar', bar='foo')), expected_greater)


class TestParser(unittest.TestCase):
    def setUp(self):
        self.attributes = (
            {
                'attr': '=.id=value',
                'key': '.id',
                'value': 'value',
            },
            {
                'attr': '=name=ether1',
                'key': 'name',
                'value': 'ether1',
            },
            {
                'attr': '=comment=',
                'key': 'comment',
                'value': '',
            }
        )
    
    def test_parse_word(self):
        for attribute in self.attributes:
            self.assertEqual(Parser.parse_word(attribute['attr']),
                             (attribute['key'], attribute['value']))
        
    def test_compose_word(self):
        for attribute in self.attributes:
            attr = Parser.compose_word(attribute['key'], attribute['value'])
            self.assertEqual(attribute['attr'], attr)
