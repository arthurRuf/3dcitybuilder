from subprocess import Popen, PIPE, STDOUT
import subprocess, sys


def execute_terminal_command(command):
    with open('test.log', 'w') as f:  # replace 'w' with 'wb' for Python 3
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        for c in iter(lambda: process.stdout.read(1), ''):  # replace '' with b'' for Python 3
            sys.stdout.write(c)
            f.write(c)

    # process = Popen(command.split(" "), shell=True, stdout=PIPE, stderr=STDOUT, stdin=PIPE)
    # # Poll process for new output until finished
    # while True:
    #     nextline = process.stdout.readline()
    #     if nextline == '' and process.poll() is not None:
    #         break
    # You can add here some progress infos
    #
    # output = process.communicate()[0]
    # exitCode = process.returncode
    #
    # if exitCode == 0:
    #     return output
    # else:
    #     raise Exception(command, exitCode, output)
