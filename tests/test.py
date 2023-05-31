# import os

# # Function to prepend line to file:
# # def line_prepender(filename, line):
# #     """
# #     filename [string]: file to be edited
# #     line [string]: content to be added

# #     need to filter by file type
# #     only prepend to .cs and .h
# #     """
# #     # for file in os.listdir(path_to):

# #         if file.endswith(".py") or file.endswith(".txt"):                               # Filter by file type

# #             # with open(filename, "r+") as f:                                             # Open file and write text
# #             with open(file, "r+") as f:
# #                 content = f.read()
# #                 f.seek(0, 0)
# #                 f.write(line.rstrip("\r\n") + "\n" + content)


# def get_config():
#     lines = []
#     options = []
#     count = 0
#     repo_names = []
#     staging_spots = []
#     final_spots = []
#     f = open("config.txt")
#     lines = [word for word in f.read().split("\r")]

#     for line in lines:
#         options = [word for word in line.split()]

#     for option in options:
#         count += 1
#         if count == 1:
#             repo_names.append(option)
#         elif count == 2:
#             staging_spots.append(option)
#         elif count == 3:
#             final_spots.append(option)
#             count = 0

#     print("REPOS:")
#     print(repo_names)
#     print("STAGES:")
#     print(staging_spots)
#     print("FINALS:")
#     print(final_spots)


# def get_files():
#     files_arr = []
#     dir_arr = []
#     for root, dirs, files in os.walk("D:/repos/~test", topdown=False):
#         for name in files:
#             files_arr.append(os.path.join(root, name))
#         for name in dirs:
#             dir_arr.append(os.path.join(root, name))
#     for file in files_arr:
#         if file.endswith(".py") or file.endswith(".txt"):  # Filter by file type

#             # with open(filename, "r+") as f:                                             # Open file and write text
#             with open(file, "r+") as f:
#                 content = f.read()
#                 f.seek(0, 0)
#                 # f.write(line.rstrip("\r\n") + "\n" + content)                           # line is content to write
#                 f.write("LICENSE#32039805948" + "\n" + content)


# def write_license():
#     files_arr = []
#     for root, dirs, files in os.walk("D:/repos/~test", topdown=False):
#         for name in files:
#             files_arr.append(os.path.join(root, name))
#     for file in files_arr:
#         if file.endswith(".py") or file.endswith(".txt"):  # Filter by file type
#             with open(file, "r+") as f:
#                 content = f.read()
#                 f.seek(0, 0)
#                 # f.write(line.rstrip("\r\n") + "\n" + content)                           # line is content to write
#                 f.write("LICENSE#32039805948" + "\n" + content)


# get_config()
