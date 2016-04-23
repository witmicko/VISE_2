import win32com.client

from utils import file_utils


class ComComms:
    def __init__(self):
        App = win32com.client.Dispatch('CANoe.Application')
        training_data = file_utils.load_training_json()
        self.vars = {}
        for name, data in training_data.items():
            self.vars[name] = App.Environment.GetVariable('vise_' + name)
        print()

    def set_env_var(self, name, value):
        self.vars[name].value = value


if __name__ == "__main__":
    cc = ComComms()
    cc.set_env_var('SPEED',89)