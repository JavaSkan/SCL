import os
import sys
import threading as th
from runtime.execution import Executor

opening_message = """
--------------------------------------
Currently Using SCL Command Prompt
made by Javaskan at https://github.com/JavaSkan
All rights reserved©
--------------------------------------
"""

def main():
    if len(sys.argv) >= 2:
        if os.path.exists(sclpath := (sys.argv[1])):
            if not sclpath.endswith(".scl"):
                print(f"wrong extension, should end with '.scl'", file=sys.stderr)
            Executor().execute(f'exec "{sclpath}" true')
        else:
            print(f"{sclpath} doest not exist",file=sys.stderr)
    else:
        print(opening_message)
        while True:
            with Executor() as mainExecutor:
                script = input("?> ")
                exth = th.Thread(target=mainExecutor.execute,args=[script])
                exth.start()
                exth.join()

if __name__ == '__main__':
    main()