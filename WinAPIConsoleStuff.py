from ctypes import *
from ctypes import wintypes
import time
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

SHORT = c_short
WORD = c_ushort
WCHAR = c_wchar

FOREGROUND_BLACK     = 0x0000
FOREGROUND_BLUE      = 0x0001
FOREGROUND_GREEN     = 0x0002
FOREGROUND_CYAN      = 0x0003
FOREGROUND_RED       = 0x0004
FOREGROUND_MAGENTA   = 0x0005
FOREGROUND_YELLOW    = 0x0006
FOREGROUND_GREY      = 0x0007
FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.

BACKGROUND_BLACK     = 0x0000
BACKGROUND_BLUE      = 0x0010
BACKGROUND_GREEN     = 0x0020
BACKGROUND_CYAN      = 0x0030
BACKGROUND_RED       = 0x0040
BACKGROUND_MAGENTA   = 0x0050
BACKGROUND_YELLOW    = 0x0060
BACKGROUND_GREY      = 0x0070
BACKGROUND_INTENSITY = 0x0080 # background color is intensified.

class COORD(Structure):
    _fields_ = [("X", SHORT), ("Y", SHORT)]
    
class SMALL_RECT(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("Left", SHORT),
    ("Top", SHORT),
    ("Right", SHORT),
    ("Bottom", SHORT)]  
    
class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [
    ("dwSize", COORD),
    ("dwCursorPosition", COORD),
    ("wAttributes", WORD),
    ("srWindow", SMALL_RECT),
    ("dwMaximumWindowSize", COORD)]

LPOFNHOOKPROC = CFUNCTYPE(c_uint, wintypes.HWND, c_uint, wintypes.WPARAM, wintypes.LPARAM)
class OPENFILENAME(Structure):
    _fields_ = [
    ("lStructSize", wintypes.DWORD),
    ("hwndOwner", wintypes.HWND), 
    ("hInstance", wintypes.HINSTANCE),
    ("lpstrFilter", wintypes.LPCWSTR),
    ("lpstrCustomFilter", wintypes.LPWSTR),
    ("nMaxCustFilter", wintypes.DWORD),
    ("nFilterIndex", wintypes.DWORD),
    ("lpstrFile", c_char_p),
    ("nMaxFile", wintypes.DWORD),
    ("lpstrInitialDir", wintypes.LPCWSTR),
    ("lpstrTitle", wintypes.LPCWSTR),
    ("Flags", wintypes.DWORD),
    ("nFileOffset", wintypes.WORD), 
    ("nFileExtension", wintypes.WORD),
    ("lpstrDefExt", wintypes.LPCWSTR),
    ("lCustData",wintypes.LPARAM),
    ("lpfnHook", LPOFNHOOKPROC),
    ("lpTemplateName", wintypes.LPCWSTR), 
    ("pvReserved", c_void_p),
    ("dwReserved", wintypes.DWORD), 
    ("FlagsEX", wintypes.DWORD)]
    
stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo
FillConsoleOutputCharacter = windll.kernel32.FillConsoleOutputCharacterA
FillConsoleOutputAttribute = windll.kernel32.FillConsoleOutputAttribute
SetConsoleCursorPosition = windll.kernel32.SetConsoleCursorPosition

csbi = CONSOLE_SCREEN_BUFFER_INFO()

def setCursor(home = COORD(0, 0), handle = windll.kernel32.GetStdHandle(-11)):
    SetConsoleCursorPosition(handle, home)
    
def changeColor(color, defaultBg=True, background=0):
    handle = windll.kernel32.GetStdHandle(-11)
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    if defaultBg:
        GetConsoleScreenBufferInfo(handle, byref(csbi))
        background = csbi.wAttributes & 0x0070
    color = color | background
    color = wintypes.WORD(color)
    SetConsoleTextAttribute(handle, color)
    
# use like changeColor(FOREGROUND | background | INTENSITY | INTENSITY)
# 
# 
# 
# 
# 

def playWavAsync(path):
    windll.winmm.PlaySoundA(path, None, 131072 | 1) #filename | async
def playWav(path):
    windll.winmm.PlaySoundA(path, None, 131072) #filename

def getSize():
    handle = windll.kernel32.GetStdHandle(-11)
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    GetConsoleScreenBufferInfo(handle, byref(csbi))
    X = csbi.srWindow.Right - csbi.srWindow.Left + 1
    Y = csbi.srWindow.Bottom - csbi.srWindow.Top + 1
    return (X, Y)
    
def center(text, dimension="both", newline=False, clearScreen=True):
    if clearScreen:
        clear()
    (X, Y) = getSize()
    length = len(text)
    positionX = int(((X - length) / 2))
    positionY = int(((Y - 1) / 2))
    newlines = "\n" * positionY
    spaces = " " * positionX
    if dimension == "both" or dimension.lower() == "y":
        print(newlines, end='')
    if dimension == "both" or dimension.lower() == "x":
        print(spaces, end='')
    if newline:
        print(text)
    else:
        print(text, end='')
    return (positionX, positionY)
    
def loading():
    blue = FOREGROUND_BLUE
    green = FOREGROUND_GREEN
    grey = FOREGROUND_GREY
    changeColor(green)
    center("Foster Productions 2017")
    time.sleep(.25)
    clear()
    (X, Y) = getSize()
    X = int(((X - 30) / 2))
    Y = int(((Y - 1) / 2) - 1)
    print("\n" * Y)
    spaces = " " * X
    print(spaces, end='')
    for num in range(1, 26):
        bar = "["
        for i in range(0, num):
            bar += "|"
        for j in range(0, 25 - num):
            bar += " "
        bar += "] {}%\r".format(num * 4)
        print(bar, end='')
        if num != 25:
            print(spaces, end='')
        time.sleep(.5)
    playWavAsync("C:\\Windows\\winsxs\\x86_microsoft-windows-s..undthemes-landscape_31bf3856ad364e35_6.1.7600.16385_none_1e650d9135666d13\\Windows Logon Sound.wav")
    time.sleep(2)
    clear()
    changeColor(grey)
    
def clear():
    setCursor()
    handle = windll.kernel32.GetStdHandle(-11)
    home = COORD(0, 0)
    GetConsoleScreenBufferInfo(handle, byref(csbi))
    conSize = wintypes.DWORD(csbi.dwSize.X * csbi.dwSize.Y)
    charsWritten = wintypes.DWORD() 
    FillConsoleOutputCharacter(handle, WCHAR(" "), conSize, home, byref(charsWritten))
    GetConsoleScreenBufferInfo(handle, byref(csbi))
    FillConsoleOutputAttribute(handle, csbi.wAttributes, conSize, home, byref(charsWritten))
    setCursor()

def messageBox(text, caption, flags):
	#text = wintypes.LPCSTR(text)
	#caption = wintypes.LPCSTR(caption)
	MessageBox = windll.user32.MessageBoxW
	return MessageBox(0, text, caption, flags)

def messageBoxYN(text, caption): # 7 = no, 6 = yes
    #text = wintypes.LPCSTR(text)
    #caption = wintypes.LPCSTR(caption)
    btn = windll.user32.MessageBoxW(0, text, caption, 4)
    if btn == 7:
        return False
    return True

def messageBoxTimeout(text, caption, time, flags):
    text = wintypes.c_char_p(text)
    caption = wintypes.c_char_p(caption)
    return windll.user32.MessageBoxTimeoutA(None, text, caption, c_uint(flags | 0x10000), 0, wintypes.DWORD(time))

def chooseFile():
    openFilename = OPENFILENAME()
    charArray100 = c_char * 100
    szFile = charArray100()
    openFilename.lStructSize = wintypes.DWORD(sizeof(openFilename))
    openFilename.Flags = wintypes.DWORD(0x1000 | 0x80000 | 0x800)
    openFilename.lpstrFilter = "All\0*.*\0"
    openFilename.nFilterIndex = 0
    szFile[0] = "\0"
    openFilename.lpstrFile = pointer(szFile)
    openFilename.nMaxFile = wintypes.DWORD(sizeof(szFile))
    openFilename.hwndOwner = None 
    openFilename.lpstrFileTitle = None
    openFilename.nMaxFileTitle = 0
    openFilename.lpstrInitialDir = None
    ret = windll.comdlg32.GetOpenFileNameA(byref(openFilename))
    if not ret:
        return None
    else:
        return openFilename.lpstrFile
