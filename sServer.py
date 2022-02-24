import glob
import os
import time
import requests
import json

def anon(line):
     url = 'https://prod.pangeamt.com:8443/NexRelay/v1/translate'
     data = {
	"src":"en",
	"tgt":"en",
	"text":[line],
	"engine":948,
	"username":"admin@pangeanic.mt",
	"runparms":
		{"Sensitivity":"0.8",
		"Type":"Redaction",
		"Tags":[]
		}
        }

     headers = {'Content-type': 'application/json'}

     r = requests.post(url, data=json.dumps(data), headers=headers)
     ans = r.text
     print(ans)
     translationresponse = json.loads(ans, strict=False)
     #print(translationresponse[0][0]['tgt'])
     return translationresponse[0][0]['tgt']

filestore="/home/ubuntu/filestore/"
# root_dir needs a trailing slash (i.e. /root/dir/)
error=False
while not error:
     #filestore IN to client IN
     print("checking filestore/IN")
     for filename in glob.iglob(filestore+"IN/" + '**/*.txt', recursive=True):
          #read filename line by line, send to anonimize and write in anon file
          filein = open(filename, 'r')
          lines = filein.readlines()
          fileout = open('tmp.anon.txt', 'w')
          for line in lines:
              anonline=anon(line)
              fileout.write(anonline)
          fileout.close()

          #cp anonfile into OUT bo
          command="cp tmp.anon.txt " + filestore+ 'OUT/' + os.path.basename(filename).replace(".txt",".anon.txt")
          print(command)
          os.system(command)
          #delete in file
          command="rm -f tmp.anon.txt " + filename
          print(command)
          os.system(command)

     time.sleep(5)


