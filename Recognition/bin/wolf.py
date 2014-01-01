#!/usr/bin/env python


import lispeak,sys,urllib2

from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "pod":
            self.podIndex = self.podIndex + 1
        elif tag == "plaintext":
            if self.podIndex == 2 and self.go == True:
                self.next = True
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        if self.next == True:
            self.output = data
            self.next = False
            self.go = False

try:
    appid = lispeak.getInfo()['WAKEY']
except:
    appid = ""
if appid != "":
    q = sys.argv[1]
    response = urllib2.urlopen("http://api.wolframalpha.com/v1/query?input="+q.replace(" ","%20")+"&appid="+appid)

    html = response.read() 
    data = open("data.html",'w')
    data.write(html)
    data.close()
    parser = MyHTMLParser()
    parser.podIndex = 0
    parser.go = True
    parser.next = False
    parser.feed(html)

    try:
        output = parser.output
        try:
            out = output.split("\n")
            output = ""
            for l in out:
                l = l.split("|")
                output = output + l[0].title()+": "+l[1] + "\n"
            output = output[:-2]
        except:
            output = parser.output
    except:
        output = "Command Not Found"
else:
    output = "Command Not Found"
print "OUTPUT:"+output
lispeak.displayNotification(output)
