import re

def generate_grid(plain_text,max_columns):
    rows=[[]]
    plain_text=plain_text.replace(" ","%")
    rows=[[*str(plain_text[i:i+max_columns])] for i in range(0, len(plain_text), max_columns)]
    return rows

def clean_text(text):

    pattern = r'[^\w\s]'
    return re.sub(pattern, '', text)

def encrypt(plaintext,key):
    grid=generate_grid(clean_text(plaintext.replace('\n', ' ')),max(key))
    encryptedText=""
    for currentKey in key:
        currentIndex=currentKey-1
        for i in range(0,len(grid),1):
            if (len(grid[i])-1)<currentIndex:
                encryptedText=encryptedText+"%"
            else:
                encryptedText=encryptedText+str(grid[i][currentIndex])
    return (encryptedText)
def decrypt(plaintext,key):
    max_columns=max(key)
    max_rows=len(plaintext)/max_columns
    grid=generate_grid(plaintext,int(max_rows))
    
    cols={}
    i=0
    for currentKey in key:
        currentIndex=currentKey-1
        
        cols[currentIndex]=grid[i]
        i=i+1
    colsList=[]
    for k in sorted(cols): 
        colsList.append(cols[k])
        i=i+1
    colsList=transpose_matrix(colsList)



    ans=""
    for j in range(0,len(colsList),1):
        for k in range(0,len(colsList[j]),1):
            ans=ans+str(colsList[j][k])
    return ans.replace("%"," ")

def transpose_matrix(input):
    result = [[input[j][i] for j in range(len(input))] for i in range(len(input[0]))]
    return result

def main():
    
    key=[3,9,4,6,1,7,2,8,5,10]
    input_plain_text_reader= open('encryptInput.txt', 'r')    
    lines=input_plain_text_reader.readlines()
    plainText=""
    for line in lines:
        plainText=plainText+str(line)
    print("plain text is "+plainText)
    encryptedText_output=encrypt(plainText,key)

    input_encrypted_text_reader= open('decryptInputTransposition.txt', 'r') 
    lines=input_encrypted_text_reader.readlines()
    encryptedText=""
    for line in lines:
        encryptedText=encryptedText+str(line)


    print("encrypted text is "+encryptedText_output)
    decrypted_text=decrypt(encryptedText,key)
    print("decrypted text is "+decrypted_text)



if __name__ == "__main__":
    main()


