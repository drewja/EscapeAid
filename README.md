EscapeAid
=========

## Python API and CLI tool for easy 256 color printing in Xterm.
##### getting started...
`git clone https://github.com/drewja/EscapeAid.git`  

for printing directly from the shell you must first add a symlink to a folder in your path..
If you dont have a folder in somewhere in your home directory that is in your PATH enviroment.  
create one like so..
```bash
mkdir ~/bin
```
now for the symlink...
```bash
cd ~/bin
ln -s -T path/to/EscapeAid/escapeaid.py escapeaid
```
and finally append ~/bin to your PATH enviroment variable and add it to your .bash_profile
to keep it accross reboots...
`export PATH=$PATH:~/bin && echo "export PATH=$PATH:~/bin" >> ~/.bash_profile`  
[more on PATH and exporting enviroment variables here](http://unix.stackexchange.com/questions/26047/how-to-correctly-add-a-path-to-path#answer-26059)

now you can use the escapeaid command from anywhere in the shell. try this...  
```bash
   [jdoe@jdoepc ~]$ escapeaid 'this is fun' red yellow bold
```
should print <b style=<"font-color:red;">this is fun</b> with bold red text and yellow background



 
 

