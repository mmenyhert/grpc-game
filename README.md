# Game of Life server and client

The program implements Conway's Game of Life based on a server-client architecture.
The communication is based on the gRPC protocol.
The server and the client are both written in Python.

In the program, we have to select a previous session, or start a new game. Starting a new game selects the new game's session. We can also list previous sessions.

After setting a session or starting a new game, we can step forward to progress the game for the selected session. 

We can also browse through previous game states for the selected session.

## Setup

* Python>=3.8.10
* MySQL>=8.0.39
* TODO: create requirements for Python

## Running the application

1) Start MySQL server, create tables as in `./sql/create_databases.sql`
2) Update the login parameters to be found in `./python/game/game_of_life_globals.py`

```python
DATABASE_CONFIG = {
  'user': 'username',
  'password': 'password',
  'host': '127.0.0.1',
  'database': 'game',
  'raise_on_warnings': True
}
```

3) Run server 

```bash
$ python './python/game/game_server.py'
```

4) Run client

```bash
$ python './python/game/game_client.py'
```

5) Execute game commands defined in the application. For commands, run 

```bash
$ python './python/game/game_client.py' -h
```

## Available client commands

```
positional arguments:
  {say_hello,new_game,show_all_sessions,get_current_session,set_current_session,get_state,step}
                        Subcommands
    say_hello           Say hello to someone. Placeholder example function. Not relevant.
    new_game            Request a new Game of Life and set session to it.
    show_all_sessions   Request to show all sessions and relevant details.
    get_current_session
                        Get the current session ID with relevant details.
    set_current_session
                        Set the current session ID.       
    get_state           Gets the state at step index for  
                        the current session ID.
    step                Progress the current session.

optional arguments:
  -h, --help            show this help message and exit 
```

## Example usage





Let's create a new Game of Life instance with the following command.
```bash
Game of Life >> new_game
```

We should get a similar response.

```
NewGameRequest sent. Received new game and game ID set.
New session requested with (20, 20) with 6adfd653-ee9f-4c56-abab-7305be3724f8 with metadata (_Metadatum(key='user-agent', value='grpc-python/1.66.1 grpc-c/43.0.0 (windows; chttp2)'),)
```

We can check the state of the board.

```bash
Game of Life >> get_state


□□■■■■■■■□■□□□■□□□□□
□□□□□■■□■■□■■□■■■■■■
□□□■□□□■□□□■■□□■■□□□
□■■■□■□□■■□□□■□■□■□■
■□□□□■■■□■□■■■□□■■■■
□■■■■□■■■□□□□□□■■□■■
■□■□■□□■■□□■■□■□■■□■
■■□■■■□■□□■□■■■■■■□□
□□□□■□□■□□□■■□■■■□■□
□□□■□■□□■□■■■□□□■■■□
■□□■■■□□■□■■■■■□□□■■
■□■■■■□■■■□□□□□□□□□□
■■■■■□■■■□□□■■□□■□■■
□■□■□■□■□■□□□□□□■□□■
■■□■■□■□□□■■□■□■■■□■
□□□□■□■■□■■■■□□■□□□■
■■■□■□■■□■□■□■□■□□■■
□■□■□□■□■□□□■■■□■□■■
■□■□■■□■□■■□■■□□□□■□
□■□□□■■■■□■□□□□□■■□□
```

In this case, we can step forward.
```bash
Game of Life >> step
```

We can check the new state of the board. Indexing directly matches with Python's negative indexing.

```bash
Game of Life >> get_state --step -1

□□■■■■■■■□■□□□■□□□□□
□□□□□■■□■■□■■□■■■■■■
□□□■□□□■□□□■■□□■■□□□
□■■■□■□□■■□□□■□■□■□■
■□□□□■■■□■□■■■□□■■■■
□■■■■□■■■□□□□□□■■□■■
■□■□■□□■■□□■■□■□■■□■
■■□■■■□■□□■□■■■■■■□□
□□□□■□□■□□□■■□■■■□■□
□□□■□■□□■□■■■□□□■■■□
■□□■■■□□■□■■■■■□□□■■
■□■■■■□■■■□□□□□□□□□□
■■■■■□■■■□□□■■□□■□■■
□■□■□■□■□■□□□□□□■□□■
■■□■■□■□□□■■□■□■■■□■
□□□□■□■■□■■■■□□■□□□■
■■■□■□■■□■□■□■□■□□■■
□■□■□□■□■□□□■■■□■□■■
■□■□■■□■□■■□■■□□□□■□
□■□□□■■■■□■□□□□□■■□□
```

We can also check details about our session.
    get_current_session

```bash
Game of Life >> get_current_session
```

And get a response similar to this.

```bash
session_id: "6adfd653-ee9f-4c56-abab-7305be3724f8"        
date: "2024-09-25 17:06:20"
metadata: "(_Metadatum(key=\'user-agent\', value=\'grpc-python/1.66.1 grpc-c/43.0.0 (windows; chttp2)\'),)"
steps: 2
last: "2024-09-25 17:06:20"
```

If we create a new game, we immideately switch to it.

```bash
Game of Life >> new_game
NewGameRequest sent. Received new game and game ID set.
New session requested with (20, 20) with 917d692a-46e0-4c24-9a1d-b17ee51673c3 with metadata (_Metadatum(key='user-agent', value='grpc-python/1.66.1 grpc-c/43.0.0 (windows; chttp2)'),)
```

```bash
Game of Life >> new_game
NewGameRequest sent. Received new game and game ID set.
New session requested with (20, 20) with 917d692a-46e0-4c24-9a1d-b17ee51673c3 with metadata (_Metadatum(key='user-agent', value='grpc-python/1.66.1 grpc-c/43.0.0 (windows; chttp2)'),)
```

If we list all sessions, we can see all available sessions.
```bash
Game of Life >> show_all_sessions

session_id: "6adfd653-ee9f-4c56-abab-7305be3724f8"        
date: "2024-09-25 17:06:20"
metadata: "(_Metadatum(key=\'user-agent\', value=\'grpc-python/1.66.1 grpc-c/43.0.0 (windows; chttp2)\'),)"
steps: 2
last: "2024-09-25 17:06:20"

...
```

Now, we can activate the one that we created first.

```bash
Game of Life >> set_current_session -session 6adfd653-ee9f-4c56-abab-7305be3724f8

Current session set to
session_id: "6adfd653-ee9f-4c56-abab-7305be3724f8"        
date: "2024-09-25 17:06:20"
metadata: "(_Metadatum(key=\'user-agent\', value=\'grpc-python/1.66.1 grpc-c/43.0.0 (windows; chttp2)\'),)"
steps: 1
last: "2024-09-25 17:06:20"
```

We can browse previous states with

```bash
Game of Life >> get_state --step 0
□□■■■■■■■□■□□□■□□□□□
□□□□□■■□■■□■■□■■■■■■
□□□■□□□■□□□■■□□■■□□□
□■■■□■□□■■□□□■□■□■□■
■□□□□■■■□■□■■■□□■■■■
□■■■■□■■■□□□□□□■■□■■
■□■□■□□■■□□■■□■□■■□■
■■□■■■□■□□■□■■■■■■□□
□□□□■□□■□□□■■□■■■□■□
□□□■□■□□■□■■■□□□■■■□
■□□■■■□□■□■■■■■□□□■■
■□■■■■□■■■□□□□□□□□□□
■■■■■□■■■□□□■■□□■□■■
□■□■□■□■□■□□□□□□■□□■
■■□■■□■□□□■■□■□■■■□■
□□□□■□■■□■■■■□□■□□□■
■■■□■□■■□■□■□■□■□□■■
□■□■□□■□■□□□■■■□■□■■
■□■□■■□■□■■□■■□□□□■□
□■□□□■■■■□■□□□□□■■□□
```

We can also browse other states.

```bash
Game of Life >> get_state --step 1
□□■■□□□□□□■□□■■□□□□□
□□■□□□□□□■□□■□■□□■■□
■□□■□■□■□□□■□□□□□□□■
□■■■□■□□□■□□□■□■□□□■
□□□□□□□□□■■□■■□□□□□□
□□■□■□□□□■■□□□■□□□□□
□□□□□□□□□■□■■□□□□□□□
■■■□□■□■□□■□□□□□□□□□
□□■□□□□■■■□□□□□□□□■■
□□□■□■■■■□□□□□□□■□□□
■■□□□□□□□□□□□■□□□□■□
□□□□□□□□□□■□□□■□□■□□
□□□□□□□□□□□□□□□□□■■□
□□□□□□□□□■■■□■■□□□□□
□■□■□□□□□□□□□□■■□■□■
□□□□■□□□□■□□□■□■□■□□
□■■□■□□□□■□□□□□■■■□□
□□□□□□□□□□□□□□□■□□□□
■□■■■□□□□□■□■□■■■□■□
□■□□□□□□□□■□□■□□□■□□
```








## TODO

* Error handling on the server and client sides.
* More efficient stateful server. E.g. store each relevant field for the current session.
* Refactor fully statefulnes for more efficient queries. E.g. for `get_state`, `set_state` and `step`.
* Implement ORM for higher level SQL representation in Python. Also, to circumvent SQL injection.