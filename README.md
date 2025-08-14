# Realmlist changing CLI util for World of Warcraft

## See usage.txt for more info

```
cat usage.txt
```
Or
```
chmod +x ./realm.py && ./realm.py --help
```

### Starting from 1.1.1 - pipes enabled for next usecase:

- ./realm.py list --hidden | ./realm.py show

### New in 1.1.2b

#### realm_tk.py - minimalistic tkinter GUI app

```
chmod +x ./realm_tk.py && ./realm_tk.py
```

- "Use" function available for chosen realm to play
- "Remove" function available for realm hiding from list
- "Add" and "Clear" functions are 'NotImplemented' yet

### Starting from 1.2.3 - git clone --recurse-submodules required for 'tools' submodule

### Starting from 1.2.4 - new script for fast submodule usage config (locally)

```
chmod +x ./config-submodules.sh && ./config-submodules.sh
```
