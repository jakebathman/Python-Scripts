from bs4 import BeautifulSoup
import urllib2
import re
import csv
import os

#Or retrieve it from the web, etc. 
url = "http://www.theskepticsguide.org/archive/podcastinfo.aspx?mid=1&pid=397"
html_data = urllib2.urlopen(url)
soup=BeautifulSoup(html_data.read())

lstResults=[["Episode #","Item 1", "Item 2", "Item 3", "Item 4", "Item 5","Notes"]]
lstTmp=[]



#regex examples: http://flockhart.virtualave.net/RBIF0100/regexp.html
for i in xrange(410,1,-1):
    strItem="Item"
    url = "http://www.theskepticsguide.org/archive/podcastinfo.aspx?mid=1&pid=" + str(i)
    html_data = urllib2.urlopen(url)
    soup=BeautifulSoup(html_data.read())
    print("Episode " + str(i) + ":"),
    #print("URL: " + url)
    scifisegtest=soup.find(text=re.compile("Segment:.*Science or Fiction"))
    #print(scifisegtest)
    if scifisegtest is not None:     
        scifiseg=soup.find(text=re.compile("Segment:.*Science or Fiction")).parent.next_sibling
        if scifiseg.find_next(text=re.compile("Item.?#")) is not None:
            strItem="Item"
        elif scifiseg.find_next(text=re.compile("Question.?#")) is not None:
            strItem="Question"
        else:
            strItem="None"
        if strItem is not "None":
            try:
                item1 = scifiseg.find_next(text=re.compile(strItem + ".?#"))
                ans1= item1.find_next("img").string.strip()
            except:
                ans1=""

            try:
                item2 = item1.find_next(text=re.compile(strItem + ".?#"))
                ans2= item2.find_next("img").string.strip()
            except:
                ans2=""
            
            try:
                item3 = item2.find_next(text=re.compile(strItem + ".?#"))
                ans3= item3.find_next("img").string.strip()
            except:
                ans3=""

            try:
                item4 = item3.find_next(text=re.compile(strItem + ".?#"))
                ans4 = item4.parent.find_next("img").string.strip()
            except:
                ans4=""
            try:
                item5 = item4.find_next(text=re.compile(strItem + ".?#"))
                ans5 = item5.parent.find_next("img").string.strip()
            except:
                ans5=""
                
            lstTmp=[i,ans1,ans2,ans3,ans4,ans5]
            lstResults.append(lstTmp)
            print("success!")
            ans1=ans2=ans3=ans4=ans5=""
        else:
            ans1=ans2=ans3=ans4=ans5=""
            lstTmp=[i,ans1,ans2,ans3,ans4,ans5,"website error?"]
            lstResults.append(lstTmp)
            print("success! (website error?)")
    else:
        ans1=ans2=ans3=ans4=ans5=""
        lstTmp=[i,ans1,ans2,ans3,ans4,ans5,"missing S/F?"]
        lstResults.append(lstTmp)
        print("success! (missing S/F?)")

    
print(lstResults)
fn=os.path.abspath("C:/Users/e008922/Dropbox/_Git/Python-Scripts/SGU SciFi/results/output.csv")
with open(fn,'wb') as f:
    writer = csv.writer(f)
    writer.writerows(lstResults)

print("DONE!")

#for tag in soup.find_all("tr"):
#    print(tag.name)

#Create the soup object from the HTML data
#fooId = soup.find('tr',name='fooId',type='hidden') #Find the proper tag
#value = fooId.attrs[2][1] #The value of the third attribute of the desired tag 
                          #or index it directly via fooId['value']
