 #-*- coding: utf-8 -*-
import string
import os
import io
#import chardet
import codecs
from cltk.stem.latin.syllabifier import Syllabifier
format=['txt']
counter=0
syllabus = [' ' for i in range (10000)]
word = [' ' for i in range (10000)]

def ChunkLyrics(lyrics, word, list):
    lyrics = lyrics.lower()
    vowel = ['a','e','i','o','u']
    coounter = 0
    sign = 0
    numofSyllabus = 0
    numofWord = 0
    begin = end = 0
    for i in range(1, len(lyrics)):

        if(lyrics[i] == ' '):

            if(begin!=end): #not the first space
                end = i - 1
                word[numofWord] = lyrics[begin:end+1]
                numofWord = numofWord + 1
                begin = i + 1
            else: begin = 1 # skip the first space
    syllabifier = Syllabifier()
    for i in range(numofWord):
        #print (word[i])
        tmp = syllabifier.syllabify(word[i])
        #print (syllabifier.syllabify(word[i]))
        for element in tmp:
            list[numofSyllabus] = element
            numofSyllabus = numofSyllabus + 1








def WriteToFile(originalFname, newFid):
     originalFid = open(originalFname, 'r')

     for line in originalFid.readlines():
         # print line
         newFid.write(line + '\n')
     originalFid.close()


def PrintMeasure(id, newFid):
     # print ("<measure n=\"%i\" >" %id)
     # print ("<staff>\n")
     # print ("<layer>\n")
     newFid.write("\n <measure n=\"%i\" >\n" % id)
     newFid.write("<staff>\n")
     newFid.write("<layer>\n")


def PrintNote(pitchid, octid, newFid, ptr, status, syllabus, ptr2):
     # print ("<note pname=\"%s\" oct=\"%i\" dur=\"4\" stem.dir=\"up\"> </note>" % (pitchid,octid))


         if(status[ptr]=='n'):
             if(len(status)-1>ptr):
                 #print (len(status))
                 #print(ptr)
                 if(status[ptr+1]!='g'):
                    newFid.write("<note pname=\"%s\" oct=\"%i\" dur=\"4\" stem.dir=\"up\"> </note>\n" % (pitchid[ptr], octid[ptr]))
         elif(status[ptr]=='g'): # grace note
            newFid.write("<note pname=\"%s\" grace=\"acc\" oct=\"%i\" dur=\"8\" stem.dir=\"up\"> </note>\n" % (pitchid[ptr-1], octid[ptr]))
         elif(status[ptr]=='l'):
             if(len(status)-1>ptr):
                newFid.write("<note pname=\"%s\" oct=\"%i\" dur=\"4\" stem.dir=\"up\">\n " % (pitchid[ptr+1], octid[ptr]))
                newFid.write("<verse n=\"1\">\n")
                newFid.write("<syl>%s</syl>\n" % syllabus[ptr2])
             #ptr2 = ptr2 + 1
             #ptr = ptr + 1
                newFid.write("</verse>\n")
                newFid.write("</note>\n")
         #return (ptr, ptr2)

'''def SearchMode(mode):
     if (mode == '1' or mode == '2'):
         return Dor
     elif (mode == '3' or mode == '4'):
         return Phr
     elif (mode == '5' or mode == '6'):
         return Lyd
     elif (mode == '7' or mode == '8'):
         return Mix'''


def NumToPitchClassWithOct(num, mode, final, oct):
     Dict = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
     # mod = SearchMode(mode)

     for ptr in range(len(num)):
         for i in range(7):
             if (final == Dict[i]):
                 break
         if (num[ptr] == '>'):
             num = num[0:ptr] + '3' + num[ptr + 1:]

             oct[ptr] = oct[ptr] + 1
         elif (num[ptr] == '-'):
             num = num[0:ptr] + '6' + num[ptr + 1:]

             oct[ptr] = oct[ptr] - 1
         elif (num[ptr] == '0'):
             num = num[0:ptr] + '7' + num[ptr + 1:]

             oct[ptr] = oct[ptr] - 1
         elif (num[ptr] == '*'):
             num = num[0:ptr] + '5' + num[ptr + 1:]

             oct[ptr] = oct[ptr] - 1

         elif (num[ptr] == '%'):
             num = num[0:ptr] + '4' + num[ptr + 1:]

             oct[ptr] = oct[ptr] - 1
         elif (num[ptr] == '='):
             num = num[0:ptr] + num[ptr - 1] + num[ptr + 1:]
             oct[ptr] = oct[ptr - 1]
             # debug
             # elif (num[ptr] == ','):
             # status[ptr - 1] = 'g'  # the last note is grace note
         if (num[ptr].isdigit()):
             m = int(num[ptr])
             ii = i
             for j in range(m - 1):
                 i = i + 1
                 ii = ii + 1
                 if (ii >= 7):
                     oct[ptr] = oct[ptr] + 1
                     ii = ii % 7
                 i = i % 7
             num = num[0:ptr] + Dict[i] + num[ptr + 1:]
     return (num, oct)
def MelodyLineToMEIFunc(melody, input, newFid, syllabus):

    ptr = 0
    mode = input[0]
    final = input[1]


    length = len(melody)
    PitchClass = [' ' for i in range (len(melody))]
    Oct = [4 for i in range (len(melody))]

    status = [' ' for i in range (len(melody))]  # 0 for grace note
    WriteToFile(r'/Users/yaolongju/Nutstore/Codes/Parser for medieval chants/TemplateHead.txt',newFid)
    for i in range (length):
        if (melody[i] == ','):
            status[i] = 'g'
        elif(melody[i] == '.'):
            status[i] = 'l'
        else:
            status[i] = 'n'

    #melody = melody.replace(".", '')
    #melody = melody.replace(",", '')
    (melody, Oct) = NumToPitchClassWithOct(melody, mode, final, Oct)
    i = 0
    while(i<length):

        if(i%4==0 and i!=0):# wrong, bug
            print ("</measure>")
            newFid.write("</layer>\n")
            newFid.write("</staff>\n")
            newFid.write("</measure>\n")


            PrintMeasure(i/4+1, newFid)
        elif(i%4==0):
            PrintMeasure(i/4 + 1, newFid)
        #print melody[i]
        #print NumToPitchClassWithOct(melody[i], mode, final, oct)

        PrintNote(melody, Oct, newFid, i, status, syllabus, ptr)
        if(status[i]=='l'):
            i = i + 1
            ptr = ptr + 1
        i = i + 1
    #print "</measure>"
    newFid.write("</layer>\n")
    newFid.write("</staff>\n")
    newFid.write("</measure>\n")


    WriteToFile(r'/Users/yaolongju/Nutstore/Codes/Parser for medieval chants/TemplateButtom.txt',newFid)

    #print PitchClass
    #print Oct
    #measure = length/4+1
    #print measure
    #os.system("pause")
for filex in os.listdir('.'):
    if os.path.isfile(filex) and (os.path.splitext(filex)[1][1:].lower() in format)== True:
        print (filex)
        mark=0 # not find a head yet
        f1=open(filex,'r', encoding='iso8859') # encode with extended ASCII (256)
        for blank in f1.readlines():
            #print (type(blank))
            #blank = bytes(blank, 'utf-8')
            print (blank)
           # blank = blank.decode("iso8859")
            if((blank.find('[File')!=-1 or blank.find('[file')!=-1) and mark==0):

                print (blank) #show all the volumes
                ptr=blank.find('CH-')
                #blankT=blank.decode("ascii").encode("utf-8")

                #print chardet.detect(blank)
                if(os.path.exists(blank[ptr:-2])==False):
                    os.mkdir(blank[ptr:-2])# create the folder for each volume
                os.chdir(blank[ptr:-2])# go into that folder
                mark=1 # write volumn file
                continue # read next line
            elif(blank.find('|.')==-1 and mark==1): # Not saint yet, it will be head instructions, save it into file

                fI=codecs.open('instructions.txt','a+','utf-8')


                print (blank)

                fI.write(blank)

            elif(mark==1 and (blank.find('=')==-1 or blank.find('70=XCX')!=-1 or blank.find('8=0504')!=-1 or (blank.find('(')!=-1 and blank.find(')')!=-1) or blank.find('[Advent')!=-1) and blank.find('|.')!=-1): # find a saint, continue to create folder for that saint
                print (blank)
                fI.close()
                ptr=blank.find('|.')
                if(os.path.exists(blank[ptr+2:-2])==False):
                    os.mkdir(blank[ptr+2:-2])# create the folder for each volume
                os.chdir(blank[ptr+2:-2])# go into that folder
                mark=2 # write saint file
                continue
            elif(mark==2 and blank.find('|.')==-1):

                fI=codecs.open('instructions.txt','a+','utf-8')

                print (blank)
                print(blank, file=fI)
            elif(mark==2 and blank.find('=')!=-1 and blank.find('|.')!=-1): #saint's name=letter
                print (blank)
                fI.close()
                blank=blank.replace('"','-')

                ptr=blank.find('|.')

                if(os.path.exists(blank[ptr+2:-2])==False):
                    os.mkdir(blank[ptr+2:-2])# create the folder for each volume
                os.chdir(blank[ptr+2:-2])# go into that folder

                mark=3 # write saint= letter head file
                continue
            elif(mark==3 and blank.find('|g')==-1):
                fI=codecs.open('instructions.txt','a+','utf-8')


                print (blank)

                fI.write(blank)
            elif(mark==3 and blank.find('|g')!=-1):
                if (blank.find('|g')!=-1): # find the individual song
                    if(counter != 0): fmei.close()
                    ptr2=blank.find('.')
                    mode=blank[ptr2+1:ptr2+3]
                    ptr=blank.find('|g')
                    blank=blank.replace('?','-')
                    counter = counter + 1 # num of songs
                    print (counter)
                    fsong=codecs.open(blank[ptr+1:-2]+'.txt','a+','utf-8')
                    fmei=codecs.open(blank[ptr+1:-2]+'.mei','a+','utf-8')
                    print (blank)
                    print(blank, file=fsong)


                    mark=4 # write individual song
                    continue
            elif(blank.find('|.')==-1 and blank.find('[File')==-1 and blank.find('[file')==-1 and blank.find('|g')==-1 and mark==4): #write lines into a txt file
                print (blank)
                print(blank, file=fsong)
                if (blank[0:2] == '\ '):  # this is melody with lyric line

                    blank = blank.replace("'", ' ')
                    blank = blank.replace('\\', '')

                    blank = blank.replace('#', '')
                    blank = blank.replace('(', '')
                    blank = blank.replace(')', '')


                    blank = blank.replace('\r', '')
                    blank = blank.replace('\n', '')
                    blank = blank.replace('?', '')
                    blank = blank.replace('+', '')
                    blank = blank.replace('v', '')
                    for i in range(len(blank)):
                        if(blank[i].isalpha()):
                            blank = blank.replace(blank[i],' ')
                    blank = blank.replace(' ', '')
                    blank = blank.replace(';', '')
                    blank = blank.replace('$', '')
                    blank = blank.replace('^', '')
                    blank = blank.replace('!', '')
                    print(('melody'+blank))

                    MelodyLineToMEIFunc(blank, mode, fmei, syllabus)#blank2 = blank.replace('.', '')  # melody with syllabus sign
                    #blank = blank.replace(',', '')
                elif(blank[0:2]=='/ '): # lyric line
                    for i in range(len(blank)):
                         if((blank[i].isalpha() or blank[i] == ' ')==False):
                             blank = blank.replace(blank[i],' ')
                    print(("lyric" + blank))
                    ChunkLyrics(blank, word, syllabus)
                    '''
                    '''




            elif(mark==4):

                    if(blank.find('[File')!=-1 or blank.find('[file')!=-1):
                         # find a volume
                        print (blank) #show all the volumes
                        ptr=blank.find('CH-')
                        #blankT=blank.decode("ascii").encode("utf-8")

                        #print chardet.detect(blank)
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                        if(os.path.exists(blank[ptr:-2])==False):
                            os.mkdir(blank[ptr:-2])# create the folder for each volume
                        os.chdir(blank[ptr:-2])# go into that folder
                        mark=1
                        continue # read next line
                    elif((blank.find('=')==-1 or blank.find('70=XCX')!=-1 or blank.find('8=0504')!=-1 or (blank.find('(')!=-1 and blank.find(')')!=-1) or blank.find('[Advent')!=-1) and blank.find('|.')!=-1): # Not saint yet, it will be head instructions, save it into file
                        print (blank)
                        ptr=blank.find('|.')
                        os.chdir(os.pardir)
                        os.chdir(os.pardir)
                        blank=blank.replace('\t','-')
                        blank=blank.replace('"','-')
                        if(os.path.exists(blank[ptr+2:-2])==False):
                            os.mkdir(blank[ptr+2:-2])# create the folder for each volume
                        os.chdir(blank[ptr+2:-2])# go into that folder
                        mark=2 # write saint file
                        continue


                    elif(blank.find('|.')!=-1 and blank.find('=')!=-1): #saint's name=letter
                        print (blank)
                        ptr=blank.find('|.')
                        blank=blank.replace('?','-')
                        blank=blank.replace('/','-')
                        blank=blank.replace('"','-')
                        os.chdir(os.pardir)
                        if(os.path.exists(blank[ptr+2:-2])==False):
                            os.mkdir(blank[ptr+2:-2])# create the folder for each volume
                        os.chdir(blank[ptr+2:-2])# go into that folder
                        mark=3 # write saint= letter head file
                        continue
                        #print type(blank)
                        #print unicode(blank)
                        #os.mkdir(blank)'''
                    elif(blank.find('|g')!=-1):
                        if (counter != 0): fmei.close()
                        ptr=blank.find('|g')
                        blank=blank.replace('?','-')
                        blank=blank.replace('/','-')
                        counter = counter + 1 # num of songs
                        print (counter)
                        fsong=codecs.open(blank[ptr+1:-2]+'.txt','a+','utf-8')
                        fmei = codecs.open(blank[ptr + 1:-2] + '.mei', 'a+', 'utf-8')
                        print (blank)
                        print(blank, file=fsong)
                        mark=4 # write individual song
                        continue
