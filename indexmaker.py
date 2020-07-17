import nltk
from nltk.chunk import tree2conlltags
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import Tree
from nltk.corpus import brown
import collections
import string
import ast

def taggingparsed(page_array):
    output=[]
    out=[]

    for page in page_array:
        tokened_text=nltk.word_tokenize(str(page[1]))
        tagged_text=nltk.pos_tag(tokened_text)

        tree=ne_chunk((tagged_text))

        grammar=r"""
            NP:{<JJ>*<NN>}
               {<NNP>+}
               {<PERSON>}
        """

        cp=nltk.RegexpParser(grammar)
        result=cp.parse(tree)

        for s in result:
            if (type(s) == Tree and s.label() == 'NP'):
                output.append([str(s),page[0]])
          
    return output


def occurrencecount(dic):
    d=collections.defaultdict(list)
    arr=[]
    wrd=""
    for k,v in dic:
        d[k].append(v)

    #print(d[k][1])

    #print(str(d[2][1]))
    
    for k in d:
        t=Tree.fromstring(k)
        for x in t.leaves():
                word=nltk.tag.str2tuple(x)
                wrd=wrd+" "+word[0]

        arr.append([wrd,d[k]])
        wrd=""

    return arr

def namecount(dic):
    d=collections.defaultdict(list)
    arr=[]
    wrd=""

    for k,v in dic:
        t=Tree.fromstring(k)
        for x in t.subtrees():
            if x.label()=="PERSON":
                d[k].append(v)
              #  print("i appended "+k)
                
    for k in d:
        arr.append([k,d[k]])
        
    for x in arr:
        t=Tree.fromstring(x[0])
        for y in t.subtrees():
            
            if y.label()=="PERSON":
                for z in t.leaves():
                    word=nltk.tag.str2tuple(z)
                    wrd=wrd+" "+word[0]
                    
                    x[0]=wrd
                    
                wrd=""    

    names=arr

    new_array=[]
    newer_array=[]
    even_newer_array=[]
    names.sort(key=lambda x:x[0])

    for i in names: 
        i[0]=i[0].lower()
        i[0]=i[0].lstrip()
        #print(str(i[0]))
        if(i[0][0].isalpha()):
            new_array.append(i)
           # print("i get here")

      
    for i in new_array:
        appendedthis=0
        if(i[0].isalpha() and len(i[0])>3):
            for j in new_array:
                if(not j[0].isalpha()):
                    if j[0].find(i[0])!=-1:
                        newer_array.append([i[0], [i,j]])
                        appendedthis=1
                        
        if(appendedthis==0 and i[0].isalpha() and len(i[0])>3):
            newer_array.append([i[0],[i]]) #was just append(i)


    return newer_array
    

def textparser(text, start, end):
    pages=[]
    left=0
    for x in range(start,end):
        page_begin=text.find(str(x),left)
        page_end=text.find(str(x+1), page_begin)
        page=text[page_begin:page_end]
        page.replace("'",'"')
        pages.append([x,page])
        left=page_end

    return pages                
        
def nicepres(array):
    #print(str(array))
    new_array=[]
    array.sort(key=lambda x:x[0])

    for i in array: 
        i[0]=i[0].lower()
        i[0]=i[0].lstrip()
        #print(str(i[0]))
        if(i[0][0].isalpha()):
            new_array.append(i)
           # print("i get here")
  
    return new_array

def duplicates(array):

  #  for x in range(0,8):
   #     print(array[x])
    array.sort(key=lambda x:x[0])
    
    new_array=[]
    d=collections.defaultdict(list)
    for k in array:
        d[k[0]].append(k[1])
        if(k[0]=="concept"):
            print("added concept!")
       # print("added k "+k[0])

    for k in d:
        if(k=="concept"):
            print(str(d[k]))
        new_array.append([k,d[k]])
            
    return new_array
        
        
def categorize_nouns(array):
  #  f2=open("ooo_at.txt","w")
    d=collections.defaultdict(list)
    word=""
    new_array=[]
    toggle=0
    
    for j in array:
        s=j[0]
        if(word!=""):
            if(s.find(word)!=-1):
               if(toggle==0):
                 #  print(word)
                  # print("----")
                   toggle=1
               #print(j)
               d[word].append(j)

            else:
                d[s].append(j)
               
        else:
                d[s].append(j)
        if(not s.isalpha()):
            try:
                word_new=s[0:s.index(" ")]
                if(word_new==word):
                    toggle=1
                else:
                    toggle=0
                    #new_array.append(word_new)
                word=word_new
                
            except:
                word=""
    for k in d:
        if(len(d[k])>7):
            new_array.append([k,d[k]])

    return new_array
    #f2.write(str(new_array))        

def categorize_adjs(array):
    d=collections.defaultdict(list)
    in_arr=[]
    noun=""
    new_array=[]
    for i in array:
        s=i[0]
        if(not s.isalpha()):
                try:
                    noun=s[s.index(" ")+1:len(s)]
                    if(not noun.isalpha()):
                        noun=noun[noun.index(" ")+1:len(noun)]
                    if(not len(noun)>4):
                        noun=""
                
                       
                
                except:
                    pass
                else:
                    for j in array:
                        if(noun!="" and noun!=j[0] and not j in d[noun]):
                            if j[0].find(noun)!=-1:
                                d[noun].append(j)
                             #   print(str(noun)+": "+str(j))
        
    for k in d:
        if(len(d[k])>7):
            new_array.append([k,d[k]])

    return new_array
            
def searchfor(text, terms):
    outarray=[]
    pagearray=[]
    for term in terms:
        for pages in text:
            if str(pages[1]).find(term)!=-1:
                pagearray.append(pages[0])
        outarray.append([term,pagearray])
        pagearray=[]

    return outarray
        
        
def philpapers(array):
    ppfile=open("texts/philpapersencore.txt","r")
    a=json.loads(ppfile.read())
    arr=[]
    d=collections.defaultdict(list)

    for i in array:
    
        for j in a:
            if i[0].find(str(j))!=-1:
                d[j].append(i)

    for i in d:
            arr.append([i,d[i]])
    
    return arr

def categorizeav(array):
    arr=[]
    sifted_arr=[]
    news_text = brown.words(categories='news')
    fdist = nltk.FreqDist(w.lower() for w in news_text)
    adj_classtext=categorize_adjs(array)
       
    n_classtext=categorize_nouns(array)

    arr=adj_classtext+n_classtext
    
    for i in arr:
        if (fdist[i[0]]<18 and len(i[0])>2):
            sifted_arr.append(i)

    return(sifted_arr)

def indexprint(array):
    #f_js=open("index.js","w")
    array.sort(key=lambda x:x[0])
    #f_js.write("var index="+str(array))
    
    
    string=""
    for i in array:
       # print(i[0].upper())
        string=string+i[0].upper()+"\n"
        for z in i[1]:
            if(type(z)==list and len(z)>1 and len(z[0])>1):
             #   print(str(z[0])+":", end=' ')
                string=string+str(z[0])+": "
                for x in z[1]:
                    if(type(x)==list):
                        for b in x:
                        #    print(str(b)+",", end='')
                            string=string+str(b)+","
                    else:
                     #   print(str(x)+",",end='')
                        string=string+str(x)+","
               # print('\n')
                string=string+"\n"
            #else:
              #  print(str(z))
              #  print("\n")
             #   string=string+str(z)
        string=string+"\n"

    return array    


def quick_make(file, range):
    inputfile=open(file,"r")
    indexfile=open("index.js","w")
    textfile=open("text.js","w")
    parsedtext=textparser(inputfile.read(),range[0],range[1])

    print("Tagging text. This might take a minute...")
    taggedparsedtext=taggingparsed(parsedtext)


    textfile.write("var text_file="+str(parsedtext).lower())

    print("Wrote the text file to text.js")

    nametext=namecount(taggedparsedtext)
    otptext=occurrencecount(taggedparsedtext)

    otptext=nicepres(otptext)
    nametext=nicepres(nametext)
    cat=categorizeav(otptext)

    #need to add the categorize function here
    total_index=cat+nametext

    total_index.sort(key=lambda x:x[0])

    index_string="var index="+str(total_index)

    indexfile.write(index_string)
    print("Wrote the index to index.js. Now you can open edit.html to, well, edit")
    
    

