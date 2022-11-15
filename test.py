import os

# Function to prepend line to file:
# def line_prepender(filename, line):
#     """
#     filename [string]: file to be edited
#     line [string]: content to be added

#     need to filter by file type
#     only prepend to .cs and .h
#     """
#     # for file in os.listdir(path_to):

#         if file.endswith(".py") or file.endswith(".txt"):                               # Filter by file type

#             # with open(filename, "r+") as f:                                             # Open file and write text
#             with open(file, "r+") as f:
#                 content = f.read()
#                 f.seek(0, 0)
#                 f.write(line.rstrip("\r\n") + "\n" + content)


def get_config():
    lines = []
    options = []

    f = open("config.txt")
    # for word in f.read().split('\r'):
    #     # print(word)
    #     lines.append(word)
    lines = [word for word in f.read().split("\r")]

    for parameter in lines:
        # for word in parameter.split():
        #     options.append(word)
        options = [word for word in parameter.split()]

    for i in options:
        print(i)


# def get_files():
import os

files_arr = []
dir_arr = []
for root, dirs, files in os.walk("D:/repos/~test", topdown=False):
    for name in files:
        files_arr.append(os.path.join(root, name))
    for name in dirs:
        dir_arr.append(os.path.join(root, name))

print(files_arr)
print("------------")
print(dir_arr)


# for file in os.listdir(path_to):
for file in files_arr:
    if file.endswith(".py") or file.endswith(".txt"):  # Filter by file type

        # with open(filename, "r+") as f:                                             # Open file and write text
        with open(file, "r+") as f:
            content = f.read()
            f.seek(0, 0)
            # f.write(line.rstrip("\r\n") + "\n" + content)                           # line is content to write
            f.write("LICENSE#32039805948" + "\n" + content)


# get_config()


def write_license():
    files_arr = []
    for root, dirs, files in os.walk("D:/repos/~test", topdown=False):
        for name in files:
            files_arr.append(os.path.join(root, name))
    for file in files_arr:
        if file.endswith(".py") or file.endswith(".txt"):  # Filter by file type
            with open(file, "r+") as f:
                content = f.read()
                f.seek(0, 0)
                # f.write(line.rstrip("\r\n") + "\n" + content)                           # line is content to write
                f.write("LICENSE#32039805948" + "\n" + content)
