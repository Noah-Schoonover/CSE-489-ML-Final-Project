import numpy as np
from keras.datasets import mnist
import ConsolePlot as cp

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = np.where(train_images > 80, 255, 0)
test_images = np.where(test_images > 80, 255, 0)

print('')
print('shape of training images Tensor:',train_images.shape)
print('shape of test images Tensor:',test_images.shape)
print('')
print('''Search syntax:
    \t<L or T> <i>,<i>,<i>\tgives indexed images
    \t<L or T> <i>-<i>\tgives a range of indexed images
    \t<L or T> <i>,<i>-<i>\tcombination of range and specific indexing

    \tL or T (for learning and testing)
    \tIndex: any whole number''')

testing_library = test_images
learning_library = train_images

def convertToInt(d):
    if d == '-':
        return '-'
    else:
        return(int(d))

def getDigits(l, q):
    queue = []
    digits = q[1:].strip()
    digits = digits.replace(' ','')

    newDigits = ''
    for x in range(len(digits)):
        if digits[x] == '-':
            if digits[x-1] != ',':
                newDigits = newDigits + ',' + digits[x]
            if digits[x+1] != ',':
                newDigits = newDigits + ','
        else:
            newDigits = newDigits + digits[x]
    digits = newDigits
        
    invalid = False
    for char in digits:
        if (char.isdigit() == False) and (char != '-') and (char != ','):
            invalid = True
    if not invalid:
        digits = digits.split(',')
        digits = list(filter(None, digits))
        digits = [convertToInt(digit) for digit in digits]
        print(digits)
        for x in range(len(digits)):
            if digits[x] != '-':
                queue.append(digits[x])
            else:
                reachedTarget = False
                target = digits[x+1]
                val = digits[x-1] + 1
                if val != target:
                    while not reachedTarget:
                        queue.append(val)
                        val = val + 1
                        if val == target:
                            reachedTarget = True
        print(queue)
        for index in queue:
            if index < len(l):
                cp.printImage(l[index], 1, False)
            else:
                print("\nIndex", index, "out of range.")
        print()
    else:
        print("Invalid Arguments")

def getLibrary(q):
    q = q.strip()
    q = q.lower()
    
    if q[0] == "t":
        library = testing_library
        print("testing_library", end='')
        getDigits(library, q)
    elif q[0] == "l":
        library = learning_library
        print("learning_library", end='')
        getDigits(library, q)
    else:
        print("Invalid Library")

while True:
    query = input(': ')
    try:
        getLibrary(query)
    except:
        print("Invalid Entry")
