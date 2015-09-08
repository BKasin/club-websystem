# club-websystem
starting up django...
- boot nitrous container

For development purposes only, the django superuser is 'root' with a password of 'password123'.

Using the Linux 'tmux' tool, so all collaborators can use the same terminal:
- Check if there is a screen running:
  - tmux list-sessions
- If it is, attach to it by number:
  - tmux attach
- If not, run a new one:
  - tmux
  - cd code/club-websystem
  - source .env/bin/activate
  - cd src
  - python manage.py runserver 0.0.0.0:3000
- To see who is connected to the tmux session:
  - tmux list-clients
- Exit from the screen session:
  - Type *Ctrl+B*, followed by the *d* key
- To get help on 'tmux' type *Ctrl+B*, followed by the *?* key

Using the Linux 'screen' tool, so all collaborators can use the same terminal:
- Check if there is a screen running:
  - screen -r
- If it is, attach to it by number:
  - screen -x [idnumber]
- If not, run a new one:
  - screen
  - cd code/club-websystem
  - source .env/bin/activate
  - cd src
  - python manage.py runserver 0.0.0.0:3000
- Exit from the screen session:
  - Type *Ctrl+A*, followed by the *d* key
- To get help on 'screen' type *Ctrl+A*, followed by the *?* key
