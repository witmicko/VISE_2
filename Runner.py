import os

from easygui import buttonbox

choices = ('Camera Settings',
           'Training Mode',
           'CAN bus settings',
           'CANdb generator',
           'Working Mode')


while True:
    choice = buttonbox(msg='Select mode:', title='VISE', choices=choices,
                       image='gui/VISE_logo.png',
                       default_choice=None,
                       cancel_choice=None)

    if choice is None:
        break
        
    if choice == 'Camera Settings':
        os.system("CameraSettings.py")

    elif choice == 'Training Mode':
        os.system("Training.py")

    elif choice == 'CAN bus settings':
        os.system("CanBusSettings.py")

    elif choice == 'CANdb generator':
        os.system("CANdbBuilder.py")

    elif choice == 'Working Mode':
        os.system("ClusterReader.py")

