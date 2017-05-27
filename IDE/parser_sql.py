import fileinput
import datetime
import time
import sqlparse

filename = 'texto.txt'
with open(filename) as f:
    data = f.readlines()

ts=time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
dicc=open("diccionario.txt","a+") #"a+"

for n, sql in enumerate(data, 1): # read the entire text
    sql = sql.rstrip()
    parsed = sqlparse.parse(sql)
    stmt = parsed[0]
    
    if str(stmt.tokens[0]) == "CREATE":
        number_tokens = 4 # 
        nombre =str(stmt.tokens[4]) 
        f=open("data/"+nombre+".txt","a+") #"a+"
        f.close
        lines = len((str(stmt.tokens[4]).rstrip()))
        lines = '{'+(str(stmt.tokens[4]))+' '*(25-lines)+'}'+" "
        dicc.write(lines)
        myString = (str(stmt.tokens[6]))
        
        number_columns = (myString.count(' ')+1)/2;
        for i in range(0,number_columns):
            index = myString.index('{')
            index2 = myString.index('}')
            name_column = myString[index+1:index2]
            index3 = myString.index('[')
            index4 = myString.index(']')
            type_column = myString[index3+1:index4]
            myString = myString[index4+3:] # +3 cuz +1 is the next char y +2 the comma and space 
            lenght3 = len(name_column)
            line3 = '['+name_column+' '*(20-lenght3)+']'
            lenght4 = len(type_column)
            line4 = '['+type_column+' '*(11-lenght4)+']'+" "
            dicc.write(line3+line4)
        dicc.write("["+st+"]"+"#\n")
        
    if str(stmt.tokens[0]) == "INSERT":
        filename2 = 'diccionario.txt'
        with open(filename2) as ff:
            data2 = ff.readlines()
        data22 = str(data2)
        number_lines_text = data22.count('{')
        # print data22

        for i in range(0,number_lines_text):
            index33 = data22.index('{')
            index44 = data22.index('}')
            index_opc = data22.index('#')
            name_table = data22[index33+1:index44]
            data100 = data22
            data22 = data22[index_opc+1:]
            name_table = name_table.replace(" ", "")
            

            # only compare if the fields and names are the same
            # we don't compare if the id is the same is repeated or is incremental, maybe save in diccionary a field with id and his actual id,

            if name_table == (str(stmt.tokens[4])):
                # print name_table
                number_fields_diccionary = data100[index33:index_opc].count('][')
                number_fields_query = (str(stmt.tokens[8])).count(',')
                if number_fields_diccionary==number_fields_query: # we don't compare the right fields (ex. int with int, char with char ) only the # of fields
                    f=open("data/"+name_table+".txt","a+") #"a+"
                    data = (str(stmt.tokens[8]))
                    for j in range(0,number_fields_diccionary):
                        # print data
                        index98 = data.index('(')
                        index99 = data.index(',')
                        data2 = data
                        data = data[index98+1:index99]
                        fff=open("data/"+name_table+".txt","a+") #"a+"
                        large = len(data)
                        fff.write('{'+data+'}'+' '*(15-large)+" ")
                        data = data2[index98:index98+1]+data2[index99+1:]
                    fff.write("\n")
                    fff.close()
    if str(stmt.tokens[0]) == "DELETE":

        index333 = (str(stmt)).index("FROM")        
        if index333==7:
            index444 = (str(stmt)).index("WHERE")
            name_table = (str(stmt))[index333+5:index444-1]
            rest_string = (str(stmt))[index444+6:]
            number_braces = (str(stmt)).count('(')

            if number_braces==1:
                index555 = (str(stmt)).index("(")
                index777 = (str(stmt)).index(")")
                cut_string = (str(stmt))[index555+1:index777]
                
                index888 = (str(stmt)).index("=")
                name_column = (str(stmt))[index555+1:index888]
                value = (str(stmt))[index888+1:-1]

                # for line in fileinput.input("data/"+name_table+".txt", inplace=True): 
                #     print line.replace(value, '0').rstrip()

                filename = "data/"+name_table+".txt"
                with open(filename, 'r') as fin:
                    lines = fin.readlines()
                with open(filename, 'w') as fout:
                    for line in lines:
                        if str(value) not in line:
                            fout.write(line)

            elif number_braces>1: # we don't make the case: "WHERE id=1 AND nombre="renato"" not yet, but in the future 
                print " "

        elif index333==9: # the other case if it is * , DELETE all the register in table
            index444 = (str(stmt)).index("#")
            name_table = (str(stmt))[index333+5:index444-1]
            # print name_table
            create_new_file = open("data/"+name_table+".txt","w") # to delete all the data in the table or .txt
