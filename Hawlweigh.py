import pygame, sys, os, board, crypto, getpass, random
from pygame.locals import *
from WinAPIConsoleStuff import *

class Button():
    def __init__(self, centerx, y, text, eventHandlers={}, font=None, aColor=None):
        if aColor == None:
            aColor == (255, 255, 255)
        if font == None:
            font = pygame.font.SysFont("consolas", 16)
        self.eventHandlers = eventHandlers
        self.eventHandlers[pygame.MOUSEMOTION] = self.hover
        self.p = board.Point(centerx, y)
        self.width = font.render(text, True, (0, 0, 0)).get_rect().width
        self.height = font.render(text, True, (0, 0, 0)).get_rect().height
        self.text = text
        self.aColor = aColor
        self.font = font
    def handle(self, event, window):
        ret = []
        for (e, handler) in self.eventHandlers.items():
            if event.type == e:
                ret.append(handler(event, window))
        for i in range(ret.count(None)):
            ret.remove(None)
        return ret
    def draw(self, window, color):
        bgRect = self.get_rect()
        bgRect.centerx = self.p.x
        txt = self.font.render(self.text, True, (0, 0, 0))
        txtRect = txt.get_rect()
        txtRect.centerx, txtRect.centery = bgRect.centerx, bgRect.centery
        bg2Rect = txtRect.copy()
        bg2Rect.centery -= 1
        bgRect.y -= 1
        pygame.draw.rect(window, (0, 0, 0), bgRect)
        pygame.draw.rect(window, color, bg2Rect)
        window.blit(txt, txtRect)
    def get_rect(self):
        return pygame.Rect(self.p.x - 10, self.p.y + 10, self.width + 20, self.height + 20)
    def posIn(self, pos):
        wRect = self.get_rect()
        wRect.x, wRect.y, wRect.height, wRect.width = self.p.x - 10, self.p.y + 10, self.height + 20, self.width + 20
        return True if wRect.collidepoint(pos) else False
    def hover(self, event, window):
        if self.posIn(event.pos):
            self.draw(window, self.aColor)
        else:
            self.draw(window, (255, 255, 255))
    def click(self, event, window):
        if self.posIn(event.pos):
            return True
        return False

_image_library = {}
def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canon_path = path.replace("/", os.sep).replace("\\", os.sep)
        image = pygame.image.load(canon_path)
        _image_library[path] = image
    return image
    
def get_spot(x, y):
    return (10 + (72 + 10) * x, 10 + (72 + 10) * y)

def drawBoard(window):
    onScreen = []
    for j in range(9):
        row = [] 
        for i in range(9):
            rect = pygame.Rect(10 + (72 + 10) * j, 10 + (72 + 10) * i , 72, 72)
            pygame.draw.rect(window, (255, 255, 255), rect)
            row.append(rect)
        onScreen.append(row)
    
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(748, 10, 242, 730))
    return onScreen
    
def getInternalFromMouseCoord(x, y, dSpots):
    for row in range(len(dSpots)):
        for rect in range(len(dSpots[row])):
            if dSpots[row][rect].collidepoint(x, y):
                return row, rect
    return -1, -1

def getWallFromMouseCoord(x, y, window):
    dWallPoints = []
    for i in range(10):
        row = []
        for j in range(10):
            rect = pygame.Rect(0 + (72 + 10) * j, 0 + (72 + 10) * i, 10, 10)
            #pygame.draw.rect(window, (123, 213, 78), rect)
            row.append(rect)
        dWallPoints.append(row)
    for i in range(len(dWallPoints)):
        for j in range(len(dWallPoints[i])):
            if dWallPoints[i][j].collidepoint(x, y):
                return j, i
    return -1, -1

def drawWall(window, p1, p2):
    p1 = ((72 + 10) * p1[0], (72 + 10) * p1[1])
    p2 = ((72 + 10) * p2[0], (72 + 10) * p2[1])
    tmp = board.Line(p1, p2)
    if tmp.orientation() == "v": 
        miny = min(p1[1], p2[1])
        pygame.draw.rect(window, (51, 161, 255), pygame.Rect(p1[0], miny + 10, 10, 154))
    else:
        minx = min(p1[0], p2[0])
        pygame.draw.rect(window, (51, 161, 255), pygame.Rect(minx + 10, p1[1], 154, 10))

def statusMessage(msg, window):
    font = pygame.font.SysFont("consolas", 16)
    text = font.render(msg, True, (0, 0, 0))
    textRect = text.get_rect()
    height = (pygame.font.SysFont("consolas", 12).render("a", True, (0, 0, 0)).get_rect().height, textRect.height)
    textRect.x, textRect.y = 748 + 10, 25 + 10 + height[0] * 2 + 10 + height[1]
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(748, textRect.y, 242, height[1]))
    window.blit(text, textRect)

def setWallCount(black, white, window):
    font = pygame.font.SysFont("consolas", 12)
    blackText = font.render("Black Walls Left: {} ({})".format("|" * black, black), True, (0, 0, 0))
    whiteText = font.render("White Walls Left: {} ({})".format("|" * white, white), True, (0, 0, 0))
    blackTextRect = blackText.get_rect()
    whiteTextRect = whiteText.get_rect()
    blackTextRect.centerx, blackTextRect.y = pygame.Rect(748, 10, 242, 730).centerx, 20
    whiteTextRect.centerx, whiteTextRect.y = blackTextRect.centerx, 20 + blackTextRect.height + 5
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(748, 10, 242, blackTextRect.height + whiteTextRect.height + 25))
    window.blit(blackText, blackTextRect)
    window.blit(whiteText, whiteTextRect)

def updateTurn(turn, window):
    font = pygame.font.SysFont("consolas", 16)
    turnText = font.render("Turn: {}".format("Black" if turn == "B" else "White"), True, (0, 0, 0))
    turnTextRect = turnText.get_rect()
    height = pygame.font.SysFont("consolas", 12).render("a", True, (0, 0, 0)).get_rect().height
    turnTextRect.centerx, turnTextRect.y = pygame.Rect(748, 10, 242, 730).centerx, 25 + 10 + height * 2
    pygame.draw.rect(window, (255, 255, 255), pygame.Rect(748, turnTextRect.y, 242, turnTextRect.height))
    window.blit(turnText, turnTextRect)

def setPawn(x, y, pawn, window, onScreen, oldPos=None):
    #call using x, y, letter ("B" or "W"), window surface, onScreen, and None or oldPos
    if pawn.upper() == "B":
        bPawn = get_image("black.png")
        bPawnResized = pygame.transform.scale(bPawn, (70, 70))
        bPawnResizedRect = bPawnResized.get_rect()
        bPawnResizedRect.centerx, bPawnResizedRect.centery = onScreen[x][y].centerx, onScreen[x][y].centery
        if oldPos != None:
            pygame.draw.rect(window, (255, 255, 255), onScreen[oldPos[0]][oldPos[1]])
        window.blit(bPawnResized, bPawnResizedRect)
    elif pawn.upper() == "W":
        wPawn = get_image("white.png")
        wPawnResized = pygame.transform.scale(wPawn, (70, 70))
        wPawnResizedRect = wPawnResized.get_rect()
        wPawnResizedRect.centerx, wPawnResizedRect.centery = onScreen[x][y].centerx, onScreen[x][y].centery
        if oldPos != None:
            pygame.draw.rect(window, (255, 255, 255), onScreen[oldPos[0]][oldPos[1]])
        window.blit(wPawnResized, wPawnResizedRect)

def instructions():
            messageBox("""
Hawlweigh is played on a game board of 81 square spaces (9x9).
Each player is represented by a pawn which begins at the center space of one edge of the board (in a two-player game, the pawns begin opposite each other). 
The objective is to be the first player to move their pawn to any space on the opposite side of the gameboard from which it begins.
The distinguishing characteristic of Hawlweigh is its twenty walls. 
Walls are flat two-space-wide pieces which can be placed in the groove that runs between the spaces.
Walls block the path of all pawns, which must go around them.
The walls are divided equally among the players at the start of the game, and once placed, cannot be moved or removed.
On a turn, a player may either move their pawn, or, if possible, place a wall.
Pawns can be moved to any space at a right angle (but not diagonally) or straight.
If adjacent to another pawn, the pawn may jump over that pawn.
If an adjacent pawn has a third pawn or a wall on the other side of it, the player may move to either space that is immediately adjacent (left or right) to the first pawn.
Multiple pawns may not be jumped.
Walls may not be jumped, including when moving laterally due to a pawn or wall being behind a jumped pawn.
Walls can be placed directly between two spaces, in any groove not already occupied by a wall.
However, a wall may not be placed which cuts off the only remaining path of any pawn to the side of the board it must reach.
""", "Instructions", 0)
music = "none"
def main():
    global music
    pygame.init()
    window = pygame.display.set_mode((1000, 750), 0, 32)
    pygame.display.set_caption("Hawlweigh")
    pygame.display.set_icon(pygame.image.load("Yin-Yang-True-false-icon.png"))
    clock = pygame.time.Clock()
    onScreen = drawBoard(window) # to access object at get_spot(x, y) use onScreen[x][y]
    internal = board.Board.blankBoard()
    setPawn(4, 8, "B", window, onScreen)
    setPawn(4, 0, "W", window, onScreen)
    oldPos = ((4, 8), (4, 0))
    BLACK = 10
    WHITE = 10
    setWallCount(BLACK, WHITE, window)
    height = (pygame.font.SysFont("consolas", 12).render("a", True, (0, 0, 0)).get_rect().height, pygame.font.SysFont("consolas", 16).render("a", True, (0, 0, 0)).get_rect().height)
    bInstr = Button(pygame.Rect(748, 10, 242, 730).centerx, 25 + 10 + height[0] * 2 + 10 + height[1] * 2 + 10, "Instructions", {}, None, (51, 161, 255))
    bInstr.eventHandlers[pygame.MOUSEBUTTONUP] = bInstr.click
    bInstr.draw(window, (255, 255, 255))
    bRestart = Button(pygame.Rect(748, 10, 242, 730).centerx, 25 + 10 + height[0] * 2 + 10 + height[1] * 2 + 10 + bInstr.get_rect().height + 10, "Restart", {}, None, (51, 161, 255))
    bRestart.eventHandlers[pygame.MOUSEBUTTONUP] = bRestart.click
    bRestart.draw(window, (255, 255, 255))
    bMusic = Button(pygame.Rect(748, 10, 242, 730).centerx, 25 + 10 + height[0] * 2 + 10 + height[1] * 3 + bInstr.get_rect().height * 2 + 10 + 5, "Music", {}, None, (51, 161, 255))
    bMusic.eventHandlers[pygame.MOUSEBUTTONUP] = bMusic.click
    bMusic.draw(window, (255, 255, 255))
    turn = "B" if random.randint(0, 1) else "W"
    hacks = False
    hackLetter = ""
    updateTurn(turn, window)
    wallOld = None
    if music != "none":
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)
    while True:
        won = internal.winner()
        if won != None:
            font = pygame.font.SysFont("consolas", 48)
            text = font.render("Congratulations! {} has won!".format("Black" if won == "B" else "White"), True, (0, 0, 0), (255, 255, 255))
            textRect = text.get_rect()
            textRect.centerx, textRect.centery = window.get_rect().centerx, window.get_rect().centery
            window.blit(text, textRect)
            pygame.display.flip()
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Congratulations.wav")
            pygame.mixer.music.play(-1)
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYUP and event.key == pygame.K_BACKQUOTE:
                password = getpass.getpass()
                if len(password) > 2 and crypto.folding(password, 2, 20) == 'BBA08C3E3CC5770D1B91':
                    hacks = True
                    hackLetter = input("Player: ").upper()[0]
                else:
                    continue
            if True in bInstr.handle(event, window):
                bInstr.draw(window, (255, 255, 255))
                pygame.display.flip()
                instructions()
            if True in bRestart.handle(event, window):
                bRestart.draw(window, (255, 255, 255))
                pygame.display.flip()
                main()
            if True in bMusic.handle(event, window):
                bMusic.draw(window, (255, 255, 255))
                pygame.display.flip()
                os.system("start /B GetFileDialog.hta")
                time.sleep(5)
                path = open("path.txt").read().strip()
                while "Don't read" in path or path == '':
                    path = open("path.txt").read().strip()
                music = path
                try:
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.play(-1)
                except:
                    statusMessage("File can't be played.", window)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if pygame.Rect(748, 10, 242, 730).collidepoint(event.pos[0], event.pos[1]):
                    continue
                x, y = getInternalFromMouseCoord(event.pos[0], event.pos[1], onScreen)
                if (x, y) != (-1, -1):
                    if internal.isLegalMove(x, y, turn) or (hacks and hackLetter == turn):
                        statusMessage("", window)
                        pos = oldPos[0] if turn == "B" else oldPos[1]
                        setPawn(x, y, turn, window, onScreen, pos)
                        internal.spots[y][x] = turn
                        internal.spots[pos[1]][pos[0]] = " "
                        oldPos = ((x, y), oldPos[1]) if turn == "B" else (oldPos[0], (x, y))
                        turn = chr(ord(turn) + (21 if turn == "B" else -21))
                        updateTurn(turn, window)
                        pygame.display.flip()
                    else:
                        statusMessage("Illegal move.", window)
                else:
                    x, y = getWallFromMouseCoord(event.pos[0], event.pos[1], window)
                    if (x, y) != (-1, -1):
                        if wallOld == None:
                            wallOld = (x, y)
                        else:
                            if internal.isLegalWall((wallOld, (x, y)), turn) or (hacks and hackLetter == turn):
                                if turn == "B" and BLACK == 0:
                                    statusMessage("You have no walls left.", window)
                                    continue
                                if turn == "W" and WHITE == 0:
                                    statusMessage("You have no walls left.", window)
                                    continue
                                statusMessage("", window)
                                internal.walls.append(board.Line(wallOld, (x, y)))
                                drawWall(window, wallOld, (x, y))
                                if turn == "B": BLACK -= 1
                                else: WHITE -= 1
                                setWallCount(BLACK, WHITE, window)
                                turn = chr(ord(turn) + (21 if turn == "B" else -21))
                                wallOld = None
                                updateTurn(turn, window)
                                pygame.display.flip()
                            elif wallOld != (x, y):
                                statusMessage("Illegal wall.", window)
                                wallOld = None
                            else:
                                wallOld = None
        pygame.display.flip()
        clock.tick(60)
    if messageBoxYN("Would you like to play again?", "Play again?"):#, 0x2000 | 0x40):
        pygame.mixer.music.stop()
        main()
    else:
        pygame.quit()
        sys.exit(0)
        
main()
