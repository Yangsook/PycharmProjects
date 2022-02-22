"""
1. turns : integer. I'll using while roof 9 times with this.
2. selected : dictionary. This is for having what numbers each player selected.
3. board : 2x2 list. This is for showing selected numbers.


"""

from colorama import Fore, Back, Style, init
init()


def setInit():
    global turns
    global selected
    global board

    turns = 0
    selected = {"X":[], "O":[]}
    board = [
      ["1", "2", "3"],
      ["4", "5", "6"],
      ["7", "8", "9"]
    ]


def printBoard():
    global board
    print()

    for row in board:
        coloredRow = ""
        for slot in row:
            if slot == "X":
                coloredRow += Fore.BLUE + ' X ' + Style.RESET_ALL
            elif slot == "O":
                coloredRow += Fore.RED  + ' O ' + Style.RESET_ALL
            else:
                coloredRow += ' ' + slot + ' ' + Style.RESET_ALL
        print(coloredRow)


def updateBoard(player, getN):
    global board
    col = (getN - 1) // 3
    row = (getN - 1) % 3
    board[col][row] = player


def checkNumber(getN):
    if getN < 1 or getN > 9:
        print("\t==> It is not valid number!")
        return False
    elif getN in selected["X"] or getN in selected["O"]:
        print("\t==> It is already selected number!")
        return False
    else:
        return True


def checkWin(player):
    global selected
    winCase = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

    for case in winCase:
        cnt = 0
        for n in selected[player]:
            if n in case: cnt += 1

        if cnt == 3:
            print("\n\n**************************************")
            print(f"Congratulation!!  '{player}' player wins!!!!!")
            return True

    return False


def askReplay():
    print("**************************************")
    getYN = input("\nDo you want to play again? (y/n) => ")
    getYN.strip()
    if getYN.upper() == "Y":
        return True
    else:
        return False


print("#####################################")
print("   T i c   T a c   T o e  G a m e")
print("#####################################")

setInit()

while turns < 9:
    if turns % 2 == 0:
        player = "X"
    else:
        player = "O"

    printBoard()
    getNum = input(f"You're '{player}' player! Please choose a number 1 through 9 except already taken!\n")

    try:
        getNum = int(getNum.strip())
    except:
        print("\t==> Wrong Input. Enter the number only!\n")
        continue


    if not checkNumber(getNum):
        continue

    selected[player].append(getNum)
    updateBoard(player, getNum)

    chkWin = checkWin(player)

    if turns == 8:
        print("**************************************")
        print("*******  This game is draw!!!  *******")

    if chkWin or turns == 8:
        printBoard()
        replay = askReplay()

        if replay:
            setInit()
            replay = False
        else:
            break

    turns += 1




