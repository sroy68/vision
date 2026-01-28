import os

user = input("name: ")
query = "SELECT * FROM users WHERE name = '" + user + "'"
os.system("ping " + user)
