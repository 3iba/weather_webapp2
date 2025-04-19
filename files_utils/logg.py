def log_message(message):
    with open("log.txt", "a", encoding="utf-8") as log:
        log.write(message + "\n")
        