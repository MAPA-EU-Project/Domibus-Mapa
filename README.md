# TEST Domibus-MAPA
## Setup
We use 2 boxes (Ubuntu 20.04 on AWS Ireland region):

> 3.249.139.208, is the box containing a Domibus End Point and the Anonimization functionality [SERVER].

> 34.249.115.177, is the box containing a second Domibus endpoint Point and the Client/Plugin Bridge [CLIENT].

Both boxes run latest Domibus distribution on Tomcat (domibus-distribution-4.2.7-tomcat-full.zip) and the latest Domibus fileplugin (domibus-distribution-4.2.7-default-fs-plugin.zip). Domibus components were downloaded from official repository at https://ec.europa.eu/digital-building-blocks/wikis/display/CEFDIGITAL/Domibus and installed strictly with the documented procedures. 


### Domibus configuration
On both machines DOMIBUS is installed in **/home/ubuntu/DOMIBUS**

And the FilePlugin file repository is at **/home/ubuntu/filestore**

Configuration is default as documented. The server is RED node and the client is BLUE node.
Fileplugins in both boxes are configured to communicate by default.

Admin access to the Domibus endpoints thru the Domibus console
  **http://3.249.139.208:8080/domibus/ (user:admin, password:------)** [SERVER]
	
  **http://34.249.115.177:8080/domibus/ (user:admin, password:------)** [CLIENT]

If everything works, what happens is that a file that is copied to one of the **filestore/OUT** directories will appear on the other machine in a 
subdirectory of **filestore/IN**

(this can be checked at this point, before moving on. This tests the Domibus/AS4 communication mechanism. Traces such as messages on the administration web should corroborate this).

## Bridges
Bridges are Python3 programs in **/home/ubuntu/**.

### Client Bridge
The client checks periodically files appearing in the directory **/home/ubuntu/client/out** and uses the fileplugin to send the new files to the server endpont securely.

The client also checks the reception by domibus of anonimized files and moves them to the **/home/ubuntu/client/in** 

### Server Bridge
The bridge server watches the **filestore/IN directory**, when it receives a file it sends it to MAPA and 
waits for it to be processed (translated). When the file is translated, it copies it to **filestore/OUT** sending it back to the client using the secure Domibus channel.



## Test
1. Create a txt file with some english sentences to be anonimized by Mapa, for instance:
```
My name is John Taylor
I live in Paris
I'm currently working for Pangeanic
```
2. Use any sftp client to send the file to the client box at 34.249.115.177:/home/ubuntu/client/out (user:client, password:------)

3. Wait for the process to complete, typically one minute for small files. Use any sftp client to check 34.249.115.177:/home/ubuntu/client/out where the anonimized file will be created.


## Verification

A complete verification should additionally:

* Check with the administrator of the Domibus Access Points (Server and Client) that the anonimization request has generated messages between the 2 Domibus.
* Verify the code of the 2 Bridges. It is VERY simple and the verification can be done in half an hour.	

