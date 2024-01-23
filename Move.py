from Symbol import *
from Algorithm import closest_stack_search
def move_input(board, player): #funkcija za unos poteza
    move = input(f"{"Beli" if player is W else "Crni"} na potezu. Unesite potez: ")
    if(move.upper()=="PREDAJEM"):
        return "PREDAJEM"
    move = tuple(move.split())
    moveValid = moveValidation(move, board, player)
    while (moveValid[0] == False):
        print("Neispravan unos poteza!")
        print(moveValid[1])
        move = tuple(input("Ponovo unesite potez: ").split())
        moveValid = moveValidation(move, board, player)
    return moveValid

def moveValidation(move, board, player): #funkcija koja proverava ispravnost unetog poteza
    dim = len(board)
    errMessage=""
    letterToNumber = {}
    for i in range(dim):
        letterToNumber.update({chr(65+i): i})
    if (len(move) != 4):
        errMessage="Morate uneti 4 parametara oblika: red, kolona, mesto, smer"
        return (False,errMessage)
    row, col, placeInStack, direction = move

    if (len(row)>1) or (ord(row)<65 or (ord(row)>90 and ord(row)<97) or ord(row)>122):
        errMessage="Red mora da bude slovo"
        return (False,errMessage)
    if(False in [True if ord(x)>47 and ord(x)<58 else False for x in col]):
        errMessage="Kolona mora da bude broj"
        return (False,errMessage)
    if(False in [True if ord(x)>47 and ord(x)<58 else False for x in placeInStack]):
        errMessage="Mesto na steku mora da bude broj"
        return (False,errMessage)
    direction = direction.upper()
    if(direction not in ["GL", "GD", "DL", "DD"]):
        errMessage="Smer mora da bude jedan od sledecih: GL, GD, DL, DD"
        return (False,errMessage)
    row = row.upper()
    row = letterToNumber.get(row, False)
    col = int(col)-1
    placeInStack = int(placeInStack) - 1
    if (row is False) or (row < 0 or row > dim - 1):
        errMessage="Zadato polje ne postoji na tabli! - Nevalidan red"
        return (False,errMessage)
    if (col < 0 or col > dim - 1):
        errMessage="Zadato polje ne postoji na tabli! - Nevalidna kolona"
        return (False,errMessage)

    if (placeInStack < 0 or placeInStack > 6):
        errMessage="Nevalidno uneta pozicija figure na steku!"
        return (False,errMessage)

    dstFieldRow, dstFieldCol = direction_to_RowCol(direction, row, col, dim)
    if(type(dstFieldRow) is bool):
        if(dstFieldRow == False):
            return (dstFieldRow, dstFieldCol)

    if (board[row][col][placeInStack] == "_"):
        errMessage = "Ne postoji figura na zadatom mestu na steku na zadatom polju!"
        return (False, errMessage)
    if (board[row][col][placeInStack] != player):
        errMessage = "Ne mozete igrati figurom drugog igraca!"
        return (False, errMessage)

    numFiguresToMove = 0
    for i in range(placeInStack, 7):
        if(board[row][col][i] == "_"):
            break
        numFiguresToMove=numFiguresToMove+1

    dstPlaceInStack=0
    for i in range(8):
        if(board[dstFieldRow][dstFieldCol][i] == "_"):
            dstPlaceInStack=i
            break

    closestStackDistance = closest_stack_search(board, row, col)
    if (closestStackDistance!=1):
        closestStackDistance2 = closest_stack_search(board, dstFieldRow, dstFieldCol, row, col)
        if (closestStackDistance2+1 != closestStackDistance):
            errMessage = "Potez ne vodi ka jednom od najbližih stekova!"
            return (False, errMessage)
    else:
        if((dstFieldRow, dstFieldCol) not in neighbourNotEmpty(board, row, col)):
            errMessage = "Potez ne vodi ka jednom od najbližih stekova!"
            return (False, errMessage)

    numFiguresCanBeMoved = 8 - dstPlaceInStack
    if(numFiguresToMove>numFiguresCanBeMoved):
        errMessage = "Na odredisnom polju nema dovoljno mesta za figure!"
        return (False, errMessage)

    if (placeInStack!=0):
        if(not movingStacksRule(placeInStack, dstPlaceInStack)):
            errMessage = "Potez se ne moze odigrati prema pravilima pomeranja definisanim za stekove!"
            return (False, errMessage)

    return (True, (row, col, placeInStack, direction))

def direction_to_RowCol(direction, row, col, dim):
    dstFieldRow = 0
    dstFieldCol = 0
    if (direction == "GL"):
        if (row - 1 < 0 or col - 1 < 0):
            errMessage = "Nije moguce pomeranje figura u zadatom smeru!"
            return (False, errMessage)
        dstFieldRow = row - 1
        dstFieldCol = col - 1
    elif (direction == "GD"):
        if (row - 1 < 0 or col + 1 > dim - 1):
            errMessage = "Nije moguce pomeranje figura u zadatom smeru!"
            return (False, errMessage)
        dstFieldRow = row - 1
        dstFieldCol = col + 1
    elif (direction == "DL"):
        if (row + 1 > dim - 1 or col - 1 < 0):
            errMessage = "Nije moguce pomeranje figura u zadatom smeru!"
            return (False, errMessage)
        dstFieldRow = row + 1
        dstFieldCol = col - 1
    elif (direction == "DD"):
        if (row + 1 > dim - 1 or col + 1 > dim - 1):
            errMessage = "Nije moguce pomeranje figura u zadatom smeru!"
            return (False, errMessage)
        dstFieldRow = row + 1
        dstFieldCol = col + 1
    return dstFieldRow, dstFieldCol

def movingStacksRule(placeInStack, dstPlaceInStack): # da li se potez moze odigrati prema pravilima pomeranja definisanim za stekove
    if(placeInStack>=dstPlaceInStack):
        return False
    else:
        return True

def everyPossibleMove(board, player):
    dim=len(board)
    validMoves=[]
    letterToNumber = {}
    for i in range(dim):
        letterToNumber.update({i: chr(65+i)})
    for r in range(dim):
        for c in range(dim):
            for s in range(7):
                if(board[r][c][s]==player):
                    isValidMove = moveValidation((letterToNumber.get(r), str(c+1), str(s+1), "GL"),board, player)
                    if(isValidMove[0]):
                        validMoves.append((r, c, s, "GL"))
                    isValidMove = moveValidation((letterToNumber.get(r), str(c+1), str(s+1), "GD"),board, player)
                    if(isValidMove[0]):
                        validMoves.append((r, c, s, "GD"))
                    isValidMove = moveValidation((letterToNumber.get(r), str(c+1), str(s+1), "DL"),board, player)
                    if(isValidMove[0]):
                        validMoves.append((r, c, s, "DL"))
                    isValidMove = moveValidation((letterToNumber.get(r), str(c+1), str(s+1), "DD"),board, player)
                    if(isValidMove[0]):
                        validMoves.append((r, c, s, "DD"))
    return validMoves

def neighbourNotEmpty(board, row, col):
    dim = len(board)
    ls=list()
    if (row-1 >= 0 and col-1 >= 0):
        if board[row-1][col-1][0] != "_":
            ls.append((row-1,col-1))
    if (row-1 >= 0 and col+1 < dim):
        if board[row-1][col+1][0] != "_":
            ls.append((row-1,col+1))
    if (row+1 < dim and col-1 >= 0):
        if board[row+1][col-1][0] != "_":
            ls.append((row+1,col-1))
    if (row+1 < dim and col+1 < dim):
        if board[row+1][col+1][0] != "_":
            ls.append((row+1,col+1))
    return ls

def convertMoveForPrint(move):
    r, c, p, d = move
    r = chr(65+r)
    c = c + 1
    p = p + 1
    return (r,c,p,d)

