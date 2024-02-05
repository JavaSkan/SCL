from runtime import execution

def main():
    script = ""
    while True:
        script = input("> ")
        execution.execute(script)

if __name__ == '__main__':
    main()