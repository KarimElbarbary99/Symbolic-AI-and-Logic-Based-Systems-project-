import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote
from urllib.parse import urlparse, parse_qs, unquote

xml_file_path = "C:\\Users\\PC\\Downloads\\example-problems-big.xml"  # Edit this path to point to your XML file containing the problems
rdf_path = "C:/Users/PC/Desktop/zbMathOpen_OAIPMH_int.rdf"  # Edit this path to point to the your RDF file
solution_xml_path = "solutions_big.xml"  # Edit this path to point to the resulting XML file containing the solutions

def transform_xml(input_xml, query_in,id,type):

    name_space = {'xmlns': 'http://www.w3.org/2005/sparql-results#',
                  'zbmath': 'https://zbmath.org/zbmath/elements/1.0/'}
    # Parse the input XML
    root = ET.fromstring(input_xml)

    # Create a new XML tree for the desired format
    solution = ET.Element("Solution", id=str(id))
    query = ET.SubElement(solution, "Query")
    # Iterate over result elements and create Solution elements
    for idx, result in enumerate(root.findall(".//xmlns:result", namespaces=name_space)):
        
        query.text = query_in
        if type == 'coauthors':

            for author_uri in result.findall(".//xmlns:uri", namespaces=name_space):
                author = ET.SubElement(solution, "Author")
                author.text = author_uri.text
        elif type == 'msc-intersection':
            for paper_uri in result.findall(".//xmlns:uri", namespaces=name_space):
                paper = ET.SubElement(solution, "Paper")
                paper.text = paper_uri.text

        elif type == 'top-authors':
            for author_uri in result.findall(".//xmlns:uri", namespaces=name_space):
                author = ET.SubElement(solution, "Author",count="")
                num = result.find(".//xmlns:literal", namespaces=name_space).text
                author.set("count",num)
                author.text = author_uri.text
                               
            

    transformed_tree = ET.ElementTree(solution)

    transformed_xml = ET.tostring(solution, encoding="utf-8").decode("utf-8")

    return transformed_xml

def extract_keyword_from_url(url):
    try:
        # Parse the URL
        parsed_url = urlparse(url)

        # Get the query parameters
        query_params = parse_qs(parsed_url.query)

        # Extract the 'ut' parameter and decode it
        term_encoded = query_params.get('q', [''])[0]
        term_decoded = unquote(term_encoded)

        # Check if 'ut:' is present and extract the term after it
        if 'ut:' in term_decoded:
            term_after_ut = term_decoded.split('ut:')[1]
            return term_after_ut
        else:
            return None

    except Exception as e:
        print(f"Error extracting term from URL: {e}")
        return None

def delete_tripls():
    url = "http://localhost:9999/blazegraph/namespace/kb/sparql?update=DROP%20ALL"
    response = requests.post(url)
    print(response.status_code)
    print(response.text)
    
def load_tripls(file_path ="C:/Users/PC/Downloads/rdf_tripls_mini.rdf"):

    sparql_endpoint = "http://localhost:9999/blazegraph/namespace/kb/sparql"

    query = f'LOAD <file:{file_path}>'

    # Set the POST request parameters
    params = {'update': query}

    # Send the POST request
    response = requests.post(sparql_endpoint, params=params)

    # Check the response status
    if response.status_code == 200:
        print("RDF triples loaded successfully.")
    else:
        print(f"Error loading RDF triples. Status code: {response.status_code}")
        print(response.text)

def query_tripls(query):
    url = "http://localhost:9999/blazegraph/namespace/kb/sparql"

    params = {"query": query}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        #print("Request successful!")
        return response.text
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def get_query_coauthors(author_id):
    query = """
    PREFIX ns1: <https://zbmath.org/>
    SELECT DISTINCT ?coauthor
    WHERE {
    ?document ns1:author <https://zbmath.org/authors/?q=ai%3Azhu.yucan> .
    ?document ns1:author ?coauthor .
    FILTER (?coauthor != <https://zbmath.org/authors/?q=ai%3Azhu.yucan>)
    }
    """
    # Replace URLs in the query
    modified_query = query.replace(
        '<https://zbmath.org/authors/?q=ai%3Azhu.yucan>',
        f'<{author_id}>'
    )
    return modified_query

def get_query_intersections(classifications):

    filters = [
        f'?publication zb:classification ?cls{idx} .\n  FILTER(CONTAINS(STR(?cls{idx}), "{classification}"))'
        for idx, classification in enumerate(classifications, start=1)
    ]
    return f"""
    PREFIX zb: <https://zbmath.org/>
    SELECT DISTINCT ?publication
    WHERE {{
        {' '.join(filters)}
    }}
    """

def get_query_top_authors(key, beforeyear, afteryear):
    sparql_query = f"""
    PREFIX ns1: <https://zbmath.org/>

    SELECT ?author (COUNT(?document) AS ?numDocuments)
    WHERE {{
      ?document ns1:author ?author .
      ?document ns1:keyword "{key}" .
      ?document ns1:publicationYear ?publicationYear .
      FILTER (STR(?publicationYear) > "{afteryear}" && STR(?publicationYear) < "{beforeyear}")
    }}
    GROUP BY ?author
    ORDER BY DESC(?numDocuments) 
    LIMIT 10
    """
    return sparql_query

delete_tripls()

load_tripls(rdf_path)

# Parse the XML file
tree = ET.parse(xml_file_path)
root = tree.getroot()
xml = "<Solutions>\n"
# Iterate through each <Problem> element
for problem in root.findall('Problem'):
    problem_id = problem.get('id')
    problem_type = problem.get('type')
    print(problem_id,problem_type)
    if problem_type == 'coauthors':
        
        # Get the author URL from the <Author> element
        author_id = problem.find('Author').text

        sparql_query = get_query_coauthors(author_id)
         
        query_result = query_tripls(sparql_query)
        
        result_xml = transform_xml(query_result, sparql_query,problem_id,problem_type)
        xml = xml +result_xml + "\n"
        
    elif problem_type == 'msc-intersection':
        classifications = problem.findall('Classification')
        classifications = [classification.text for classification in classifications]
        sparql_query = get_query_intersections(classifications)
        print(sparql_query)
        query_result = query_tripls(sparql_query)
        print(query_result)
        result_xml = transform_xml(query_result, sparql_query,problem_id,problem_type)
        xml = xml +result_xml + "\n"
        
         
    elif problem_type == 'top-authors': 
        keyword = problem.find('Keyword').text
        keyword = extract_keyword_from_url(keyword)
        before_year = problem.find('BeforeYear').text
        after_year = problem.find('AfterYear').text
        sparql_query = get_query_top_authors(keyword, before_year, after_year)
        query_result = query_tripls(sparql_query)
        result_xml = transform_xml(query_result, sparql_query,problem_id,problem_type)  
        xml = xml +result_xml + "\n"      


xml = xml + "</Solutions>"
with open(solution_xml_path, "w", encoding="utf-8") as file:
        file.write(xml)




