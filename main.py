from os import environ

from discord import (Client, Intents, Message)
import discord


class Record:
    def __init__(self, myself: str = "", debtor: str = "", date: str = "", amount: int = 0, info: str = ""):
        self._myself: str = myself      # username
        self._debtor: str = debtor      # debtor who borrow money from you
        self._date: str = date          # the date that event happened
        self._amount: int = amount      # how much you lent him or her
        self._info: str = info          # the info of the item


class User:
    def __init__(self, myself: str = "", userID: str = ""):
        self._myself: str = myself             # username
        self._userID: str = userID             # user ID in discord
        # for all the debtors and the total money of each
        self._debtors: dict[str, int] = dict()
        self._records: list[Record] = list()   # store all the records

    def append_record(self, debtor: str, money: int, record: Record):
        if (debtor in self._debtors):
            self._debtors[debtor] += int(money)
        else:
            self._debtors[debtor] = int(money)

        self._records.append(record)


def setUpUser(name: str, ID: int, allUsers: list):  # set a new record for a user
    for i in range(len(allUsers)):
        if (allUsers[i]._myself == str(name)):
            return ("account is already existed")

    newUser: User = User(str(name), "<@"+str(ID)+">")
    send: str = newUser._userID + " is the new user, the whole name is "+newUser._myself
    allUsers.append(newUser)
    return send


def newRecord(command: str, ID: int, allUser: list):  # append a record for a certain user
    temp: list = command.split()
    new: Record = Record(
        "<@"+str(ID)+">", temp[1], temp[2], int(temp[3]), temp[4])
    send: str = new._date+"  $"+str(new._amount)+"  " + \
        new._info + "  " + new._debtor + " borrowed from " + new._myself

    for i in range(len(allUsers)):
        if (allUsers[i]._userID == new._myself):
            allUsers[i].append_record(new._debtor, new._amount, new)
            break

    return send


def modify(command: str, ID: int):  # modify the record
    temp = command.split()
    if (temp[1] == "-name"):
        ...
    elif (temp[1] == "-date"):
        ...
    elif (temp[1] == "sum"):
        ...
    elif (temp[1] == "info"):
        ...

    return ("modified successfully")


def remove():  # remove the record
    print("remove here")


def check(name: str, allUsers: list):  # print the debt data
    send = list()
    temp = User()

    for i in range(len(allUsers)):
        if (allUsers[i]._myself == name):
            temp: User = allUsers[i]

    if (len(temp._debtors) == 0):
        return ("there is no data")

    for key, value in temp._debtors.items():
        m: str = key+"  borrowed $"+str(value)+"  from you"
        send.append(m)

    return send


if __name__ == "__main__":
    allUsers = list()  # store all the UserData

    intents = Intents.default()
    intents.message_content = True

    client = Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    @client.event
    async def on_message(message: Message):

        # print(message)

        if (message.author == client.user):
            return

        args = message.content.split(" ")

        if (args[0] == "record"):
            await message.channel.send(newRecord(message.content, message.author.id, allUsers))
        # func(args[1:])

        if (message.content[:4] == "new"):
            await message.channel.send(setUpUser(str(message.author), message.author.id, allUsers))

        if (message.content[:6] == ("modify")):
            await message.channel.send(modify(message.content, message.author.id))

        if (message.content[:6] == ("remove")):
            await message.channel.send("on progressing function remove")

        if (message.content[:5] == ("check")):
            send = check(str(message.author), allUsers)

            for i in range(len(send)):
                await message.channel.send(send[i])

        # check if the data is stored
        # for item in range(len(allUsers)):
        #     await message.channel.send(allUsers[item]._myself)
        #     for r in range(len(allUsers[item]._records)):
        #         m = allUsers[item]._records[r]._debtor + " : " + allUsers[item]._records[
        #             r]._date + "  $" + allUsers[item]._records[r]._amount + "  " + allUsers[item]._records[r]._info
        #         await message.channel.send(m)
        #     await message.channel.send("--------------------------------")
        #     for r in range(len(allUsers[item]._debtors)):
        #         m = allUsers[item]._records[r]._debtor+" " + \
        #             str(allUsers[item]._debtors[allUsers[item]._records[r]._debtor])
        #         await message.channel.send(m)

    client.run(environ["TOKEN"])
