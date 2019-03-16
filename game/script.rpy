# darkmind
# by Shane George (https://github.com/t3liph0n3) 2019

# .: Characters :. 
define e = Character("Eileen")


# .: Game Start :.

label start:

# # # # # #
# Battle system 
# # # # # #

    define rnarrator = nvl_narrator

    # Create pros (name, loc, tic, tok, pwd, tkn)
    $ioni = pro("ionian", 1, 0, 1, 1, 0)
    $dori = pro("dorian", 0, 1, 0, 1, 1)
    $phry = pro("phrygian", 0, 0, 1, 1, 1)
    $lydi = pro("lydian", 0, 1, 1, 0, 0)
    # Defensive pros (name, loc, tic, tok, pwd, tkn)
    $tic1 = pro("tic-tok", 0, 1, 1, 0, 0)
    $tic2 = pro("tic-pas", 0, 1, 0, 1, 0)
    $loc1 = pro("loc-tok", 1, 0, 1, 0, 0)
    $tic3 = pro("tic-tkn", 0, 1, 0, 0, 1)
    $loc2 = pro("loc-pwd", 1, 0, 0, 1, 0)
    $tok1 = pro("tok-tkn", 0, 0, 1, 0, 1)

    # Create battle actors (name, max_hp, pros, def_pro, type)
    $player = Actor("Cali",2, [ioni, dori, phry, lydi], [lydi])
    $Demon = Actor("Demon",2,[tic1, loc1],[tic1, loc1])
    $Cartman = Actor("Cartman",1,[tok1],[tok1])


init -1 python:
    from copy import copy    

    # Pro are the protocols silos use for defence...
    class pro():
        def __init__(self, name, loc, tic, tok, pwd, tkn):
            self.name = name
            self.loc = loc
            self.tic = tic
            self.tok = tok
            self.pwd = pwd
            self.tkn = tkn

    # Actors are Players and Silos they battle...
    class Actor(renpy.store.object):
        def __init__(self, name, max_hp=0, pros=[], def_pro=[]):
            self.name=name
            self.max_hp=max_hp
            self.hp=max_hp
            self.pros = pros
            self.def_pro = def_pro

        # BATTLES! (called silo_runs)
        # 1) give the name of the silo/target
        #   2) the silo pops() pro to challenge hacker
        #   3) player selects pro to defeat silo's pro
        #   4) compare pro (if hacker > then silo -1hp)
        #   5) if silo hp > 0 go back to step 2 repeat
        # 6) move on with the story
        def silo_run(self, target):
            nvl_clear()
            rnarrator (">>_ starting run against {}\n".format(target.name))
            while target.hp>0:
                self.command(target)
                if self.hp < 1:
                    rnarrator ("gameover")
                    renpy.full_restart()
            rnarrator ("//* * *\n// now connected to {}".format(target.name))
            return

        # Player chooses an app for the attack
        def command(self, target):            
            target.pro = target.pros.pop()
            rnarrator ("//* {} has active {}:pro\n>>_ select protocol   (or end run)".format(target.name,target.pro.name))
            self.pro = renpy.call_screen("command")
            self.attack(self.pro, target.pro, target)
            if target.hp < 1:
                return

        # In attack
        # check that the choice matches/betters the defense pro
        def attack(self,pro, prot, target):
            if self.pro.loc >= prot.loc and self.pro.tic >= prot.tic and self.pro.tok >= prot.tok and self.pro.pwd >= prot.pwd and self.pro.tkn >= prot.tkn:
                rnarrator ("//* {} has passed {}:pro\n// connecting. . .".format(self.pro.name,prot.name))
                target.hp -= 1
            else:
                target.pros.append(prot)
                rnarrator ("!!\n!!! {} access error".format(target.name))
                self.hp -= 1
                # todo: bad thing for bad attempt...

        # Reset the player
        def reset(self, target):
            self.hp = self.max_hp
            target.hp = target.max_hp
            target.pros = target.def_pro



# Battle Screens
#todo: make this look less gross    
init:           
    screen command:
        style_prefix "choice"
        vbox: 
            for i in player.pros:
                textbutton "[i.name]" action Return (value=i)

    screen battle_ui(target):
        hbox:
            vbox:    
                use battle_frame(char=target, position=(1,.1))
            vbox:
                use battle_frame(char=player, position=(.95,.5))

    screen battle_frame:
        frame area (0, 0, 140, 80) align position:
            vbox yfill True:
                text "[char.name]"
                hbox xfill True:
                    text "HP"
                    text "[char.hp]/[char.max_hp]" xalign 1.0

    # # # # # # 
    # End of Battle System (lines 12 - 129)
    # # # # # #

label battle:

    "welcome..." 
    show screen battle_ui(Demon)
    $ player.silo_run(Demon)
    hide screen battle_ui

    "It worked!"

    show screen battle_ui(Cartman)
    $ player.silo_run(Cartman)
    hide screen battle_ui

    "So..."
