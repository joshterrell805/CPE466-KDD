import unittest
from io import StringIO
from document import Document
from elements.stopword import StopwordElement
from elements.porterstemmer import PorterStemmerElement
from elements.summary import SummaryElement
from elements.jsonreader import JsonReader
from elements.freqcounter import FreqCounter
from elements.queryparser import QueryParser
from elements.querymetadataparser import QueryMetadataParser

class TestModelBuilder(unittest.TestCase):
    def testStopwords(self):
        doc_itr = FakeParser({'words': {'this': 3, 'that': 2, 'these': 4, 'those': 5}})
        sw_itr = iter(StopwordElement(doc_itr, ['these', 'those']))
        self.assertEqual(next(sw_itr), document({'this': 3, 'that': 2}))

    def testStemming(self):
        doc_itr = FakeParser({'words': {'caresses': 3, 'flies': 4, 'dies': 5, 'mules': 6, 'mule': 4, 'denied': 7}})
        stem_itr = iter(PorterStemmerElement(doc_itr))
        self.assertEqual(next(stem_itr), document({'caress': 3, 'fli': 4, 'die': 5, 'mule': 10, 'deni': 7}))

    def testAccumulator(self):
        documents = [document({'this': 3, 'that': 2, 'these': 4, 'those': 5}),
                     document({'this': 2, 'those': 2})]
        documents[0]['text'] = "abc def ghi" # 11 characters
        documents[1]['text'] = "lpq 345" # 7 characters
        # Run all the documents through the summary filter
        summary = SummaryElement(x for x in documents)
        for doc in summary:
            pass
        self.assertEqual({'this': 2, 'that': 1, 'these': 1, 'those': 2}, summary.DF())
        self.assertEqual({'this': 0, 'that': 1, 'these': 1, 'those': 0}, summary.IDF())
        self.assertEqual(9, summary.averageLength())

    def testReader(self):
        with open('elements/test.json') as fh:
            read_itr = JsonReader(fh)
            data = [document for document in read_itr]
            expected = [{'words': {'first' : 1}},
                        {'things': {'second' : 2}},
                        {'another': {'third' : 3}}]
            self.assertEqual(expected, data)
        fh.close()

    def testFreqCount(self):
        doc_itr = FakeParser({'text': "first second first second second"})
        freq_itr = iter(FreqCounter(doc_itr, 'text'))
        data = next(freq_itr)
        expected = {'text': "first second first second second",
                    'words': {'first': 2, 'second': 3}}
        self.assertEqual(expected, data)

    def testQueryParser(self):
        query_itr = iter(QueryParser("abc def"))
        query = next(query_itr)
        self.assertEqual({'text': "abc def"}, query)

    def testQueryMetadataParser(self):
        p = QueryMetadataParser(
                [{'query': '<a:2,b:3,b:z> apples'}])
        doc = next(p)
        self.assertEqual(doc['query'], ' apples')
        self.assertEqual(p.metaData, {'a': ['2'], 'b': ['3', 'z']})

        p = QueryMetadataParser(
                [{'query': 'apples are good'}])
        doc = next(p)
        self.assertEqual(doc['query'], 'apples are good')
        self.assertEqual(p.metaData, {})

def document(words):
    return {'words': words}

class FakeParser:
    def __init__(self, doc):
        self.__doc = doc

    def __iter__(self):
        return iter([self.__doc])
