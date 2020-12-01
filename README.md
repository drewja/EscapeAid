EscapeAid
=========

## Python API and CLI tool for easy 256 color printing in Xterm.
##### getting started...
`git clone https://github.com/drewja/EscapeAid.git`  

Symlink escapeaid.py to a folder in your path: 
```bash
mkdir -p ~/bin
cd ~/bin
ln -s -T path/to/EscapeAid/escapeaid.py escapeaid
`export PATH=$PATH:~/bin && echo "export PATH=$PATH:~/bin" >> ~/.bash_profile` 
``` 
[more on PATH and exporting enviroment variables here](http://unix.stackexchange.com/questions/26047/how-to-correctly-add-a-path-to-path#answer-26059)


now you can use the escapeaid command from anywhere in the shell. try this...  
```bash
   [jdoe@jdoepc ~]$ escapeaid 'this is fun' red yellow bold
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b style="color:red;background-color: #FFFF00">this is fun</b>
