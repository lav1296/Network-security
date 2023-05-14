import re

def generate_grid(key):
    rows={}
    rowsList=[[]]
    key=str(key).upper()
    key=clean_text(key)
    key=str(key).replace("J","I")
    number_of_Col=0
    number_of_row=0
    for letter in key:
        if rows.get(letter)==None:
            rows[letter]=co_ordinate(number_of_row,number_of_Col)
            rowsList[number_of_row].append(letter)
            number_of_Col=number_of_Col+1
        if number_of_Col==5:
            number_of_row=number_of_row+1
            number_of_Col=0
            rowsList.append([])
    for letter in range(65,91,1):
        if letter==ord('J'):
            continue
        if rows.get(chr(letter))==None:
            rows[chr(letter)]=co_ordinate(number_of_row,number_of_Col) 
            rowsList[number_of_row].append(chr(letter))
            number_of_Col=number_of_Col+1
        if number_of_Col==5:
            number_of_row=number_of_row+1
            number_of_Col=0
            rowsList.append([])
    return rows,rowsList
class co_ordinate:
  def __init__(self, row, column):
    self.row = row
    self.column = column

def clean_text(text):

    pattern = r'[^a-zA-Z]'
    return re.sub(pattern, '', text)


def encrypt(grid,gridList,plaintext):
    plaintext=clean_text(plaintext)
    plaintext=str(plaintext).upper()
    plaintext=str(plaintext).replace("J","I")
    groupedWords=[]
    encryptedwords=""


    for i in range(0, len(plaintext), 2):
        letter1=plaintext[i]
        if i+1==len(plaintext):
            letter2='X'
        else:
            letter2=plaintext[i+1]
        if letter1==letter2:
            letter2='X'
        groupedWords.append([letter1,letter2])
    ##encrypt
    for pairs in groupedWords:
        encryptedwords=encryptedwords+""+get_encrypted_pair(pairs,grid,gridList)
    return encryptedwords
    

def get_encrypted_pair(pairs,grid_dictionary, grid_list):
        word1_co_ordinate=grid_dictionary.get(pairs[0])
        word2_co_ordinate=grid_dictionary.get(pairs[1])
        rowWord1=word1_co_ordinate.row
        if rowWord1 is None:
            print(pairs)
        columnWord1=word1_co_ordinate.column
        rowWord2=word2_co_ordinate.row
        if rowWord2 is None:
            print(pairs)
        columnWord2=word2_co_ordinate.column

        encryptedWord1=""
        encryptedWord2=""

        if ((rowWord1==rowWord2) and(columnWord1!=columnWord2)):
            right_column_Word1=columnWord1
            if columnWord1==4:
                right_column_Word1=0
            else :
                right_column_Word1=right_column_Word1+1
            right_column_Word2=columnWord2
            if columnWord2==4:
                right_column_Word2=0
            else :
                right_column_Word2=right_column_Word2+1
            encryptedWord1=grid_list[rowWord1][right_column_Word1]
            encryptedWord2=grid_list[rowWord2][right_column_Word2]

        elif ((columnWord1==columnWord2) and(rowWord1!=rowWord2)):
            down_row_Word1=rowWord1
            if rowWord1==4:
                down_row_Word1=0
            else :
                down_row_Word1=down_row_Word1+1
            down_row_Word2=rowWord2
            if rowWord2==4:
                down_row_Word2=0
            else :
                down_row_Word2=down_row_Word2+1
            encryptedWord1=grid_list[down_row_Word1][columnWord1]
            encryptedWord2=grid_list[down_row_Word2][columnWord1]

        else:
            swapped_column_word1=columnWord2
            swapped_column_word2=columnWord1
            encryptedWord1=grid_list[rowWord1][swapped_column_word1]
            encryptedWord2=grid_list[rowWord2][swapped_column_word2]
        return str(encryptedWord1)+""+str(encryptedWord2)

def get_decrypted_pair(pairs,grid_dictionary, grid_list):
        word1_co_ordinate=grid_dictionary.get(pairs[0])
        word2_co_ordinate=grid_dictionary.get(pairs[1])
        rowWord1=word1_co_ordinate.row
        columnWord1=word1_co_ordinate.column
        rowWord2=word2_co_ordinate.row
        columnWord2=word2_co_ordinate.column

        encryptedWord1=""
        encryptedWord2=""

        if ((rowWord1==rowWord2) and(columnWord1!=columnWord2)):
            right_column_Word1=columnWord1
            if columnWord1==0:
                right_column_Word1=4
            else :
                right_column_Word1=right_column_Word1-1
            right_column_Word2=columnWord2
            if columnWord2==0:
                right_column_Word2=4
            else :
                right_column_Word2=right_column_Word2-1
            encryptedWord1=grid_list[rowWord1][right_column_Word1]
            encryptedWord2=grid_list[rowWord2][right_column_Word2]

        elif ((columnWord1==columnWord2) and(rowWord1!=rowWord2)):
            down_row_Word1=rowWord1
            if rowWord1==0:
                down_row_Word1=4
            else :
                down_row_Word1=down_row_Word1-1
            down_row_Word2=rowWord2
            if rowWord2==0:
                down_row_Word2=4
            else :
                down_row_Word2=down_row_Word2-1
            encryptedWord1=grid_list[down_row_Word1][columnWord1]
            encryptedWord2=grid_list[down_row_Word2][columnWord1]

        else:
            swapped_column_word1=columnWord2
            swapped_column_word2=columnWord1
            encryptedWord1=grid_list[rowWord1][swapped_column_word1]
            encryptedWord2=grid_list[rowWord2][swapped_column_word2]
        return str(encryptedWord1)+""+str(encryptedWord2)   
def decrypt(encrypted_text,grid_dictionary,grid_list):
    encrypted_text=clean_text(encrypted_text)
    encrypted_text=str(encrypted_text).upper()
    groupedWords=[encrypted_text[i:i+2] for i in range(0, len(encrypted_text), 2)]
    decryptedText=""
    for word in groupedWords:
        decryptedText=decryptedText+get_decrypted_pair(word,grid_dictionary,grid_list)
    return decryptedText

def main():
    input_plain_text_reader= open('encryptInput.txt', 'r')    
    lines=input_plain_text_reader.readlines()
    plaintext=""

    for line in lines:
        plaintext=plaintext+str(line)
    
    input_encrypted_text_reader= open('decryptInputPlayFair.txt', 'r')    
    lines=input_encrypted_text_reader.readlines()
    encryptedText=""

    for line in lines:
        encryptedText=encryptedText+str(line)
    
    grid,gridList=generate_grid("RAYQUAZA")
    encryptedTextOutput=encrypt(grid,gridList,plaintext)
    print("encrypted text is "+encryptedTextOutput)
    decryptedText=decrypt(encryptedText,grid,gridList)
    print("decrypted text is "+decryptedText)


if __name__ == "__main__":
    main()
