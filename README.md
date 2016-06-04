# Online Python Tutor extension for the IPython shell

[Introduction](#introduction)  
[Prerequisites](#prerequisites)  
[Instructions](#instructions)  
[Changes](#changes)  

---
  
  
### Introduction

When this extension is loaded, you can type code into the IPython prompt and visualize its execution in a web browser.

This extension also defines a `%clear` magic command to clear the user's global environment and accompanying visualization, and `%run_server` command to start tornado server and run default browser from within IPython

One-minute video demo:

[![Online Python Tutor + IPython shell](http://img.youtube.com/vi/Q3oarDuZPL0/0.jpg)](http://www.youtube.com/watch?v=Q3oarDuZPL0)
  
  
### Prerequisites:

 - IPython shell (http://ipython.org)
 - Tornado Web server (http://www.tornadoweb.org)
  
  
### Instructions:

Clone this repo:
    
```shell
$ git clone https://github.com/klonuo/opt-ipy
$ cd opt-ipy
```

then start the IPython shell in this directory by running:

```shell
$ ipython
```

and load the extension and start server by running: 

```python
In[1]: %load_ext opt_ipy

In[2]: %run_server
```

At this point, as soon as you execute a Python statement in the IPython shell, it should immediately be visualized in your browser.
  
  
### Changes

 - restructure files from [OPT](https://github.com/pgbovine/OnlinePythonTutor) repo related to OPT IPython extension
 - refactor scripts and cleanup code
 - rename files by replacing hyphen with underscore
 - new command to launch server from within IPython shell
