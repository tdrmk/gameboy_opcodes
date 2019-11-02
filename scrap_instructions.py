import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.pastraiser.com/cpu/gameboy/gameboy_opcodes.html'
r = requests.get(url)
html_page = r.text

soup = BeautifulSoup(html_page, 'html.parser')
instr_table, prefix_cb_table, _, instr_type_table, *_ = soup.findAll('table')
color_desc_map = {}
for tr in instr_type_table.findAll('tr'):
    tds = tr.findAll('td')
    color = tds[0]['bgcolor']
    desc = tds[2].string
    color_desc_map[color] = desc

def parse(table):
    instructions = {}
    for row_index, tr in enumerate(table.findAll('tr')[1:]):
        for col_index, td in enumerate(tr.findAll('td')[1:]):
            descendants = list(td.descendants)

            if len(descendants) > 1: # Then instruction
                instr = descendants[0]
                operator, *operands = instr.split()
                length, duration = descendants[2].string.split()
                # if '/' in duration:
                #     duration = max(map(int, duration.split('/')))
                length = int(length)
                z, n, h, c = descendants[4].string.split()
                flags = {'Z': z, 'N': n, 'H': h, 'C': c}
                opcode = f'0x{row_index:X}{col_index:X}'
                desc = color_desc_map[td['bgcolor']]

                instructions[opcode] =  {
                    'opcode': opcode,
                    'instruction': instr,
                    'operator': operator,
                    'length': length,
                    'duration': duration,
                    'flags': flags,
                    'color': td['bgcolor'],
                }
                if operands:
                    instructions[opcode]['operands'] = operands[0].split(',')

                if '8bit' in desc:
                    instructions[opcode]['type'] = '8-bit'
                elif '16bit' in desc:
                    instructions[opcode]['type'] = '16-bit'

    return instructions

root_instructions = parse(instr_table)


# FIXES
root_instructions['0xE2']['length'] = 1
root_instructions['0xF2']['length'] = 1
root_instructions['0xE9']['instruction'] = 'JP HL'
root_instructions['0xE9']['operands'][0] = 'HL'
root_instructions['0xCB']['length'] = 2
root_instructions['0xCB']['duration'] = "8"


prefix_instructions = parse(prefix_cb_table)

prefix_instructions['0x28']['flags']['C'] = 'C'
prefix_instructions['0x29']['flags']['C'] = 'C'
prefix_instructions['0x2A']['flags']['C'] = 'C'
prefix_instructions['0x2B']['flags']['C'] = 'C'
prefix_instructions['0x2C']['flags']['C'] = 'C'
prefix_instructions['0x2D']['flags']['C'] = 'C'
prefix_instructions['0x2E']['flags']['C'] = 'C'
prefix_instructions['0x2F']['flags']['C'] = 'C'


all_instructions = {
    'metadata': {
        'website': url,
    },
    'instructions': root_instructions,
    'prefix-cb': prefix_instructions,
    'color-description': color_desc_map,
}

with open('instructions.json', 'w') as f:
    f.write(json.dumps(all_instructions, indent=4))