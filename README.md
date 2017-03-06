# postsai-commitstop

A Postsai extension that adds the capability to establish and manage commit stops through a simple web interface for both Git and CVS.


## CVS


The integration with CVS repositories is achieved via a CVS verifymsg hook.

After you copied the file hooks/verifymsg.py to your CVS server, you need to edit CVSROOT/verifymsg in order to invoke it. Please note that verifymsg only supports one hook per module pattern (unlike loginfo).

For example, to use the commitstop extension for all CVS modules in the current repository with a postsai server at example.com:

~~~~
  .* /usr/local/bin/verifymsg.py --repository=repo --url=https://example.com/postsai/extensions/commitstop/api.py --msgfile=%l
~~~~


## Frontend for viewing and updating configurations 


The source code of the web frontend is located under the directory ./frontend. After building it with angular-cli using the command

ng build -w -prod --bh ""

, it can be invoked by opening the location

$domain/postsai/extensions/postsai-commitstop/frontend/dist/

where $domain is the base url of the postsai installation.