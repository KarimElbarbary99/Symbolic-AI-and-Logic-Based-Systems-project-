import xml.sax
import io
import requests
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, DCTERMS

xml_location_path = "zbMathOpen_OAIPMH_int (1).xml"  # Edit this path to point to your XML file
rdf_path = 'C:\\Users\\PC\\Desktop\\zbMathOpen_OAIPMH_int.rdf'  # Edit this path to point to the resulting RDF file

# Define your namespaces
ZBMATH = Namespace("https://zbmath.org/")

class MyContentHandler(xml.sax.ContentHandler):
    def __init__(self, g):
        super().__init__()
        self.g = g
        self.currentElement = ''
        self.currentRecord = None
        self.buffer = ''  # To capture the text content of XML elements

    def startElement(self, name, attrs):
        self.currentElement = name
        self.buffer = ''  # Reset the buffer
        if name == 'record':
            self.currentRecord = {}  # Initialize a dictionary for the current record's data

    def endElement(self, name):
        if self.currentRecord is not None:
            if name == 'zbmath:document_id':
                document_id = self.buffer.strip()
                self.currentRecord['document_id'] = URIRef(f"https://zbmath.org/?q=an%3A{document_id}")
            elif name == 'zbmath:classification':
                classification = self.buffer.strip()
                self.currentRecord.setdefault('classifications', []).append(URIRef(f"https://zbmath.org/classification/?q=cc%3A{classification}"))
            elif name == 'zbmath:author_id':
                author_id = self.buffer.strip()
                self.currentRecord.setdefault('author_ids', []).append(URIRef(f"https://zbmath.org/authors/?q=ai%3A{author_id}"))
            elif name == 'zbmath:keyword':
                keyword = self.buffer.strip()
                self.currentRecord.setdefault('keywords', []).append(Literal(keyword))
            elif name == 'zbmath:publication_year':
                publication_year = self.buffer.strip()
                self.currentRecord['publication_year'] = Literal(publication_year)

        if name == 'record':
            # Process completed record data to RDF
            if 'document_id' in self.currentRecord:
                doc_uri = self.currentRecord['document_id']
                self.g.add((doc_uri, RDF.type, ZBMATH.Publication))
                for cls in self.currentRecord.get('classifications', []):
                    self.g.add((doc_uri, ZBMATH.classification, cls))
                for author in self.currentRecord.get('author_ids', []):
                    self.g.add((doc_uri, ZBMATH.author, author))
                for keyword in self.currentRecord.get('keywords', []):
                    self.g.add((doc_uri, ZBMATH.keyword, keyword))
                if 'publication_year' in self.currentRecord:
                    self.g.add((doc_uri, ZBMATH.publicationYear, self.currentRecord['publication_year']))

    def characters(self, content):
        self.buffer += content  # Append the text content to the buffer

class CustomInputSource(xml.sax.xmlreader.InputSource):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def getCharacterStream(self):
        file = open(self.file_path, 'r', encoding='utf-8')
        file.readline()  # Skip the first line
        return file


def convert_xml_to_rdf(xml_path, rdf_output_path):
    g = Graph()
    handler = MyContentHandler(g)
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)

    # Create a custom input source and parse it
    input_source = CustomInputSource(xml_path)
    try:
        parser.parse(input_source)
    finally:
        input_source.getCharacterStream().close()  # Ensure file is closed after parsing

    g.serialize(destination=rdf_output_path, format='xml')

convert_xml_to_rdf(xml_location_path, rdf_path)

