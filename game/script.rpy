# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


# The game starts here.

label start:

    # Protocols
    # /// I got this idea from: https://lemmasoft.renai.us/forums/viewtopic.php?p=295367#p295367
    # (name, loc, tic, tok, pwd, tkn)

    $ioni = pro("ionian", 1, 0, 1, 1, 0)
    $dori = pro("dorian", 0, 1, 0, 1, 1)
    $phry = pro("phrygian", 0, 0, 1, 1, 1)
    $lydi = pro("lydian", 0, 1, 1, 0, 1)

    $tic1 = pro("tic-tok", 0, 1, 1, 0, 0)
    $tic2 = pro("tic-pas", 0, 1, 1, 1, 0)
    $loc1 = pro("loc-tok", 1, 0, 1, 0, 0)
    $tic3 = pro("tic-tkn", 0, 1, 0, 0, 1)
    $loc2 = pro("loc-pwd", 1, 0, 0, 0, 1)
    $tok1 = pro("tok-tkn", 0, 0, 1, 0, 1)

    # Creat starting Rigg
    # and Silo to Roll against
    # (name,[pro/app])

    $hacker = rigs("Ezra", [ioni,lydi])
    $siloA = rigs("Med", [loc1, tic2])

#
#
#
label battle:
    show screen battle_ui

    $b = len(siloA.protocol)

    while b > 0:
        $hacker.command(siloA)
        $b = b-1
    
    "You win"
    hide screen battle_ui
    "Ha Ha Ha"
    jump story


#
#
#
init -1 python:
    from copy import copy

    class pro():
        def __init__(self, name, loc, tic, tok, pwd, tkn):
            self.name = name
            self.loc = loc
            self.tic = tic
            self.tok = tok
            self.pwd = pwd
            self.tkn = tkn

    class rigs(renpy.store.object):
        def __init__(self, name, protocol=[]):
            self.name = name
            self.protocol = protocol

        #TODO Make target pop their choice, then we choose our choice
        def command(self, target):
            target.prot = target.protocol.pop()
            narrator ("{} has {} pro on this level".format(target.name, target.prot.name)) 
            self.prot = renpy.call_screen("command")
            self.attack(self.prot, target.prot)
            if len(target.protocol) < 1:
                return
            #something may hapen here?

    #We compare the two protocols...
        def attack(self,protocol, target):
            if self.protocol.loc >= target.protocol.loc and self.protocol.tic >= target.protocol.tic and self.protocol.tok >= target.protocol.tok and self.protocol.pwd >= target.protocol.pwd and self.protocol.tkn >= target.protocol.tkn:
                narrator ("You bust the silo pro")
            else:
                narrator ("YOU ARE UNABLE TO GET THROUGH")
                renpy.full_restart()
            

init:
    screen command:
        vbox align (.05,.9):
            for i in hacker.protocol:
                textbutton "[i.name]" action Return (valie=i)

    screen battle_ui:    
        use battle_frame(char=hacker, position=(.05,.05))
        use battle_frame(char=siloA, position=(.95,.05))

    screen battle_frame:
        frame area (0, 0, 180, 80) align positon:
            vbox yfill True:
                text "[char.name]"

#
#
#
label story:
    "let us continue"    




    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    # These display lines of dialogue.

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"


# This ends the game

label ender:

    return
