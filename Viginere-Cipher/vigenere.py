import sys
# Vigenere cipher

def encode(text,key): # Encodes plaintext using a given key
    cipher = "" # The encoded plaintext
    count = 0
    for i in range(len(text)): # Iterate over the plaintext
        if(text[i] in LETTER_CODES_HIGH): # If the current character is uppercase
            cipher += LETTERS_HIGH[(LETTER_CODES_HIGH[text[i]]+(LETTER_CODES_HIGH[(key[(i-count)%len(key)]).upper()]))%len(LETTERS_HIGH)]
        elif(text[i] in LETTER_CODES_LOW): # If the current character is lowercase
            cipher += LETTERS_LOW[(LETTER_CODES_LOW[text[i]]+(LETTER_CODES_LOW[(key[(i-count)%len(key)]).lower()]))%len(LETTERS_LOW)]
        else: # The current character is not a letter
            count += 1
            cipher += text[i] # Don't convert non-letter characters    
    return cipher

def decode(cipher,key): # Decodes encoded text using a given key
    text = "" # The decoded cipher
    count = 0
    for i in range(len(cipher)): # Iterate over the plaintext
        if(cipher[i] in LETTER_CODES_HIGH): # If the current character is uppercase
            text += LETTERS_HIGH[(LETTER_CODES_HIGH[cipher[i]]-(LETTER_CODES_HIGH[(key[(i-count)%len(key)]).upper()]))%len(LETTERS_HIGH)]
        elif(cipher[i] in LETTER_CODES_LOW): # If the current character is lowercase
            text += LETTERS_LOW[(LETTER_CODES_LOW[cipher[i]]-(LETTER_CODES_LOW[(key[(i-count)%len(key)]).lower()]))%len(LETTERS_LOW)]
        else: # The current character is now a letter
            count += 1
            text += cipher[i] # Don't convert non-letter characters
    return text

def key_text(text): # Removes non-letter characters from a string
    plaintext = ""
    for i in range(len(text)):
        if(text[i] != " "):
            plaintext += text[i]
    return plaintext

# Uppercase letters
LETTERS_HIGH = ('A','B','C','D','E','F','G','H','I','J','K','L','M',
                'N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
# Lowercase letters
LETTERS_LOW = ('a','b','c','d','e','f','g','h','i','j','k','l','m',
               'n','o','p','q','r','s','t','u','v','w','x','y','z')
LETTER_CODES_HIGH = {} # Stores numerical values of uppercase letters
LETTER_CODES_LOW = {} # Stores numerical values of lowercase letters

for i in range(len(LETTERS_HIGH)): # Builds lower- and uppercase dictionaries' letter values.
    LETTER_CODES_HIGH[LETTERS_HIGH[i]] = i
    LETTER_CODES_LOW[LETTERS_LOW[i]] = i

task = sys.argv[1] # -e or -d to specify decoding or encoding using the given key.
key = key_text(sys.argv[2]) # Cipher key from command line arguments, with non-letter characters removed.


if(task == "-e"): # Encoding using the given key
    try:
        while(True):
            print(encode(input(),key)) # Reads all text in stdin
    except EOFError: # Exits script on end of file
        exit(0)
elif(task == "-d"): # Decoding using the given key
    try:
        while(True):
            print(decode(input(),key)) # Reads all ciphers in stdin
    except EOFError: # Exits script on end of file
        exit(0)
