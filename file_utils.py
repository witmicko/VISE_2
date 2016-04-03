import json


def load_training_json():
    with open("training.json") as json_file:
        data = json.load(json_file)
    # json doesnt support tuples so need to convert 4 points into a tuple of tuples
    for name, d_ in data.items():
        roi = d_['roi']
        a = tuple(roi[0])
        b = tuple(roi[1])
        c = tuple(roi[2])
        d = tuple(roi[3])
        d_['roi'] = [a, b, c, d]
    return data


def save_training_json(data):
    with open('training.json', 'w') as outfile:
        json.dump(obj=data,
                  fp=outfile,
                  sort_keys=True,
                  indent=4,
                  separators=(',', ":")
                  )
