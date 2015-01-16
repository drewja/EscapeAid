EscapeAid
=========

## Python API and CLI tool for easy 256 color printing in Xterm.
##### getting started...
`git clone https://github.com/drewja/EscapeAid.git`  

for printing directly from the shell you must first add a symlink to a folder in your path..  
`mkdir ~/bin`  <b>if it doesn't already exist </b>  
`ln -s path/to/EscapeAid/escapeaid.py` <b>remember to replace path/to/</b>  
execute the followed by..  
`export PATH=$PATH:~/bin`  [more on PATH and exporting enviroment variables here](http://unix.stackexchange.com/questions/26047/how-to-correctly-add-a-path-to-path#answer-26059)  
and then add the export command you just entered to your ~/.profile, or ~/.bash_profile if you only
care about bash.

now you can use the escapeaid command from anywhere in the shell. try this...  
```bash
   [jdoe@jdoepc ~]$ escapeaid 'this is fun' red yellow bold
```
should print <b style=<"font-color:red;">this is fun</b> with bold red text and yellow background



 
 

