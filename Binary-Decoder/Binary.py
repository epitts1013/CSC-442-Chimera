import sys
from textwrap import wrap

def main():
    content = getContent()
    binaryConvert(content, 7)
    binaryConvert(content, 8)


def getContent():
    for line in sys.stdin:
        return line.rstrip()

    
def binaryConvert(content, length):
    text = ""

    if (len(content) % length) == 0: 
        wrapped_content = wrap(content, length)

        for character in wrapped_content:

            int_content = int(character, 2)
            text += chr(int_content)

        print("=============================================")
        print("Solution : " + text)
        print("=============================================")
    
main()