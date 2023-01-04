"""
The goal of Mahjong is to replace the tiles in your hand until they follow a winning pattern.
A winning hand must contain at least one 2-repetition. The rest must be a set of 3-orderings or 3-repetitions, or a set
of 2-repetitions.
A 3-ordering (shun) is 3 tiles of the same type in consecutive order by value.
A 3-repetition (ke) is 3 tiles of the same type and value.
A 2-repetition (dui) is 2 tiles of the same type and value.

Tile replacement is achieved by eliminating a tile from your hand and either drawing one from the pile or catching the
opponent's eliminated tile.
There are two ways of catching the opponent's tiles: by Chi or by Peng. Catching by Gang is not implemented here because
there are only two players.
Catching by Chi is possible when the tile caught forms a 3-ordering with two tiles in your hand.
Catching by Peng is possible when the tile caught forms a 3-repetition with two tiles in your hand.
"""

import random
from tkinter import *
from tkinter.messagebox import *


class Tile(Button):
    def __init__(self, type, val, image, master):
        Button.__init__(self, master)

        self.type = type
        self.val = val

        self.face = False

        self.x = None
        self.y = None

        self.img = image
        self.id = self.type * 10 + self.val

        self.index = None

        self["width"] = 43
        self["height"] = 64

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __le__(self, other):
        return self.id <= other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def setIndex(self, n):
        self.index = n

    def getIndex(self):
        return self.index

    def getType(self):
        return self.type

    def getVal(self):
        return self.val

    def setFace(self, face):
        if face:
            self.face = True
            self["image"] = self.img
        else:
            self.face = False
            self["image"] = PhotoImage(file="./res/back.png")

    def moveTo(self, x1, y1):
        self.place(x=x1, y=y1)
        self.x = x1
        self.y = y1

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getID(self):
        return self.id


class WinningHand:
    def __init__(self):
        self.types = [
            [6, 1, 4, 1, 0, 0, 0, 0, 0, 0],
            [3, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [5, 2, 3, 0, 0, 0, 0, 0, 0, 0]
        ]

        '''
        if self.isWinning(self.types):
            print("Win!")
        else:
            print("Not Win!")
        '''


window = Tk()
window.title("两人麻将")
window.geometry("1360x600")

allTiles = []

playerHand = []
playerOut = []
cpuHand = []
cpuOut = []

playerHandY = 500 - 32
playerOutY = playerHandY - 96

cpuHandY = 50 - 32
cpuOutY = cpuHandY + 96

lastTile = None
currentTile = None

playerTurn = True


def CanPeng(hand, tile):
    n = 0
    for i in range(0, len(hand)):
        t = hand[i]
        if t == tile:
            n += 1

    if n >= 2:
        return True

    return False


def CanChi(hand, tile):
    if tile.getType == 4:
        return False

    for i in range(0, len(hand) - 1):
        t1 = hand[i]
        t2 = hand[i + 1]
        if (t1.getVal() == tile.getVal() + 1) and (t1.getType() == tile.getType()) and (
                t2.getVal() == tile.getVal() + 2) and (t2.getType() == tile.getType()):
            return True

    for i in range(0, len(hand) - 1):
        t1 = hand[i]
        t2 = hand[i + 1]
        if (t1.getVal() == tile.getVal() - 1) and (t1.getType() == tile.getType()) and (
                t2.getVal() == tile.getVal() + 1) and (t2.getType() == tile.getType()):
            return True

    for i in range(0, len(hand) - 1):
        t1 = hand[i]
        t2 = hand[i + 1]
        if (t1.getVal() == tile.getVal() - 2) and (t1.getType() == tile.getType()) and (
                t2.getVal() == tile.getVal() - 1) and (t2.getType() == tile.getType()):
            return True

    return False


def CPUSelect(hand):
    types = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    for i in range(0, len(hand)):
        tile = hand[i]

        if (tile.id > 10) and (tile.id < 20):
            types[0][0] += 1
            types[0][tile.id - 10] += 1
        if (tile.id > 20) and (tile.id < 30):
            types[1][0] += 1
            types[1][tile.id - 20] += 1
        if (tile.id > 30) and (tile.id < 40):
            types[2][0] += 1
            types[2][tile.id - 30] += 1
        if (tile.id > 40) and (tile.id < 50):
            types[3][0] += 1
            types[3][tile.id - 40] += 1

    # Choose a singular Zi type tile if possible.
    for j in range(1, 10):
        if types[3][j] == 1:
            t = CPUSelectHelper(hand, 4, j)
            return t

    # Mask the repetitions/orderings
    for i in range(0, 3):
        for j in range(1, 10):
            if types[i][j] >= 3:
                types[i][j] -= 3

            if (j <= 7) and (types[i][j] >= 1) and (types[i][j + 1] >= 1) and (types[i][j + 2] >= 1):
                types[i][j] -= 1
                types[i][j + 1] -= 1
                types[i][j + 2] -= 1

    # Choose remaining singular tile
    for i in range(0, 3):
        for j in range(1, 10):
            if types[i][j] == 1:
                t = CPUSelectHelper(hand, i + 1, j)
                return t

    # Choose one from a 2-repetition
    for i in range(3, -1):
        for j in range(1, 10):
            if types[i][j] == 2:
                t = CPUSelectHelper(hand, i + 1, j)
                return t

    # If no pattern can be maintained, choose at random
    t = random.randint(0, 13)
    return t


def CPUSelectHelper(hand, type, val):
    for i in range(0, len(hand)):
        tile = hand[i]
        if (tile.getType() == type) and (tile.getVal() == val):
            return i
    return -1


def OnButtonDrawClick():
    global playerTurn, playerHand

    tile = allTiles.pop(0)
    tile.setFace(True)
    tile.bind("<ButtonPress>", OnTileClick)

    playerHand.append(tile)

    SortHands()
    SortOut()

    result = AnalyzeHand(playerHand)
    if result:
        buttonWin["state"] = NORMAL
        return

    buttonEliminate["state"] = NORMAL
    buttonChi["state"] = DISABLED
    buttonPeng["state"] = DISABLED
    buttonDraw["state"] = DISABLED

    playerTurn = True


def OnButtonEliminateClick():
    global playerTurn, lastTile, currentTile, playerHand, playerOut

    if (currentTile is None) or (not playerTurn):
        return

    tile = playerHand.pop(currentTile.getIndex())
    SortHands()

    playerOut.append(tile)
    SortOut()

    buttonEliminate["state"] = DISABLED
    lastTile = None
    currentTile = None
    playerTurn = False

    CPUTurn()
    NextTurn()


def OnButtonCatchClick():
    global playerTurn, cpuOut, playerHand

    tile = cpuOut.pop()
    playerHand.append(tile)

    SortHands()
    SortOut()

    result = AnalyzeHand(playerHand)
    if result:
        buttonWin["state"] = NORMAL
        return

    buttonEliminate["state"] = NORMAL
    buttonDraw["state"] = DISABLED
    buttonChi["state"] = DISABLED
    buttonPeng["state"] = DISABLED

    playerTurn = True


def OnButtonWinClick():
    buttonChi["state"] = DISABLED
    buttonPeng["state"] = DISABLED
    buttonDraw["state"] = DISABLED
    buttonEliminate["state"] = DISABLED

    RevealHands()
    showinfo(message="玩家Win!")



def RevealHands():
    for tile in playerHand:
        tile.setFace(True)

    for tile in cpuHand:
        tile.setFace(True)



def CPUTurn():
    global playerTurn, cpuHand, cpuOut

    tile = allTiles.pop(0)
    cpuHand.append(tile)
    SortHands()

    result = AnalyzeHand(cpuHand)
    if result:
        '''
        buttonChi["state"] = DISABLED
        buttonPeng["state"] = DISABLED
        buttonDraw["state"] = DISABLED
        buttonEliminate["state"] = DISABLED
        '''

        RevealHands()
        showinfo(message="对手Win!")
        return

    i = CPUSelect(cpuHand)

    tile = cpuHand.pop(i)
    SortHands()

    cpuOut.append(tile)
    SortOut()

    playerTurn = True


def NextTurn():
    global playerTurn

    playerTurn = True
    buttonDraw["state"] = NORMAL

    if len(cpuOut) > 0:
        tile = cpuOut[len(cpuOut) - 1]
        canPeng = CanPeng(playerHand, tile)
        canChi = CanChi(playerHand, tile)

        if canPeng:
            buttonPeng["state"] = NORMAL
        if canChi:
            buttonChi["state"] = NORMAL

        if not (canPeng or canChi):
            buttonPeng["state"] = DISABLED
            buttonChi["state"] = DISABLED


buttonDraw = Button(window, text="摸牌", command=OnButtonDrawClick)
buttonEliminate = Button(window, text="出牌", command=OnButtonEliminateClick)
buttonPeng = Button(window, text="碰牌", command=OnButtonCatchClick)
buttonChi = Button(window, text="吃牌", command=OnButtonCatchClick)
buttonWin = Button(window, text="胡牌", command=OnButtonWinClick)

buttonDraw.place(x=600, y=545, width=50, height=50)
buttonEliminate.place(x=525, y=545, width=50, height=50)
buttonPeng.place(x=450, y=545, width=50, height=50)
buttonChi.place(x=375, y=545, width=50, height=50)
buttonWin.place(x=700, y=545, width=50, height=50)


def OnTileClick(event):
    global lastTile, currentTile

    if (event.widget["state"] == DISABLED) or (not event.widget.face):
        return

    tile = event.widget
    tile.moveTo(tile.getX(), tile.getY() - 32)

    currentTile = tile
    if lastTile is None:
        lastTile = tile
    else:
        lastTile.moveTo(lastTile.getX(), lastTile.getY() + 32)
        lastTile = tile


def StartGame():
    global playerTurn
    playerTurn = True

    LoadTiles()
    random.shuffle(allTiles)

    ResetGame()


def LoadTiles():
    for type in range(1, 4):
        for val in range(1, 10):
            faceImg = ""

            if type == 1:
                faceImg = "res/nan/1"
            if type == 2:
                faceImg = "res/nan/2"
            if type == 3:
                faceImg = "res/nan/3"

            faceImg = faceImg + str(val) + ".png"

            for _ in range(1, 5):
                tile = Tile(type, val, PhotoImage(file=faceImg), window)
                allTiles.append(tile)

    for val in range(1, 8):
        faceImg = "res/nan/4" + str(val) + ".png"

        for _ in range(1, 5):
            tile = Tile(4, val, PhotoImage(file=faceImg), window)
            allTiles.append(tile)


def ResetGame():
    global playerHand, cpuHand, playerOut, cpuOut
    playerHand = []
    playerOut = []
    cpuHand = []
    cpuOut = []

    Distribute()

    '''
    for i in range(0, len(allTiles)):
        tile = allTiles[i]

        x = 34 + (i % 13) * 50
        y = 132 + (i - i % 13) / 13 * 16
        tile.moveTo(x, y)
        tile.setFace(False)
    '''


def Distribute():
    global playerHand, cpuHand
    for i in range(0, 26):
        if i % 2 == 0:
            tile = allTiles.pop(0)
            playerHand.append(tile)
        else:
            cpuHand.append(allTiles.pop(0))

    SortHands()


def SortHands():
    global playerHand, cpuHand
    playerHand.sort()
    cpuHand.sort()

    for i in range(0, len(playerHand)):
        tile = playerHand[i]

        tile.setIndex(i)
        tile.setFace(True)
        tile.moveTo(34 + i * 50, playerHandY)
        tile.bind("<ButtonPress>", OnTileClick)

    for i in range(0, len(cpuHand)):
        tile = cpuHand[i]

        tile.setIndex(i)
        tile.setFace(False)
        tile.moveTo(34 + i * 50, cpuHandY)


def SortOut():
    global playerOut, cpuOut

    for i in range(0, len(playerOut)):
        tile = playerOut[i]

        tile.setIndex(i)
        tile.setFace(True)
        tile.moveTo(34 + (i % 20) * 50, playerOutY - (i - i % 20) / 20 * 86)
        tile.unbind("<ButtonPress>")

    for i in range(0, len(cpuOut)):
        tile = cpuOut[i]

        tile.setIndex(i)
        tile.setFace(True)
        tile.moveTo(34 + (i % 20) * 50, cpuOutY + (i - i % 20) / 20 * 86)


def Check(type, isZi):
    if type[0] == 0:
        return True

    n = 0
    for j in range(1, len(type)):
        n = j
        if type[j] != 0:
            break

    if type[n] >= 3:
        type[n] -= 3
        type[0] -= 3
        result = Check(type, isZi)
        type[n] += 3
        type[0] += 3

        return result

    if (not isZi) and (n < 8) and (type[n + 1] > 0) and (type[n + 2] > 0):
        type[n] -= 1
        type[n + 1] -= 1
        type[n + 2] -= 1
        type[0] -= 3
        result = Check(type, isZi)
        type[n] += 1
        type[n + 1] += 1
        type[n + 2] += 1
        type[0] += 3

        return result

    return False


def IsWinning(ls):
    leadPos = None
    leadExists = False

    for i in range(0, len(ls)):
        remainder = ls[i][0] % 3
        if remainder == 1:
            return False
        if remainder == 2:
            if leadExists:
                return False
            leadPos = i
            leadExists = True

    for i in range(0, len(ls)):
        if leadPos != i:
            if not Check(ls[i], i == 3):
                return False

    success = False
    jlist = ls[leadPos]

    for j in range(1, len(jlist)):
        if jlist[j] >= 2:
            jlist[j] -= 2
            jlist[0] -= 2
            if Check(jlist, leadPos == 3):
                success = True
            jlist[j] += 2
            jlist[0] += 2
            if success:
                break

    return success


def AnalyzeHand(hand):
    types = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    for i in range(0, len(hand)):
        tile = hand[i]

        if (tile.id > 10) and (tile.id < 20):
            types[0][0] += 1
            types[0][tile.id - 10] += 1
        if (tile.id > 20) and (tile.id < 30):
            types[1][0] += 1
            types[1][tile.id - 20] += 1
        if (tile.id > 30) and (tile.id < 40):
            types[2][0] += 1
            types[2][tile.id - 30] += 1
        if (tile.id > 40) and (tile.id < 50):
            types[3][0] += 1
            types[3][tile.id - 40] += 1

    result = IsWinning(types)
    return result


buttonEliminate["state"] = DISABLED
buttonPeng["state"] = DISABLED
buttonChi["state"] = DISABLED
buttonWin["state"] = DISABLED

StartGame()
window.mainloop()

'''
testHand = []
testImg = PhotoImage(file="./res/back.png")

for i in [3, 4, 5]:
    tile = Tile(1, i, testImg, window)
    testHand.append(tile)

for i in [3, 4, 4, 5, 5, 6]:
    tile = Tile(2, i, testImg, window)
    testHand.append(tile)

for i in [1, 1, 7, 7, 7]:
    tile = Tile(3, i, testImg, window)
    testHand.append(tile)

r = AnalyzeHand(testHand)
print(r)
'''

'''
testCPUHand = []
testImg = PhotoImage(file="./res/back.png")

for i in [2, 6, 7]:
    tile = Tile(1, i, testImg, window)
    testCPUHand.append(tile)

for i in [7, 9]:
    tile = Tile(2, i, testImg, window)
    testCPUHand.append(tile)

for i in [2, 4]:
    tile = Tile(3, i, testImg, window)
    testCPUHand.append(tile)

for i in [1, 1, 3, 5, 6, 7, 7]:
    tile = Tile(4, i, testImg, window)
    testCPUHand.append(tile)

r = CPUSelect(testCPUHand)
print(testCPUHand[r].getID())
'''
