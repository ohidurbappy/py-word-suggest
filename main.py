import http.server
from urllib.parse import urlparse,parse_qs
import socketserver
import webbrowser
import json
import os
import re
url="http://localhost:8080/www/index.html"
PORT=8080

Handler=http.server.SimpleHTTPRequestHandler

class CustomHandler(Handler):
        def do_GET(self):
                qp=urlparse(self.path).query
                q=parse_qs(qp).get('term',None)
                if q!=None:
                        self.send_response(200)
                        self.send_header('Content-type','text/html')
                        self.end_headers()
                        wl=self.get_words(str(q[0]))
                        print(q[0])
                        self.wfile.write(bytes(json.dumps(wl),encoding='utf-8'))
                else:
                        f = self.send_head()
                        if f:
                            try:
                                self.copyfile(f, self.wfile)
                            finally:
                                f.close()
        def get_words(self,term):
                wordlist=[]
                wf=open("words.txt","r")
                count=0
                for word in wf:
                        word=word.strip()
                        if count>=10:
                                break
                        elif re.match(term,word):
                                wordlist.append(word)
                                count+=1
                return wordlist       

# ip can be 0.0.0.0 or 127.0.0.1
# for lan access and get the ip from dhcp of router 0.0.0.0
with socketserver.TCPServer(("0.0.0.0",PORT),CustomHandler) as httpd:
    print("Http Server running at Port",PORT)
    webbrowser.open_new_tab(url)
    httpd.serve_forever()
