# object for querying and receiving keyboard input

class KeyboardInput:
    # 0 ERROR
    # 1 MOVEFORWARD
    # 2 MOVEBACKWARD
    # 3 MOVELEFT
    # 4 MOVERIGHT
    # 5 LOOKUP
    # 6 LOOKDOWN
    # 7 LOOKLEFT
    # 8 LOOKRIGHT
    keymappings = {"w": 1,
                   "s": 2,
                   "a": 3,
                   "d": 4,
                   "i": 5,
                   "k": 6,
                   "j": 7,
                   "l": 8}


    def __init__():
        return
    
    # takes in input from user and converts to int
    def readinput():
        cmdread = input()
        if cmdread in KeyboardInput.keymappings.keys():
            return KeyboardInput.keymappings[cmdread]
        else:
            return 0
    
    
    