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
        with open(output_file, 'w') as f:
            f.write('<html><head>')
            f.write('<link rel="stylesheet" type="text/css" href="style.css">')
            f.write('</head><body>')
            f.write('<table>')
            f.write(
                '<tr style="background-color:lime;"><td colspan="3" align="center"><b>BINARY</b></td><td></td><td align="center"><b>ECL</b></td></tr>')
            f.write(
                '<tr style="background-color:lime;"><th>Name</th><th>Branch</th><th>Revision</th><th>Status</th><th>branch@revision</th></tr>')
            for component, details in self.data['BINARIES'].items():
                f.write('<tr>')
                f.write('<td style="text-transform:uppercase;">' + component + '</td>')
                f.write('<td>' + details['branch'] + '</td>')
                if re.match(self.pattern, details['revision']):
                    f.write('<td><a href="https://github.com/q/commit:' + details['revision'] + '" target="_blank">' +
                            details['revision'] + '</a></td>')
                else:
                    f.write('<td>ERR</td>')
                f.write('<td>Aligned</td>')
                if re.match(self.pattern, details['revision']):
                    f.write('<td><a target="_blank" href="https://github.com/q/commit:' + details['revision'] + '"> ' +
                            details['branch'] + '@' + details['revision'] + '</a></td>')
                else:
                    f.write('<td>ERR</td>')
                f.write('</tr>')
            f.write('</table>')
            f.write('</body></html>')

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
    html_generator.generate_html(output_file)


xml_generator = XMLGenerator()
xml_generator.generate_xml(html_generator.data, "output.xml")
