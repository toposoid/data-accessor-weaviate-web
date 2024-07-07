def formatMessageForLogger(message:str, username:str) -> str:
    if message is None:
        return "\t" + username
    else:
        return message.replace("\n", "\\n").replace("\t", " ") + "\t" + username