import env
import ulang

def main():
    env._ERR_QUIT = False
    script = ""
    while True:
        script = input("> ")
        ulang.execute(script)

if __name__ == '__main__':
    main()