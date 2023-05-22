import xml.etree.ElementTree as ET
import json
import xml.dom.minidom

class XMLGenerator:
    def generate_xml(self, data, output_file):
        root = ET.Element("root")
        binaries = ET.SubElement(root, "BINARIES")

        for component, details in data['BINARIES'].items():
            binary = ET.SubElement(binaries, "binary")
            binary.set("name", component)

            branch = ET.SubElement(binary, "branch")
            branch.text = details['branch']

            revision = ET.SubElement(binary, "revision")
            revision.text = details['revision']

        xml_string = ET.tostring(root, encoding="utf-8")
        xml_dom = xml.dom.minidom.parseString(xml_string)
        formatted_xml = xml_dom.toprettyxml(indent="  ")

        with open(output_file, "w") as f:
            f.write(formatted_xml)
