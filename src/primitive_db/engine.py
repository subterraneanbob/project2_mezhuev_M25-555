import prompt


def welcome():
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    try:
        return prompt.string("Введите команду: ")
    except (KeyboardInterrupt, EOFError):
        return "exit"
