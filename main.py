from runtime import execution
import threading as th
opening_message = """
--------------------------------------
Currently Using SCL Command Prompt
made by Javaskan at https://github.com/JavaSkan
All rights reserved©
--------------------------------------
"""

def main():
    print(opening_message)
    script = ""
    while True:
        script = input("> ")
        exth = th.Thread(target=execution.execute,args=[script])
        exth.start()
        exth.join()

if __name__ == '__main__':
    main()