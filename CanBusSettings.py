from easygui import *
from canlib import canlib_xl
from utils.file_utils import load_can_bus_json, save_can_bus_json, load_training_json

if __name__ == "__main__":
    settings = load_can_bus_json()
    # Device select
    msg = "Which device is used to communicate with CAN bus?"
    title = "Device"
    choices = sorted(canlib_xl.devices.keys())
    preselect = 0
    if 'device' in settings:
        preselect = choices.index(settings['device'])
    device_choice = choicebox(msg, title, choices, preselect=preselect)


    # Baud rate select
    msg = "Select baud rate to be used."
    title = "Baud rate"
    choices = ["125 kbps", "250 kbps", "500 kbps", "1000 kbps"]

    from easygui import choicebox, integerbox, multenterbox

    preselect = 2
    if 'baud_rate' in settings:
        preselect = choices.index(str(settings['baud_rate']) + ' kbps')
    baud_rate_choice = choicebox(msg, title, choices, preselect=preselect)

    # search for lower ID and set it as start_id
    start_id = -1
    trained_messages = None
    if 'messages' in settings:
        trained_messages = settings['messages']
        start_id = 2049
        for name, data in trained_messages.items():
            start_id = data['id'] if data['id'] <= start_id else start_id

    # get user input otherwise
    if start_id == -1:
        msg = "Type in start ID for VISE messages"
        title = "Start ID"
        start_id = integerbox(msg="enter value", title=title, lowerbound=1, upperbound=2048)

    # get all trained data
    training_data = load_training_json()
    msg = "Enter IDs for tested fields"
    title = "VISE IDs"
    fieldNames = sorted(training_data.keys())
    fieldValues = []  # we start with blanks for the values
    for i in range(len(fieldNames)):
        if trained_messages is not None:
            xx = int(trained_messages[fieldNames[i]]['id'])
            fieldValues.append(xx)
            print()
        else:
            fieldValues.append(start_id + i)

    fieldValues = multenterbox(msg, title, fieldNames, values=fieldValues)
    # make sure that none of the fields was left blank or repeat
    while True:
        if fieldValues is None:
            break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg += '"%s" is a required field.\n\n' % fieldNames[i]
            elif fieldValues.count(fieldValues[i]) > 1:
                errmsg += '"%s" IDs must be unique.\n\n' % fieldNames[i]
        if errmsg == "":
            break  # no problems found
        fieldValues = multenterbox(errmsg, title, fieldNames, values=fieldValues)

    messages = {}
    for i in range(len(fieldNames)):
        dlc = 1 if training_data[fieldNames[i]]['type'] == 'LED' else 2
        messages[fieldNames[i]] = {
            'id': int(fieldValues[i]),
            'dlc': dlc
        }

    settings['device'] = device_choice
    settings['baud_rate'] = int(baud_rate_choice.split(' ')[0])
    settings['messages'] = messages
    save_can_bus_json(settings)
