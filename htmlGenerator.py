import json
import re
from xmlgenerator import XMLGenerator


class HTMLGenerator:
    def __init__(self, data_file):
        self.data_file = data_file
        self.pattern = r"^[a-z0-9]{40}$"

    def read_json(self):
        with open(self.data_file) as f:
            self.data = json.load(f)

    def generate_html(self, output_file):
        # Read the previous data if it exists
        try:
            with open('previous_data.json') as file:
                previous_data = json.load(file)
        except FileNotFoundError:
            # If previous_data.json doesn't exist, consider all components as new additions
            previous_data = {}

        # Compare the current and previous data to track modifications
        modifications = {}
        for component, current_component_data in self.data['BINARIES'].items():
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
            if component not in self.data['BINARIES']:
                modifications[component] = {'type': 'deleted'}

        # Save the current data as the previous data for future comparisons
        with open('previous_data.json', 'w') as file:
            json.dump(self.data['BINARIES'], file)

        # Generate HTML to display the modifications
        html = '<html><body>'
        html += '<h1>Modifications</h1>'
        if modifications:
            html += '<ul>'
            for component, modification in modifications.items():
                modification_type = modification['type']
                html += f'<li><strong>{component}</strong>: '
                if modification_type == 'added':
                    html += f'Added Component: {modification["details"]}'
                elif modification_type == 'deleted':
                    html += 'Deleted Component'
                elif modification_type == 'modified':
                    html += 'Modified Fields:<ul>'
                    for field, details in modification['details'].items():
                        previous_value = details['previous_value']
                        current_value = details['current_value']
                        html += f'<li>{field}: {previous_value} -> {current_value}</li>'
                    html += '</ul>'
                html += '</li>'
            html += '</ul>'
        else:
            html += '<p>No modifications</p>'
        html += '</body></html>'

        # Save the HTML file
        with open(output_file, 'w') as file:
            file.write('<html><head>')
            file.write('<link rel="stylesheet" type="text/css" href="style.css">')
            file.write('</head><body>')
            file.write('<table>')
            file.write(
                '<tr style="background-color:lime;"><td colspan="3" align="center"><b>BINARY</b></td><td></td><td align="center"><b>ECL</b></td></tr>')
            file.write(
                '<tr style="background-color:lime;"><th>Name</th><th>Branch</th><th>Revision</th><th>Status</th><th>branch@revision</th></tr>')
            for component, details in self.data['BINARIES'].items():

                if re.match(self.pattern, details['revision']):
                    file.write('<tr>')
                    file.write('<td style="text-transform:uppercase;">' + component + '</td>')
                    file.write('<td>' + details['branch'] + '</td>')
                    file.write('<td><a href="https://github.com/q/commit:' + details['revision'] + '" target="_blank">' +
                            details['revision'] + '</a></td>')
                    file.write('<td>Aligned</td>')
                else:
                    print("component "+component+" doesn't match the format.")

                if re.match(self.pattern, details['revision']):
                    file.write('<td><a target="_blank" href="https://github.com/q/commit:' + details['revision'] + '"> ' +
                            details['branch'] + '@' + details['revision'] + '</a></td>')

                file.write('</tr>')
            file.write('</table>')
            file.write(html)
            file.write('</body></html>')

    def add_entry_to_json(self, component, branch, revision):
        # Read the existing JSON data
        with open(self.data_file) as f:
            data = json.load(f)

        # Add the new entry
        data['BINARIES'][component] = {
            'details': {'ECL_revision': '37547155c9a34cd16f6992c05f110154bdcbab92', 'ECL_branch': 'master'},
            'repository': 'MN/OAM/' + component,
            'branch': branch,
            'revision': revision,
            'artifactory_url_component_specific': 'https://artifactory.com/artifactory/components/component1/master/' + revision
        }

        # Save the modifications to the JSON file
        with open(self.data_file, 'w') as f:
            json.dump(data, f)


# Example usage with user interface
data_file = 'data.json'
output_file = 'output.html'

html_generator = HTMLGenerator(data_file)
html_generator.read_json()
html_generator.generate_html(output_file)

# User interface for adding new entry
if input("Do you want to add a new entry? (Y/N): ").lower() == 'y':
    print("Add New Entry")
    component = input("Component Name: ")
    branch = input("Branch: ")
    revision = input("Revision: ")
    html_generator.add_entry_to_json(component, branch, revision)
    html_generator.generate_html(output_file)


xml_generator = XMLGenerator()
xml_generator.generate_xml(html_generator.data, "output.xml")
