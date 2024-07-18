from runtime import execution

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
        execution.execute(script)

if __name__ == '__main__':
    main()