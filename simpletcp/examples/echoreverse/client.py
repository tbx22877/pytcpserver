from simpletcp.clientsocket import ClientSocket

s1 = ClientSocket("localhost", 5000)
response = s1.send("Hello, World!")

s2 = ClientSocket("localhost", 5000, single_use=False)
r1 = s2.send("Hello for the first time...")
r2 = s2.send("...and hello for the last!")
s2.close()

# Display the correspondence
print("s1 sent\t\tHello, World!")
print("s1 received\t\t{}".format(response.decode("UTF-8")))
print("-------------------------------------------------")
print("s2 sent\t\tHello for the first time....")
print("s2 received\t\t{}".format(r1.decode("UTF-8")))
print("s2 sent\t\t...and hello for the last!.")
print("s2 received\t\t{}".format(r2.decode("UTF-8")))
