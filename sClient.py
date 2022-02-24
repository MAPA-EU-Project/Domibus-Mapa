import glob
import os
import time

client_in_dir="/home/ubuntu/client/in/"
client_out_dir="/home/ubuntu/client/out/"
filestore="/home/ubuntu/filestore/"
# root_dir needs a trailing slash (i.e. /root/dir/)
error=False
while not error:
     #client out to filestore OUT
     print("Checking client/out")
     for filename in glob.iglob(client_out_dir + '**/*.txt', recursive=True):
          command="mv " + filename + " " + filestore + "/OUT"
          print(command)
          os.system(command)

     #filestore IN to client IN
     print("checking filestore/IN")
     for filename in glob.iglob(filestore+"IN/" + '**/*.txt', recursive=True):
          command="mv " + filename + " " + client_in_dir + os.path.basename(filename)
          print(command)
          os.system(command)
     time.sleep(5)



a = threading.Thread(target=watcher, name='Thread-a', daemon=True)
a.start()
app.run(host='0.0.0.0', port= 8090)
