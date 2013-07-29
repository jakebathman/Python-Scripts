import urllib2, os, time

def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]

tms=[]
c=0
ttime=0
avgt=0
tsize=0

xs=1
xe=0
for i in xrange(xs,xe,-1):
    st = time.time()   
    f=os.path.abspath("C:/Users/e008922/Dropbox/_Git/Python-Scripts/TAL/mp3s/" + str(i) + ".mp3")
    url = "http://audio.thisamericanlife.org/jomamashouse/ismymamashouse/" + str(i) + ".mp3"
    req2 = urllib2.Request(url)
    response = urllib2.urlopen(req2)

    u = urllib2.urlopen(url)
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    fsize=round(file_size/1024/1024.0,1)
    print "Ep #: %s (%s MB)" % (str(i), fsize), 
    tsize+=fsize

    #grab the data
    data = response.read()
    et = time.time()
    ft=round(et - st,0)

    c+=1
    ttime+=ft
    tms.append(ft)
    avgt=median(tms)
    
    tleft=round((i-xe-1)*avgt,0)
    
    if tleft>60:
        tleft = str(round(tleft/60,2)) + " min)"
    else:
        tleft = str(tleft) + " sec)"
    print("(took " + str(ft) + " sec. -- " + str(i-xe) + " left -- " + "done in ~" + tleft)
    
    mp3Name = f
    song = open(mp3Name, "wb")
    song.write(data)    # was data2
    song.close()

print("Done! Total time for " + str(xs-xe) + " files was " + str(round(ttime/60,2)) + " min."),
print("(~" + str(round(tsize/ttime,2)) + " MB/s), or about " + str(round(ttime/xs-xe,2)) + " seconds per file")

