from easygui import fileopenbox,filesavebox

from utils import file_utils


training_data = file_utils.load_training_json()
vars = {}
with open("settings/can_db_template.dbc", 'r') as db_file:
    lines = []
    for line in db_file:
        lines.append(line)
        if line == 'BU_:\n':
            for name, data in training_data.items():
                str = 'EV_ vise_' + name + ': 0 [0|0] "" 0 1 DUMMY_NODE_VECTOR0 Vector__XXX;\n'
                lines.append(str)

with open("VISE_db.dbc", 'w') as db_file:
    db_file.writelines(lines)

dbc_file = filesavebox(msg='Select where to save VISE db', title='Save VISE db', default='VISE_db.dbc', filetypes='*.dbc')

if dbc_file is not None:
    with open(dbc_file, 'w') as db_file:
        db_file.writelines(lines)





