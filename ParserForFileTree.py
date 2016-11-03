# -*- coding: utf-8 -*-
import string
import os
import io
#import chardet
import codecs
format=['txt']
for filex in os.listdir('.'):
    if os.path.isfile(filex) and (os.path.splitext(filex)[1][1:].lower() in format)== True:
        print filex
        mark=0 # not find a head yet
        f1=open(filex,'r') # encode with extended ASCII (256)
        for blank in f1.readlines():
            blank = blank.decode("iso8859")
            if((blank.find('[File')!=-1 or blank.find('[file')!=-1) and mark==0):

                print blank #show all the volumes
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


                print blank

                fI.write(blank)

            elif(mark==1 and (blank.find('=')==-1 or blank.find('70=XCX')!=-1 or blank.find('8=0504')!=-1 or (blank.find('(')!=-1 and blank.find(')')!=-1) or blank.find('[Advent')!=-1) and blank.find('|.')!=-1): # find a saint, continue to create folder for that saint
                print blank
                fI.close()
                ptr=blank.find('|.')
                if(os.path.exists(blank[ptr+2:-2])==False):
                    os.mkdir(blank[ptr+2:-2])# create the folder for each volume
                os.chdir(blank[ptr+2:-2])# go into that folder
                mark=2 # write saint file
                continue
            elif(mark==2 and blank.find('|.')==-1):

                fI=codecs.open('instructions.txt','a+','utf-8')

                print blank
                print >> fI, blank
            elif(mark==2 and blank.find('=')!=-1 and blank.find('|.')!=-1): #saint's name=letter
                print blank
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


                print blank

                fI.write(blank)
            elif(mark==3 and blank.find('|g')!=-1):
                if (blank.find('|g')!=-1): # find the individual song

                    ptr=blank.find('|g')
                    blank=blank.replace('?','-')
                    fsong=codecs.open(blank[ptr+1:-2]+'.txt','a+','utf-8')
                    print blank
                    print >> fsong, blank
                    mark=4 # write individual song
                    continue
            elif(blank.find('|.')==-1 and blank.find('[File')==-1 and blank.find('[file')==-1 and blank.find('|g')==-1 and mark==4):
                print blank
                print >> fsong, blank
            elif(mark==4):

                    if(blank.find('[File')!=-1 or blank.find('[file')!=-1):
                         # find a volume
                        print blank #show all the volumes
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
                        print blank
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
                        print blank
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
                        ptr=blank.find('|g')
                        blank=blank.replace('?','-')
                        blank=blank.replace('/','-')
                        fsong=codecs.open(blank[ptr+1:-2]+'.txt','a+','utf-8')
                        print blank
                        print >> fsong, blank
                        mark=4 # write individual song
                        continue
