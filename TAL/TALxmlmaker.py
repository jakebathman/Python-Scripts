from bs4 import BeautifulSoup
import urllib2
import re
import csv
import codecs
import os
import time

lstResults=[["Episode #","Date", "Title", "Description","Link","Notes"]]
lstTmp=[]
notes=""
epnum=499

#look for the latest episode number
print("Latest episode is ."),
for e in xrange(495,496):
    html=urllib2.urlopen("http://www.thisamericanlife.org/radio-archives/episode/" + str(e))
    s=BeautifulSoup(html.read())
    #print(s)
    try:
        if s.find(text=re.compile("PAGE NOT FOUND")) is not None:
            epnum=e-1
            print(str(epnum))
            break
        else:
            print("."),
    except:
        print("."),

st=en=0

skipped=[]

#regex examples: http://flockhart.virtualave.net/RBIF0100/regexp.html

for i in xrange(epnum,0,-1):
    strItem="Item"
    try:
        url = "http://www.thisamericanlife.org/radio-archives/episode/" + str(i) + "/" + str(i)
        html_data = urllib2.urlopen(url)
        soup=BeautifulSoup(html_data.read())
        print("Episode " + str(i) + ":"),
        #print("URL: " + url)
        notes=""
        if soup is not None:
            try:
                epTitle=soup.find(attrs={"property":"twitter:title"})['content']
            except:
                epTitle="##not-found##"
            try:
                epDesc=soup.find(attrs={"name":"description"})['content']
            except:
                epDesc="##not-found##"
            try:
                epLink=soup.find(attrs={"property":"twitter:url"})['content']
            except:
                epLink="##not-found##"

            epTitle=epTitle.encode('ascii','replace')
            epDesc=epDesc.encode('ascii','replace')
            epLink=epLink.encode('ascii','replace')

            for each_div in soup.findAll('div',{'class':'date'}):
                epDate = str(each_div.contents[0])
                epDate=epDate.encode('ascii','replace')

            if ":" in epTitle:
                epTitle = epTitle[len(str(i))+1:].strip()
                epTitle=epTitle.encode('ascii','replace')

            lstTmp=[i,epDate,epTitle,epDesc,epLink,notes]
            lstResults.append(lstTmp)
            print("success!")
            epDate=epTitle=epDesc=""

            if i % 25 == 0:
                print("Outputting to csv as a safety measure")
                fn=os.path.abspath("C:/Users/e008922/Dropbox/_Git/Python-Scripts/TAL/results/TALepisodeoutput.csv")
                with open(fn,'wb') as f:
                    writer = csv.writer(f)
                    writer.writerows(lstResults)
        else:
            epDate=epTitle=epDesc=epLink=""
            notes=notes + " " + "[error?]"
            lstTmp=[i,epDate,epTitle,epDesc,notes]
            lstResults.append(lstTmp)
            print("error?")
    except Exception:
        print("Error: Outputting to csv (then quitting)")
        fn=os.path.abspath("C:/Users/e008922/Dropbox/_Git/Python-Scripts/TAL/results/TALepisodeoutput.csv")
        with open(fn,'wb') as f:
            writer = csv.writer(f)
            writer.writerows(lstResults)
        skipped.append(i)

        for x in xrange(10,0,-1):
            print("Pausing to recover from error..."),
            print(x),
            time.sleep(.5)
            print(" . "),
        print("Trying again!")
        ## Try it again, assuming it was a temporary connection issue
        url = "http://www.thisamericanlife.org/radio-archives/episode/" + str(i) + "/" + str(i)
        html_data = urllib2.urlopen(url)
        soup=BeautifulSoup(html_data.read())
        print("Episode " + str(i) + ":"),
        #print("URL: " + url)
        notes=""
        if soup is not None:
            epTitle=soup.find(attrs={"property":"twitter:title"})['content']
            epDesc=soup.find(attrs={"name":"description"})['content']
            epLink=soup.find(attrs={"property":"twitter:url"})['content']

            epTitle=epTitle.encode('ascii','replace')
            epDesc=epDesc.encode('ascii','replace')
            epLink=epLink.encode('ascii','replace')

            for each_div in soup.findAll('div',{'class':'date'}):
                epDate = str(each_div.contents[0])
                epDate=epDate.encode('ascii','replace')

            if ":" in epTitle:
                epTitle = epTitle[len(str(i))+1:].strip()
                epTitle=epTitle.encode('ascii','replace')

            lstTmp=[i,epDate,epTitle,epDesc,epLink,notes]
            lstResults.append(lstTmp)
            print("success!")
            epDate=epTitle=epDesc=""

            if i % 25 == 0:
                print("Outputting to csv as a safety measure")
                fn=os.path.abspath("C:/Users/e008922/Dropbox/_Git/Python-Scripts/TAL/results/TALepisodeoutput.csv")
                with open(fn,'wb') as f:
                    writer = csv.writer(f)
                    writer.writerows(lstResults)
        else:
            epDate=epTitle=epDesc=epLink=""
            notes=notes + " " + "[error?]"
            lstTmp=[i,epDate,epTitle,epDesc,notes]
            lstResults.append(lstTmp)
            print("error?")



print("These numbers had issues. Make sure they got re-done okay:")
print(skipped)
fn=os.path.abspath("C:/Users/e008922/Dropbox/_Git/Python-Scripts/TAL/results/TALepisodeoutput.csv")
with open(fn,'wb') as f:
    writer = csv.writer(f)
    writer.writerows(lstResults)

execfile("CSVtoXML.py")
    

print("DONE!")




