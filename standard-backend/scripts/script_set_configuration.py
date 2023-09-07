import os
import sys

os.chdir('..')

def change_configuration(argv):
    accepted_configurations = {'LOCAL', 'LOCAL-AWS', 'AWS'}
    if argv:
        configuration = argv[0]
        with open("src/common/configuration.py", "r") as fi:
            lines = fi.readlines()
        fi.close()
        if configuration in accepted_configurations:
            lines[0] = 'CURRENT_ENV = \"' + configuration + '\"\n'
            with open("src/common/configuration.py", "w") as fo:
                fo.writelines(lines)
            fo.close()
            return

    exit_flag = False
    while not exit_flag:
        configuration = input('Configuration: ')
        if configuration in accepted_configurations:
            with open("src/common/configuration.py", "r") as fi:
                lines = fi.readlines()
            fi.close()
            lines[0] = 'CURRENT_ENV = \"' + configuration + '\"\n'
            with open("src/common/configuration.py", "w") as fo:
                fo.writelines(lines)
            fo.close()
            exit_flag = True


change_configuration(sys.argv[1:])
