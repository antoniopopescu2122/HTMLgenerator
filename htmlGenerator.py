import json
import re
   
pattern = r"^[a-z0-9]{40}$"
# Read the JSON file
with open('data.json') as f:
    data = json.load(f)
#name, branch, revision, status, branch@revision
# Generate the HTML file
with open('output.html', 'w') as f:
    f.write('<html><head><style tr,td,th{border: 5px solid red}></style></head><body>')
    f.write('<table>')
    f.write('<tr style="background-color:lime;"> <td colspan="3" align="center"> <b> BINARY </b> </td> <td> </td> <td align="center"> <b> ECL </b> </td> </b> </tr>')
    f.write('<tr style="background-color:lime;" ><th>Name</th><th>Branch</th> <th>Revision</th> <th>Status</th> <th>branch@revision</th> </tr>')
    for component, details in data['BINARIES'].items():
        f.write('<tr>')
        f.write('<td style="text-transform:uppercase;">' + component + '</td>')
        f.write('<td>' + details['branch'] + '</td>')
        if re.match(pattern, details['revision']):
            f.write('<td> <a href="https://github.com/q/commit:' + details['revision'] + ' "target="_blank" >'+ details['revision'] + '</a> </td>')
        else:
            f.write('<td> ERR </td>')
        f.write('<td>' + 'Aligned' + '</td>')
        if re.match(pattern, details['revision']):
            f.write('<td> <a target="_blank" href="https://github.com/q/commit:' + details['revision'] + ' "> '+ details['branch'] +'@' + details['revision'] + '</a> </td>')
        else:
            f.write('<td> ERR </td>')
        f.write('</tr>')
    f.write('</table>')
    f.write('</head>')
    f.write('</body></html>')