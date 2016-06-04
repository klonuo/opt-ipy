## Online Python Tutor extension for the IPython shell
by Philip Guo (philip@pgbovine.net)
August 2013


When this extension is loaded, you can type code into the IPython prompt and visualize its execution in a web browser.

This extension also defines a `%clear` magic command to clear the user's global environment and accompanying visualization.

One-minute video demo:

[![Online Python Tutor + IPython shell](http://img.youtube.com/vi/Q3oarDuZPL0/0.jpg)](http://www.youtube.com/watch?v=Q3oarDuZPL0)


### Note                                                              
> Original project at: https://github.com/pgbovine/OnlinePythonTutor


### Prerequisites:

 - IPython shell (http://ipython.org/, tested on 0.13.1 and 1.0.dev)
 - tornado Web server (http://www.tornadoweb.org)


### Instructions:

1. Clone this repo:
    
    ```shell
    $ git clone https://github.com/klonuo/opt-ipy
    $ cd opt-ipy
    ```

2. Start a local web server:

    ```shell
    $ python opt/server/opt-ipy-server.py
    ```

3. Load this URL in your browser:

    `http://localhost:8888/`

4. Start the IPython shell in this directory by running:

    ```shell
    $ ipython
    ```

5. Load this extension by running:

    `%load_ext opt-ipy`

At this point, as soon as you execute a Python statement in the IPython shell, it should immediately be visualized in your browser.
