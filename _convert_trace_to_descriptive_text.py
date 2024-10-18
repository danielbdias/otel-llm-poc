import json

def convert_node_data_to_text(node_data):
  description = [
    f"The node is named as '{node_data['name']}'",
    f"it has an id '{node_data['id']}'",
    f"it has a '{node_data['kind']}' kind",
    f"it has a duration of {node_data['attributes']['tracetest.span.duration']}",
  ]

  if 'parent_id' in node_data:
    description.append(f"it has a parent id '{node_data['parentId']}'")

  if 'tracetest.span.type' in node_data['attributes']:
    description.append(f"it has a '{node_data['attributes']['tracetest.span.type']}' span type")

  return ', '.join(description)

trace_data = None

# Load JSON file
with open('./trace.json', 'r') as file:
  trace_data = json.load(file)

flat_representation = trace_data["flat"]

with open('./trace-description.txt', 'w') as file:
  for node_id in flat_representation.keys():
    file.write(convert_node_data_to_text(flat_representation[node_id]))
    file.write('\n')
