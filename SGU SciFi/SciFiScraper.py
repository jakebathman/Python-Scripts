from bs4 import BeautifulSoup
import urllib2
import re
import csv
import os

lstResults=[["Episode #","Item 1", "Item 2", "Item 3", "Item 4", "Item 5","Notes"]]
lstTmp=[]
notes=""

#look for the latest episode number
print("Latest episode is ."),
for e in xrange(405,1000):
    html=urllib2.urlopen("http://www.theskepticsguide.org/archive/podcastinfo.aspx?mid=1&pid=" + str(e))
    s=BeautifulSoup(html.read())
    #print(s)
    try:
        if s.find(text=re.compile("Oops!")) is not None:
            epnum=e-1
            print(str(epnum))
            break
        else:
            print("."),
    except:
        print("."),

st=en=0
if epnum>200:
    pts=2
else:
    pts=1
#regex examples: http://flockhart.virtualave.net/RBIF0100/regexp.html
for j in xrange(1,pts+1):
    lstResults=[]
    print("Parts: " + str(pts))
    print("j:     " + str(j))
    if pts==2 and j==1:
        st=epnum
        en=200
    elif pts==2 and j>1:
        st=200
        en=0
    elif pts==1:
        st=epnum
        en=1

    #Override start/end
    #st=250
    #en=200
    #pts=1
    print("Start: " + str(st))
    print("End:   " + str(en))
    for i in xrange(st,en,-1):
        strItem="Item"
        url = "http://www.theskepticsguide.org/archive/podcastinfo.aspx?mid=1&pid=" + str(i)
        html_data = urllib2.urlopen(url)
        soup=BeautifulSoup(html_data.read())
        print("Episode " + str(i) + ":"),
        #print("URL: " + url)
        scifisegtest=soup.find(text=re.compile("Segment:.*Science or Fiction"))
        #print(scifisegtest)
        notes=""
        if scifisegtest is not None:
            scifiseg=soup.find(text=re.compile("Segment:.*Science or Fiction")).parent.next_sibling
            if scifiseg.find_next(text=re.compile("Question.?#")) is not None:
                strItem="Question"
            elif scifiseg.find_next(text=re.compile("Item.?#")) is not None:
                strItem="Item"
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

                try:    
                    item6 = item5.find_next(text=re.compile(strItem + ".?#"))
                    ans6 = item6.parent.find_next("img").string.strip()
                    notes=notes + " " + "[more items?]"
                except:
                    ans5=""
                    
                lstTmp=[i,ans1,ans2,ans3,ans4,ans5,notes]
                lstResults.append(lstTmp)
                print("success!")
                ans1=ans2=ans3=ans4=ans5=""
            else:
                ans1=ans2=ans3=ans4=ans5=ans6=""
                notes=notes + " " + "[website error?]"
                lstTmp=[i,ans1,ans2,ans3,ans4,ans5,notes]
                lstResults.append(lstTmp)
                print("success! (website error?)")
        else:
            ans1=ans2=ans3=ans4=ans5=ans6=""
            notes=notes + " " + "[missing S/F?]"
            lstTmp=[i,ans1,ans2,ans3,ans4,ans5,notes]
            lstResults.append(lstTmp)
            print("success! (missing S/F?)")

    print(lstResults)
    fn=os.path.abspath("C:/Users/e008922/Dropbox/_Git/Python-Scripts/SGU SciFi/results/output_ep" + str(st) + "_to_ep" + str(en) + ".csv")
    with open(fn,'wb') as f:
        writer = csv.writer(f)
        writer.writerows(lstResults)

print("DONE!")





