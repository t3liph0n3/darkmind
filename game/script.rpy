# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


# The game starts here.

label start:
    ### Battle system from: https://lemmasoft.renai.us/forums/viewtopic.php?p=295367#p295367 ###
    # Create pros (name, loc, tic, tok, pwd, tkn)
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

     
    # Create battle actors (name, max_hp, pros, def_pro, type)
    $player = Actor("Nix",2, [ioni, dori, phry, lydi], [lydi])
    $Demon = Actor("Demon",2,[tic1, loc1],[tic1, loc1])
    

label battle:
    show screen battle_ui
    "Demon appeared"
    while Demon.hp>0:
        $ player.command(Demon)
        if player.hp <1:
            "gameover"
            $ renpy.full_restart()
    "You win"
    hide screen battle_ui
    $ player.reset(Demon)
    jump story
    
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
            
    class Actor(renpy.store.object):
        def __init__(self, name, max_hp=0, pros=[], def_pro=[]):
            self.name=name
            self.max_hp=max_hp
            self.hp=max_hp
            self.pros = pros
            self.def_pro = def_pro
            
        def command(self, target):
            
            target.pro = target.pros.pop()
            narrator ("{} has {}:pro installed.".format(target.name,target.pro.name))
            self.pro = renpy.call_screen("command")
            self.attack(self.pro, target.pro, target)
            if target.hp < 1:
                return
            
        def attack(self,pro, prot, target):
            if self.pro.loc >= prot.loc and self.pro.tic >= prot.tic and self.pro.tok >= prot.tok and self.pro.pwd >= prot.pwd and self.pro.tkn >= prot.tkn:
                narrator ("{} hits {}.".format(self.name,target.name))
                target.hp -= 1
            else:
                target.pros.append(prot) 
                narrator ("{} nimbly dodges {}'s attack".format(target.name,self.name))

        def reset(self, target):
            self.hp = self.max_hp
            target.hp = target.max_hp
            target.pros = target.def_pro
    
init:           
    screen command:    
        vbox align (.05,.9):
            for i in player.pros:
                textbutton "[i.name]" action Return (value=i)

    screen battle_ui:    
        use battle_frame(char=player, position=(.05,.05))
        use battle_frame(char=Demon, position=(.95,.05))
        
    screen battle_frame:
        frame area (0, 0, 180, 80) align position:
            vbox yfill True:
                text "[char.name]"
                hbox xfill True:
                    text "HP"
                    text "[char.hp]/[char.max_hp]" xalign 1.0


label story:
    "That wasn't too hard, was it?"
    call battle
