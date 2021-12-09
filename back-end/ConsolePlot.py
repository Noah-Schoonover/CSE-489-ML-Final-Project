def printHex(array):
    for row in array:
        for num in row:
            k = hex(num)            #converts to hexadecimal
            k = k[2:]               #keeps everything after the second character, removes 0x
            if len(k) == 1:         #if k is only one character
                k = "0" + k         #adds a preceding zero
            print(k + " ", end='')  #prints hex value and a space, no linebreak
        print()                     #breaks line

def printImage(array, stretch, invert): #prints image with ascii

    if invert:
        CHAR_1 = "8"
        CHAR_2 = "/"
        CHAR_3 = "."
        CHAR_4 = " "
    else:
        CHAR_1 = " "
        CHAR_2 = "."
        CHAR_3 = "/"
        CHAR_4 = "8"

    THRESHOLD_1 = 64
    THRESHOLD_2 = 128
    THRESHOLD_3 = 190
    
    HSTRETCH = stretch           #Horizontal stretch


    def getSymbol(val):
        if val <= THRESHOLD_1:
            return CHAR_1
        elif val <= THRESHOLD_2:
            return CHAR_2
        elif val <= THRESHOLD_3:
            return CHAR_3
        else:
            return CHAR_4
        
    for row in array:
        for num in row:
            for z in range(HSTRETCH):               #This just prints the character as many
                print(getSymbol(num), end='')       #times as specified in HSTRETCH
            print(getSymbol(num), end='')           #end='' prevents line break
        print()                                     #breaks line
