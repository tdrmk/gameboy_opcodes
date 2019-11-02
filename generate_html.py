import json
import os
filename = 'instructions.json'
output_filename = 'docs/index.html'

if not os.path.exists(filename):
    import scrap_instructions

with open(filename) as f:
    data = json.load(f)


title = 'Game Boy Instruction Set'
website = data['metadata']['website']

def generate_table(instructions, table_id):
    table_body = ""
    for i in range(16):
        table_row = f"<th> {i:X}x </th>"
        for j in range(16):
            opcode = f"0x{i:X}{j:X}"
            table_cell = ''
            bgcolor = '#FFFFFF'
            if opcode in instructions:
                instruction = instructions[opcode]
                table_cell = f"{instruction['instruction']} <br> " \
                             f"{instruction['length']}\t{instruction['duration']} <br>" \
                             f"{instruction['flags']['Z']} {instruction['flags']['N']} " \
                             f"{instruction['flags']['H']} {instruction['flags']['C']}"
                bgcolor = instruction['color']
            table_row += f"""<td bgcolor="{bgcolor}"> {table_cell} </td> """
        table_body += f"<tr> {table_row} </tr>\n"

    header = "<tr><th></th>" + " ".join(map(lambda x: f'<th>x{x:X}</th>', range(16))) + "</tr>\n"
    return f"<table id='{table_id}'> {header} {table_body} </table>"

instructions_table = generate_table(data['instructions'], table_id='instructions')
prefix_cb_table = generate_table(data['prefix-cb'], table_id='prefix_cb')

body = f"""
Adding fixes to instruction table at <a href={website}>{website}</a>.

<h1> Game boy Instruction Set (Z80) </h1>
{instructions_table}
<h1> Prefix CB Instructions </h1>
{prefix_cb_table}
<br>
"""
css = """
body {
    font-family: monospace;
    font-size: 8px;
}
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    text-align: center;
    width: 1350px;
}
th {
    width: 8em;
    background: #AAAAAA;
}
"""

html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
    {css}
    </style>
</head>
<body>
{body}
</body>
</html> 
"""

with open(output_filename, 'w') as f:
    f.write(html_template)
