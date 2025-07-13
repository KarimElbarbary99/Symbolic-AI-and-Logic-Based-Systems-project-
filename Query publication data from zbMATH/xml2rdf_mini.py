import xml.etree.ElementTree as ET
from rdflib import Graph, Namespace, Literal, URIRef
from urllib.parse import quote


xml_location_path = "mini-dataset.xml"  # Edit this path to point to your XML file
rdf_path = 'C:\\Users\\PC\\Desktop\\mini_rdf.rdf'  # Edit this path to point to the resulting RDF file

def parse_xml_file(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        xml_content = ''.join(file.readlines()[1:])  # Skip the first line

    # Parse the XML content
    return ET.fromstring(xml_content)

def extract_information(root):
    
    namespaces = {
        'oai': 'http://www.openarchives.org/OAI/2.0/',
        'zbmath': 'https://zbmath.org/zbmath/elements/1.0/'
    }

    for record in root.findall('.//oai:record', namespaces):
        metadata = record.find('.//zbmath:document_id', namespaces)
        document_id = metadata.text if metadata is not None else 'N/A'

        authors = record.findall('.//zbmath:author_id', namespaces)
        author_ids = [author.text for author in authors]

        classifications = record.findall('.//zbmath:classification', namespaces)
        classification_list = [classification.text for classification in classifications]

        keywords = record.findall('.//zbmath:keyword', namespaces)
        keyword_list = [keyword.text for keyword in keywords]

        publication_year_element = record.find('.//zbmath:publication_year', namespaces)
        publication_year = publication_year_element.text if publication_year_element is not None else 'N/A'

        yield {
            'document_id': document_id,
            'author_ids': author_ids,
            'classifications': classification_list,
            'keywords': keyword_list,
            'publication_year': publication_year
        }

root = parse_xml_file(xml_location_path)

# Extract information
parsed_data = []
for info in extract_information(root):
      parsed_data.append(info)
      
# Create an RDF graph
rdf_graph = Graph()

zbmath = Namespace('https://zbmath.org/')

for data in parsed_data:
    document_id = data['document_id']

    # Create a URI for the document
    document_uri = URIRef(f"{zbmath}?q=an%3A{document_id}")

    # Add triples to the graph
    rdf_graph.add((document_uri, zbmath.document_id, document_uri))

    for classification in data['classifications']:
        classification_uri = URIRef(f"{zbmath}classification/?q=cc%3A{classification}")
        rdf_graph.add((document_uri, zbmath.classification, classification_uri))

    for author_id in data['author_ids']:
        author_uri = URIRef(f"{zbmath}authors/?q=ai%3A{author_id}")
        rdf_graph.add((document_uri, zbmath.author_id, author_uri))

    for keyword in data['keywords']:
        keyword = keyword.replace(' ', '+')
        keyword = quote(keyword, safe="~:/?=&-_.(),;+'")
        keyword_uri = URIRef(f"{zbmath}?q=ut%3A{keyword}")
        rdf_graph.add((document_uri, zbmath.keyword, keyword_uri))

    rdf_graph.add((document_uri, zbmath.publicationYear, Literal(data['publication_year'])))


rdf_xml = rdf_graph.serialize(rdf_path,format='xml')


