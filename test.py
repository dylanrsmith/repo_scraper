# def line_prepender(filename, line):
#     """
#     filename [string]: file to be edited
#     line [string]: content to be added
#     """
#     with open(filename, "r+") as f:
#         content = f.read()
#         f.seek(0, 0)
#         f.write(line.rstrip("\r\n") + "\n" + content)

def get_config():
    lines = []
    options = []

    f = open('config.txt')
    # for word in f.read().split('\r'):
    #     # print(word)
    #     lines.append(word)
    lines = [word for word in f.read().split('\r')]
        
    for parameter in lines:
        # for word in parameter.split():
        #     options.append(word)
        options = [word for word in parameter.split()]

    for i in options:
        print(i)

get_config()