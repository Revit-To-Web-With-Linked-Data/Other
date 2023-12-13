import rdflib 
from pyshacl import validate

# Define the SHACL rules
shacl_rule = r'''
@prefix sh:      <http://www.w3.org/ns/shacl#> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex:      <https://ex/> .
@prefix fso:     <http://w3id.org/fso#> .
@prefix fpo:     <http://w3id.org/fpo#> .
@prefix xsd:      <http://www.w3.org/2001/XMLSchema#> .
@prefix inst:    <https://example.com/inst#> .

ex:PipePexSizing
	a sh:NodeShape ;
	sh:targetClass fpo:Pipe ;
	sh:rule [
		a sh:SPARQLRule ;
		sh:prefixes (fpo: fso: ex: );
		sh:construct """
			construct {?diameter fpo:value ex:chomologi .} 
WHERE {
  			?this a fpo:Pipe . 
  			?this fso:hasPort ?port .
    		?port fpo:outerDiameter ?diameter .
    		?diameter fpo:value ?diameterValue .
			BIND ( 
    IF(?diameterValue = 0.012, 0.015,
      IF(?diameterValue = 0.015, 0.018,
        IF(?diameterValue = 0.018, 0.020,
          IF(?diameterValue = 0.020, 0.022, 
            IF(?diameterValue = 0.022, 0.028,
              IF(?diameterValue = 0.028, 0.032,
                IF(?diameterValue = 0.032, 0.040,
                  IF(?diameterValue = 0.040, 0.050, ?diameterValue)
                )
              )
            )
          )
        ) 
      )
    )
    AS ?newSize
  )
  			} """ ;
	condition: ex:FictiveRule 

	] .
'''

# Define the data file and its format
data_file = 'Data-Model-Auto-Sizing.ttl'
data_format = 'turtle'

# Create and parse the data graph
data_graph = rdflib.Graph()
data_graph.parse(data=data_file, format=data_format)

# Create and parse the shapes graph from SHACL rules
shapes = rdflib.Graph()
shapes.parse(data=shacl_rule, format='turtle')

# Copy the original data graph for comparison after validation
data_graph_orig = rdflib.Graph()
for t in data_graph:
    data_graph_orig.add(t)

# Perform the validation
r = validate(data_graph,
             shacl_graph=shapes,
             data_graph_format=data_format,
             shacl_graph_format='turtle',
             advanced=True,
             debug=True)

conforms, results_graph, results_text = r

# Calculate and print the added triples
added_triples = data_graph - data_graph_orig
print('Added triples: ', len(added_triples))
print(added_triples.all_nodes())