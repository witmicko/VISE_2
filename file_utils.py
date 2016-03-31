import json


def load_training_json():
    with open("training.json") as json_file:
        data = json.load(json_file)
    return data


def save_training_json(data):
    with open('training.json', 'w') as outfile:
        json.dump(obj=data,
                  fp=outfile,
                  sort_keys=True,
                  indent=4,
                  separators=(',', ': '))
