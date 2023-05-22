import json

# Read the current data
with open('data.json') as file:
    current_data = json.load(file)

try:
    # Read the previous data if it exists
    with open('previous_data.json') as file:
        previous_data = json.load(file)
except FileNotFoundError:
    # If previous_data.json doesn't exist, consider all components as new additions
    previous_data = {}

# Compare the current and previous data to track modifications
modifications = {}
for component, current_component_data in current_data['BINARIES'].items():
    if component in previous_data:
        previous_component_data = previous_data[component]
        modified_fields = {}
        for field, current_value in current_component_data.items():
            previous_value = previous_component_data.get(field)
            if current_value != previous_value:
                modified_fields[field] = {
                    'previous_value': previous_value,
                    'current_value': current_value
                }
        if modified_fields:
            modifications[component] = {
                'type': 'modified',
                'details': modified_fields
            }
    else:
        modifications[component] = {
            'type': 'added',
            'details': current_component_data
        }

# Check for deleted components
for component in previous_data:
    if component not in current_data['BINARIES']:
        modifications[component] = {'type': 'deleted'}

# Save the current data as the previous data for future comparisons
with open('previous_data.json', 'w') as file:
    json.dump(current_data['BINARIES'], file)

# Generate HTML to display the modifications
html = '<html><head>'
html += '<style>'
html += 'ul { list-style-type: none; padding-left: 0; }'
html += 'li { margin-bottom: 20px; }'
html += 'h1 { font-size: 24px; }'
html += '.added { background-color: #d4f5d4; }'
html += '.deleted { background-color: #f5d4d4; }'
html += '.modified { background-color: #ffe6b3; }'
html += '.field { font-weight: bold; }'
html += '</style>'
html += '</head><body>'
html += '<h1>Modifications</h1>'
if modifications:
    html += '<ul>'
    for component, modification in modifications.items():
        modification_type = modification['type']
        html += f'<li class="{modification_type}"><strong>{component}</strong>: '
        if modification_type == 'added':
            html += f'Added Component: {modification["details"]}'
        elif modification_type == 'deleted':
            html += 'Deleted Component'
        elif modification_type == 'modified':
            html += 'Modified Fields:<ul>'
            for field, details in modification['details'].items():
                previous_value = details['previous_value']
                current_value = details['current_value']
                html += f'<li><span class="field">{field}:</span> <span>{previous_value} -> {current_value}</span></li>'
            html += '</ul>'
        html += '</li>'
    html += '</ul>'
else:
    html += '<p>No modifications</p>'
html += '</body></html>'

# Save the HTML file
with open('modifications.html', 'w') as file:
    file.write(html)
