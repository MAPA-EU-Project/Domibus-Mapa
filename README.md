# TEST Domibus-MAPA
## Setup
We use 2 machines (Ubuntu 16.04 on Amazon):

> 52.50.218.51, is the machine containing the Server Access Point and the Server Bridge [SERVER].

> 54.171.7.119, is the machine containing the Client Access Point and the Client/Plugin Bridge [CLIENT].
	
### Access to the machines
Access is done by ssh with the ubuntu user and a PEM (different for each of them):
  
* [SERVER] *ssh -i IBWC2.pem ubuntu@52.50.218.51*

* [CLIENT] *ssh -i IBWC3.pem ubuntu@54.171.7.119*


### Domibus
On both machines DOMIBUS is installed in **/home/ubuntu/cef**

And the FilePlugin file repository is at **/home/ubuntu/filestore**

To start DOMIBUS on each of the machines:

*sudo service mysql start*

*sudo /home/ubuntu/cef/domibus/bin/startup.sh* 

To check that Domibus is working
	
  *sudo tail -f /home/ubuntu/cef/domibus/logs/catalina.out*
	
  *sudo service mysql status*

To verify that everything is OK you have to enter administration:
	
  **http://52.50.218.51:8080/domibus/ (usuario:admin, password:123456)**
	
  **http://54.171.7.119:8080/domibus/ (usuario:admin, password:123456)**

If everything works, what happens is that ay file that is copied to one of the **filestore/OUT** directories will appear on the other machine in a 
subdirectory of **filestore/IN**

(this can be checked at this point, before moving on. This tests the Domibus/AS4 communication mechanism. Traces such as messages on the administration web should corroborate this).

## Bridges
Bridges are Python3.5 programs in **/home/ubuntu/bridge**.

### Client Bridge
Starting the bridge on CLIENT machine
	
  *cd /home/ubuntu/bridge*
	
  *sudo python3.5 sClient.py*

The client bridge is started. It waits for requests **as if it were the MAPA server** on port *8090*.

As it has been started from the console, the output-log is displayed. The ssh session must be kept running during the whole test. 

### Server Bridge
Starting the bridge on SERVER machine
	
  *cd /home/ubuntu/bridge*
	
  *sudo python3.5 sServer.py*

The bridge server is started. It watches the **filestore/IN directory**, when it receives a file it sends it to MAPA and 
waits for it to be processed (translated). When the file is translated, it copies it to **filestore/OUT**.

As it has been started from the console, the output-log is displayed on the screen. The ssh session must be kept running during the whole test. 



## Test
The test consists of sending an HTTP POST to the client bridge with a file and immediately sending POSTs to retrieve the translation.
The posts below can be loaded in POSTMAN but you can also use another tool or a simple curl.  

1. Sending a translation request:

>	POST /api/atranslatefile HTTP/1.1
>
>	Host: 54.171.7.119:8090
>
>	Content-Type: application/json
>
>	{
>		"token": "123456",
>		"source": "en",
>		"target": "en",
>		"fileType": "txt",
>		"file": "SG9sYSEKRXN0YSBlcyBvdHJhIGzDrW5lYS4="
>		
>	}

The client bridge receives the request and processes it (copying the file to filestore/OUT). The request must return:

> {"success": "true", 
>
> "data": {"guid": 1}, "error": "null"}

Write down the guid (in this case 1), because it is the identifier we will need to retrieve the translation.


Retrieving the translated file:
	
>  POST /api/aretrievefiletranslation HTTP/1.1
>
>	Host: 54.171.7.119:8090
>
>	Content-Type: application/json
>
>	{
>		"token": "123456",
>		"guid": "1"
>	}

If the file is not translated yet the result is:

> { "error": 
>
> { "code": 16, "statusCode": 400, "message": "Missing <guid>"}, 
> 
> "success": "false", "data": "null"}

If the file is already translated the result is:

> {"error": "null", 
>
> "success": "true", 
>
> "data": 
> 
> {"guid": "1", "file": "SGVsbG8hIAoKVGhpcyBpcyBhbm90aGVyIGxpbmUuCg==", "fileType": "txt"}}}

The file fields in the two POSTs are Base64 encoded. They can be easily decoded, e.g. at https://codebeautify.org/base64-decode.

## Verification

A complete verification should additionally:

* Check that the Domibus 3.3.3 code and the FilePlugin are the official downloadable ones from the Domibus repository.
* Check with the administrator of the Domibus Access Points (Server and Client) that the translation request has generated messages between the 2 Domibus.
* Verify the code of the 2 Bridges. It is VERY simple and the verification can be done in half an hour.	

