import json
import xml.etree.ElementTree as ET

class XMLGenerator:
    def __init__(self, data_file):
        self.data_file = data_file

    def generate_xml(self, output_file):
        with open(self.data_file) as f:
            data = json.load(f)

        root = ET.Element('Components')

        for component, details in data['BINARIES'].items():
            component_elem = ET.SubElement(root, 'Component', name=component)
            branch_elem = ET.SubElement(component_elem, 'Branch')
            branch_elem.text = details['branch']
            revision_elem = ET.SubElement(component_elem, 'Revision')
            revision_elem.text = details['revision']

        tree = ET.ElementTree(root)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
