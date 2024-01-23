from Board import create_board, print_board, endOfTheGame, makeMove
from Symbol import *
from Move import move_input, everyPossibleMove, convertMoveForPrint
from Algorithm import minimax_alpha_beta
def start_game(n):
    computer = (False if input("Izaberite mod igranja:\n1 - igrac protiv kompjutera\n2 - igrac protiv igraca\n") == "2" else True)
    player = (W if input("Da li zelite da igrate belim figurama? ").upper() == "DA" else B) if (computer) else W #izbor boja figura (U slucaju igrac protiv igraca - prvi igrac bira kojim ce figurama da igra)
    turn = True if player == W else False #postavlja se da li je igrac na potezu, beli uvek igra prvi. ***(sluzi za mod igrac protiv kompjutera)
    board = create_board(n)
    stacks=[0,0]
    print_board(board, stacks)
    #print("Pravila igre...") #detaljna uputstva o nacinu pomeranja figura i ostalim detaljima vezanim za igru
    print("• Potezi se zadaju u obliku 4 parametara:"
          "\n\t 1. - slovo koje oznacava red"
          "\n\t 2. - broj koji oznacava kolonu"
          "\n\t 3. - broj koje oznacava figuru na steku"
          "\n\t 4. - rec od 2 karaktera koja oznacava pravac pomeranja figura ('gl' - gore levo, 'gd' - gore desno, 'dl' - dole levo, 'dd' - dole desno)")
    print("• Primer pravilno unesenog poteza: d 4 1 dd")
    print("• Igrac moze predati mec ukoliko umesto poteza upise rec 'predajem'")
    surFlag = False
    maxStacks = totalStacksNum(n)
    while (not endOfTheGame(board, stacks, maxStacks)):
        if (computer and turn == False):
            min_max_alpha_beta_result = minimax_alpha_beta(board, 3, turn if player is W else not turn, stacks, maxStacks) # za tablu 8x8 preporucljivo stavljati dubinu 1-4
            if (min_max_alpha_beta_result[0] is None):
                print(f"{"Crni" if player is W else "Beli"} nema ni jedan valjan potez, stoga se isti prepusta protivniku!")
            else:
                board, stacks = makeMove(board, min_max_alpha_beta_result[0], stacks)
                print_board(board, stacks)
                print(f"{"Crni" if player is W else "Beli"} je odigrao potez {convertMoveForPrint(min_max_alpha_beta_result[0])}")
        else:
            if (everyPossibleMove(board, player) == []):
                print(f"{"Beli" if player is W else "Crni"} nema ni jedan valjan potez, stoga se isti prepusta protivniku!")
                if (not computer):
                    player = B if player is W else W
            else:
                moveValid = move_input(board, player)
                if (moveValid == "PREDAJEM"):
                    surFlag = True
                    break
                board, stacks = makeMove(board, moveValid[1], stacks)
                if (not computer):
                    player = B if player is W else W
                print_board(board, stacks)
        turn = not turn
    if(surFlag):
        print(f"{"Beli" if player is W else "Crni"} je predao. Pobednik je: {"Crni" if player is W else "Beli"}!")
        return
    winner = "Beli" if stacks[0]>stacks[1] else "Crni" if stacks[1]>stacks[0] else "D"
    if(winner == "D"):
        print("Nereseno!")
    else:
        print(f"Pobednik je: {winner}!")
def totalStacksNum(n):
    return n*(n-2)/16
def inputDim():
    while(True):
        dim = input("Uneti dimenziju table: ")
        notNumflag = False
        for i in dim:
            if(False if ord(i) >= 48 and ord(i) <= 57 else True):
                notNumflag = True
        if (notNumflag):
            print("Dimenzija mora da bude broj!")
            continue
        if (len(dim)==0):
            print("Morate uneti neku vrednost!")
            continue
        n = int(dim)
        if (n < 0):
            print("Dimenzija ne moze da bude negativan broj!")
            continue
        if (n == 0):
            print("Dimenzija ne moze da bude 0!")
            continue
        if (n < 8):
            print("Dimenzija je premala!")
            continue
        if (n > 58):
            print("Dimenzija je prevelika!")
            continue
        if (n % 2 != 0):
            print("Dimenzija mora biti parna!")
            continue
        figNum = n * (n - 2) / 2
        if (figNum % 8 != 0):
            print("Dimenzija n mora da budu takva da je broj figura deljiv sa 8! (Broj figura = n*(n-2)/2)")
            continue
        return n

if __name__ == '__main__':
    start_game(inputDim())


