from sys import exit #stops the program
import time #to allow for things to come more slowly such as dialogue or information
import random #make for random events or random amounts of damage dealt by the enemy
import threading #allows me to implement a timer for a game event

#there are two functions, setup and menu, setup contains most of the functons used to make the game work

def game():
    hp = 150 #nonlocal variables hp, atk
    atk = 15
    weapon_list = [] #for only one weapon
    inventory = []
    #changed the inventory into a nonlocal variable as to make appending items easier
    #inventory has items crucial to the gameplay
    medkits = 1
    upgrade = False
    ally = False #based on gameplay, once this is set to true, it can help with the final boss
    ally_dead = False #if the ally is dead, this is True
    past_start = False #determine whether you have went through the starting room
    first_encounter_event = False #if you have done the attack in that room
    first_encounter_return = False #once you have gone through, changes state when you go back
    first_item_event = False #if you have done the attack in that room
    first_item_return = False #once you have gone through, changes state when you go back
    cellar_enemies_dead = False #if those enemies have been killed so you dont encounter them again if you return
    lab_locked = False #once set to true, cannot access area again
    letter_taken = False #if it is False, you have the opportunity to find it
    SR_key_taken = False  # if it is False, you have the opportunity to find it
    plant_killed = False #whether the unique one time enemy is dead or not
    MH_key_taken = False  # if it is False, you have the opportunity to find it
    behemoth_info = False #affects the description of some of your actions if set to true
    survivor_met = False
    endingX = False #For all endings that are false, it means it is undiscovered
    endingF = False
    endingE = False
    endingC = False
    endingB = False
    endingA = False
    #functions are more action based rather than being a key variable,
    #e.g no function for health, instead actions to modify health

    def finding(amount):
        nonlocal medkits
        time.sleep(1)
        if amount > 1:
            print("Will you take the", amount, "medkits")  # choice
        else:
            print("Will you take the medkit")
        print("* The maximum amount of medkits to be carried is 10 *")
        choice = input("> ")
        if choice.startswith("y") == True and medkits == 10:
            print("You cannot carry anymore medkits")
        elif choice.startswith("y") == True and amount > 1:
            print("You have taken the medkits")
            medkits = medkits + amount  # adds amount that is determined so it won't repetitively ask for multiple medkits
            print("Medkits:", medkits)
        elif choice.startswith("y") == True and amount == 1:
            print("You have taken the medkit")
            medkits = medkits + amount  # adds amount that is determined so it won't repetitively ask for multiple medkits
            print("Medkits:", medkits)
        else:
            print("You don't take anything")
        pass

    def healing():  # healing function during the gameplay
        nonlocal hp
        nonlocal medkits
        if medkits >= 1 and hp < 150: #if statement to show whether you are allowed to do the action
            print("You have healed yourself")
            medkits = medkits - 1 #gain health, lose medkit
            hp = hp + 50
            print("Health items remaining: ",medkits)
        elif medkits == 0:
            print("You cannot health as you have 0 Medical items remaining")
        elif hp == 150: #maximum health
            print("You have maximum health and don't need to heal")
            print("Health items remaining: ",medkits)
        pass

    def damage(type): # all the damage types for different enemy types, randomised
        nonlocal hp
        if type == "undead_atk":
            hp = hp - random.randint(5,15)
        elif type == "animal_atk":
            hp = hp - random.randint(10,25)
        elif type == "plant_atk":
            hp = hp - random.randint(100,150)
        elif type == "survivor_atk":
            hp = hp - random.randint(15,35)
        elif type == "boss_atk":
            hp = hp - random.randint(10,65)
        elif type == "defend_undead":
            hp = hp - random.randint(1,5)
        elif type == "defend_animal":
            hp = hp - random.randint(1,10)
        elif type == "defend_plant":
            hp = hp - 1
        elif type == "defend_survivor":
            hp = hp - random.randint(5,15)
        elif type == "defend_boss":
            hp = hp - random.randint(1,25)

    def defend(): #another action during the gameplay, usually used if there are no medkits left
        nonlocal hp
        if hp < 150:
            hp = hp + random.randint(5,30)
            print("You have make a small recovery")
        elif hp >= 150:
            print("You didnt need to recover")
        pass

    def escape():
        nonlocal hp
        chance = random.randint(0,1)
        time.sleep(1)
        if chance == 0:
            print("You flee without getting hurt")
        else:
            print("You escape with a minor injury")
            hp = hp - 20
            print("HP :", hp)
        pass

    def playAgain(): #once you die, this function allows you to choose to play from the start or return to the menu
        print("Do you want to play again?")
        if input("> ").startswith('y') == True:
            test_attack()
        elif input("> ").startswith('n') == True:
            print("Bye for now")
            menu()
        else:
            print("Answer with a 'yes' or 'no'")

    def dead(why): # set the reasoning of the player's death
        time.sleep(2)
        print(why)
        playAgain()

    def loot():
        drop_chance = random.randint(0,100) #chances of a drop
        if drop_chance >= 50:
            time.sleep(1)
            print("There are no items of use here") #50/50 chance of player getting
        elif 80 >= drop_chance > 50:
            time.sleep(1)
            finding(1)
        elif 95 >= drop_chance > 80:
            time.sleep(1)
            finding(random.randint(2,4))
        pass

    #The following functions are all weapon types
    #The commenting for the screwdriver applies to all of the weapons

    def screwdriver():
        nonlocal atk
        nonlocal weapon_list
        print("Will you take the screwdriver")
        time.sleep(1)       #my system for weapons allows the player to equip only one weapon at a time
        print("* You will discard your previous weapon *") #so the equipped weapon would be discarded
        time.sleep(2)
        print("Atk: ", atk)
        print("Current weapon: ", weapon_list)
        choice = input("> ")    #a choice for the player just in case they have a better weapon
        if choice.startswith("y") == True:
            print("You have taken the screwdriver")
            weapon_list.clear()
            weapon_list.append("Screwdriver") #new weapon is added
            atk = 25 #the attack stat is changed
            print("Atk: ", atk)
            print("Current weapon: ", weapon_list) #shows the weapon equipped and attack stat
        else:
            print("You leave the item")
        pass

    def knife():
        nonlocal atk
        nonlocal weapon_list
        print("Will you take the knife")
        time.sleep(1)
        print("* You will discard your previous weapon *")
        time.sleep(2)
        print("Atk: ", atk)
        print("Current weapon: ", weapon_list)
        choice = input("> ")
        if choice.startswith("y") == True:
            print("You have taken the knife")
            weapon_list.clear()
            if upgrade == True: #the weapon upgrade applies to all except the screwdriver
                atk = 45
                weapon_list.append("Knife (Upgraded)") #upgraded version of the weapon in the list
            else:
                atk = 30
                weapon_list.append("Knife")
            print("Atk: ", atk)
            print("Current weapon: ", weapon_list)
        else:
            print("You leave the item")
        pass

    def pistol():
        nonlocal upgrade
        nonlocal atk
        nonlocal weapon_list
        print("Will you take the pistol")
        time.sleep(1)
        print("* You will discard your previous weapon *")
        time.sleep(2)
        print("Atk: ", atk)
        print("Current weapon: ", weapon_list)
        choice = input("> ")
        if choice.startswith("y") == True:
            print("You have taken the pistol")
            weapon_list.clear()
            if upgrade == True:
                atk = 60
                weapon_list.append("Pistol (Upgraded)")
            else:
                atk = 45
                weapon_list.append("Pistol")
            print("Atk: ", atk)
            print("Current weapon: ", weapon_list)
        else:
            print("You leave the item")
        pass

    def revolver():
        nonlocal atk
        nonlocal weapon_list
        print("Will you take the revolver")
        time.sleep(1)
        print("* You will discard your previous weapon *")
        time.sleep(2)
        print("Atk: ", atk)
        print("Current weapon: ", weapon_list)
        choice = input("> ")
        if choice.startswith("y") == True:
            print("You have taken the revolver")
            weapon_list.clear()
            if upgrade == True:
                atk = 70
                weapon_list.append("Revolver (Upgraded)")
            else:
                atk = 55
                weapon_list.append("Revolver")
            time.sleep(2)
            print("Atk: ", atk)
            print("Current weapon: ", weapon_list)
        else:
            print("You leave the item")
        pass

    def shotgun():
        nonlocal atk
        nonlocal weapon_list
        print("Will you take the shotgun")
        time.sleep(1)
        print("* You will discard your previous weapon *")
        time.sleep(2)
        print("Atk: ", atk)
        print("Current weapon: ", weapon_list)
        time.sleep(1)
        print("* You will discard your previous weapon *")
        choice = input("> ")
        if choice.startswith("y") == True:
            print("You have taken the shotgun")
            weapon_list.clear()
            if upgrade == True:
                atk = 80
                weapon_list.append("Shotgun (Upgraded)")
            else:
                atk = 65
                weapon_list.append("Shotgun")
            time.sleep(2)
            print("Atk: ", atk)
            print("Current weapon: ", weapon_list)
        else:
            print("You leave the item")
        pass

    def BWCR():
        nonlocal atk
        nonlocal weapon_list
        print("Will you take the BioWeapon Countermeasure Rife")
        time.sleep(1)
        print("* You will discard your previous weapon *")
        time.sleep(2)
        print("Atk: ", atk)
        print("Current weapon: ", weapon_list)
        time.sleep(1)
        print("* You will discard your previous weapon *")
        choice = input("> ")
        if choice.startswith("y") == True:
            print("You have taken the BioWeapon Countermeasure Rife")
            weapon_list.clear()
            weapon_list.append("BWCR-V0.8")
            if upgrade == True:
                atk = 100
                weapon_list.append("BWCR-V0.8 (Upgraded)")
            else:
                atk = 85
                weapon_list.append("BWCR-V0.8")
            print("Atk: ", atk)
            print("Current weapon: ", weapon_list)
        else:
            print("You leave the item")
        pass

    def weapon_upgrade():
        print("You've found a weapon upgrader")
        time.sleep(2)
        print("It adds +15 to attack")
        time.sleep(1)
        inventory.append("Weapon Upgrader")
        upgrade = True #once this condition is true, every weapon will get +15 attack
        pass

    #commenting for enemies is mostly the same except for the behemoth boss

    def first_undead(): #as said in the function name, it is the first undead encounter
        nonlocal atk
        nonlocal hp
        enemy_HP = 40 #enemy hp
        time.sleep(1)
        print("the corpse rises")
        time.sleep(2)
        print("He isn't dead, he is undead!")
        time.sleep(2)
        print("He is trying to attack you!")
        time.sleep(1)
        print("")
        while hp > 0 and enemy_HP > 0: #while you and the enemy are alive
            print("(1) Attack")
            print("(2) Heal ") # 3 actions
            print("(3) Defend")
            defence = False

            choice = input("> ")
            if choice == "1":
                enemy_HP = enemy_HP - atk #enemy loses health based on the number your attack is
            elif choice == "2":
                healing() #healing function
            elif choice == "3":
                defend()   #defend function
            chance = random.randint(0, 4) #chance of dodging the enemy attack
            if chance == 0 or chance == 4:
                print("You dodged the undead's attack")
            elif defence == True:
                damage("defend_undead") #defending reduces damage
                print("You defended the undead's attack")
                defence = False
            else:
                damage("undead_atk") #uses attack function
                print("You have been hurt")
            print("")
            print("HP :", hp) #display enemy and player hp
            print("Undead's HP: ", enemy_HP)
            print("")
            if enemy_HP <= 0:   #once the enemy's health hits 0, it is defeated
                print("")
                print("You killed that horror")
                pass #continue to the room function
            elif hp <= 0: #if you die
                print("")
                print("**********************")
                dead("You were devoured by that abomination") #player is defeated, uses dead function

    def undead(intro):  # similar to first undead
        nonlocal atk
        nonlocal hp
        enemy_HP = random.randint(20, 50)
        time.sleep(1)
        print(intro) #as it is a common enemy, you can write different intros
        time.sleep(2)
        print("What will you do")
        time.sleep(2)
        print("")
        print("Undead's HP: ", enemy_HP)
        print("")
        time.sleep(2)
        while hp > 0 and enemy_HP > 0:
            print("(1) Attack")
            print("(2) Heal ")
            print("(3) Defend")
            print("(4) Run") #this time you have an escaoe option
            run = False
            defence = False

            choice = input("> ")
            if choice == "1":
                enemy_HP = enemy_HP - atk
            elif choice == "2":
                healing()
            elif choice == "3":
                defend()
            elif choice == "4":
                escape() #escape damage may be taken
                run = True
            if run == True:
                break #breaks the loop
                pass
            chance = random.randint(0, 4)
            if chance == 0 or chance == 4:
                print("You dodged the undead's attack")
            elif defence == True:
                damage("defend_undead")
                print("You defended the undead's attack")
                defence = False
            else:
                damage("undead_atk")
                print("You have been hurt")
            print("")
            print("HP :", hp)
            print("Undead's HP: ", enemy_HP)
            print("")
            if enemy_HP <= 0:
                print("")
                print("You killed the undead creature")
                print("You search it...")
                loot()
                pass
            elif hp <= 0:
                print("")
                print("**********************")
                dead("You were devoured by the abomination")

    def animal(intro):  # same as undead
        nonlocal atk
        nonlocal hp
        enemy_HP = random.randint(30, 50)
        time.sleep(1)
        print(intro)
        time.sleep(2)
        print("What will you do")
        time.sleep(2)
        print("")
        print("Animal's HP: ", enemy_HP)
        print("")
        time.sleep(2)

        while hp > 0 and enemy_HP > 0:
            print("(1) Attack")
            print("(2) Heal ")
            print("(3) Defend")
            print("(4) Run")
            run = False
            defence = False

            choice = input("> ")
            if choice == "1":
                enemy_HP = enemy_HP - atk
            elif choice == "2":
                healing()
            elif choice == "3":
                defend()
            elif choice == "4":
                escape()
                run = True
            if run == True:
                break
                pass
            chance = random.randint(0, 4)
            if chance == 0 or chance == 4:
                print("You dodged the animal's attack")
            elif defence == True:
                damage("defend_animal")
                print("You defended the animal's attack")
                defence = False
            else:
                damage("animal_atk")
                print("You have been hurt")
            print("")
            print("HP :", hp)
            print("Animal's HP: ", enemy_HP)
            print("")
            if enemy_HP <= 0 and run == False:
                print("")
                print("You killed the mutant animal")
                print("You search it...")
                loot()
                pass
            elif hp <= 0:
                print("")
                print("**********************")
                dead("Your flesh was ripped apart by that infected animal")

    def plant_beast():  # as said in the function name, it is the first undead encounter
        nonlocal atk
        nonlocal hp
        enemy_HP = 40
        time.sleep(1)
        print("A half plant man attacks you!")
        time.sleep(1)
        print("")
        while hp > 0 and enemy_HP > 0:
            print("(1) Attack")
            print("(2) Heal ")
            print("(3) Defend")
            defence = False

            choice = input("> ")
            if choice == "1":
                enemy_HP = enemy_HP - atk
            elif choice == "2":
                healing()
            elif choice == "3":
                defend()
            chance = random.randint(0, 4)
            if chance == 0 or chance == 4:
                print("You dodged the plant's attack")
            elif defence == True:
                damage("defend_plant")
                print("You defended the plant's attack")
                defence = False
            else:
                damage("plant_atk")
                print("You have been hurt")
            print("")
            print("HP :", hp)
            print("Plant Hybrid's HP: ", enemy_HP)
            print("")
            if enemy_HP <= 0:
                print("")
                print("You killed that twisted thing")
                shotgun()
                chance = random.randint(0,8)
                if chance == 3:
                    weapon_upgrade()
                pass
            elif hp <= 0:
                print("")
                print("**********************")
                dead("You were tenderised by that plant hybrid")

    def survivor_snapped(): #same as first undead, you cannot escape, more of an optional sub boss
        nonlocal atk
        nonlocal hp
        enemy_HP = 150
        time.sleep(1)
        print("He's snapped")
        time.sleep(2)
        print("He won't let you go now")
        time.sleep(1)
        print("He wants you dead")
        time.sleep(2)
        print("")
        print("Survivor's HP: ", enemy_HP)
        print("")
        time.sleep(2)
        while hp > 0 and enemy_HP > 0:
            print("(1) Attack")
            print("(2) Heal ")
            print("(3) Defend")
            defence = False

            choice = input("> ")
            if choice == "1":
                enemy_HP = enemy_HP - atk
            elif choice == "2":
                healing()
            elif choice == "3":
                defend()
            chance = random.randint(0, 4)
            if chance == 0 or chance == 4:
                print("You dodged his attack")
            elif defence == True:
                damage("defend_survivor")
                print("You defended the survivor's attack")
                defence = False
            else:
                damage("survivor_atk")
                print("You have been hurt")
            print("")
            print("HP :", hp)
            print("Survivor's HP: ", enemy_HP)
            print("")
            if enemy_HP <= 0:
                print("You killed the poor man")
                ally_dead = True
            elif hp <= 0:
                print("**********************")
                dead("He killed you and felt nothing for it")

    def behemoth_fight(): #if you gain the ally, he fights along side you
        nonlocal atk    #this is the final boss, the outcomes of your actions from the battle
        nonlocal hp     #and from choices affect the ending, there are 5 ending achievable this way
        nonlocal ally   #ending 6 achievable from the start
        nonlocal ally_dead
        nonlocal behemoth_info
        ally_hp = 100 #ally hp
        ally_atk = 40   #ally attack
        enemy_HP = 2000
        time.sleep(1)
        print("You come into the main hall")
        time.sleep(2)
        print("The chandelier is illumating this grand hall")
        time.sleep(2)
        if behemoth_info == True:
            print("The B1-42/Behemoth is right in front of your eyes")
            time.sleep(2)
            print("It is horrific!")
        else:
            print("WHAT ON EARTH?")
            time.sleep(2)
            print("What is this huge creature?????")
        time.sleep(2)
        print("An 9ft beast with a humanoid body with a gaping jaw and empty lifeless eyes")
        time.sleep(4)
        print("It's right arm occupied with a huge piercing tentacle")
        time.sleep(3)
        print("As you process what you are seeing, the beast lets out a horrific shriek")
        time.sleep(4)
        print("The thing is bursting out more limbs! and it is growing bigger")
        time.sleep(3)
        print("There is no turning back now, you must fight it")
        if ally == True:
            print("")
            time.sleep(2)
            print("You hear the door open from behind")
            time.sleep(1)
            print("'Yo, I wanted to take a piece of this thi-'")
            time.sleep(2)
            print("'Oh God.'")
            time.sleep(2)
            print("'We need to kill the thing before it mutates!'")
        time.sleep(2)
        print("")
        print("Behemoth's HP: ", enemy_HP)
        print("")
        time.sleep(2)
        while hp > 0 and enemy_HP > 0:
            print("(1) Attack")
            print("(2) Heal ")
            print("(3) Defend")
            defence = False

            choice = input("> ")
            if choice == "1":
                enemy_HP = enemy_HP - atk
                if ally_dead == False and ally == True:
                    enemy_HP = enemy_HP - ally_atk #ally will attack with you
            elif choice == "2":
                healing()
                if ally_dead == False and ally == True:
                    ally_hp = ally_hp + 20  #ally has no limit for healing and will always heal 20
            elif choice == "3":
                defend()
                if ally_dead == False and ally == True:
                    enemy_HP = enemy_HP - ally_atk #ally will attack while you defend
            chance = random.randint(0, 4)
            if chance == 0 or chance == 4:
                if ally == True and ally_dead == False:
                    print("You both dodged the creature's attack")
                else:
                    print("You've dodged the beast's attack")
            elif defence == True:
                damage("defend_undead")
                print("You defended the undead's attack")
                defence = False
            else:
                damage("boss_atk")
                if ally == True and ally_dead == False:
                    ally_hp = ally_hp - random.randint(5, 60)
                    print("You've both been hurt")
                else:
                    print("You've been hurt")
                if ally_hp <= 0 and ally == True:
                    time.sleep(2)
                    print("Josh is badly injured") #during the battle, your ally can die
                    time.sleep(2)                  #but you still fight
                    print("'KEEP FIGH-, KEEP FIGHTING IT, I-IT MUST DIE!'")
                    time.sleep(2)
                    ally_dead = True
            print("HP :", hp)
            if ally == True and ally_dead == False:
                print("Ally's HP", ally_hp)
            print("Behemoth's HP: ", enemy_HP)

            if enemy_HP <= 0:
                time.sleep(2)
                print("It spurts out blood from its mouth")
                time.sleep(2)
                print("The beast convulses and falls to the ground")
                time.sleep(2)
                print("It seems you have killed the behemoth")
                if ally == False:
                    ending_c()
                elif ally_dead == True and ally == True: #depending on the boolean conditions
                    ending_b()                           #you will get a different ending
                elif ally_dead == False and ally == True:
                    ending_a()
            elif hp <= 0:
                print("**********************")
                if ally == True and ally_dead == True:
                    ending_e()
                elif ally == False and ally_dead == False:
                    ending_f()

    #endings
    #all endings leave the story somewhat unfufilled in different ways
    #however, the player may be able to understand the story once they see all endings excluding ending x

    def ending_x():
        nonlocal endingX
        time.sleep(4)
        print("\n")
        print("Well...")
        time.sleep(4)
        print("You sit down...")
        time.sleep(5)
        print("with no hope in yourself to escape")
        time.sleep(6)
        print("You pass out...")
        time.sleep(10)
        print("...many hours later...")
        time.sleep(10)
        print("You hear a huge crash and swiftly get up")
        time.sleep(5)
        print("A huge figure looms over you")
        time.sleep(5)
        print("shrouded in darkness you cannot tell what it is")
        time.sleep(5)
        print("It grabs you...")
        time.sleep(6)
        print("and you never see daylight again...")
        time.sleep(4)
        print("")
        print("That is the story you forged")
        time.sleep(5)
        print("...yet it doesn't feel right")
        time.sleep(3)
        print("Doesn't it?")
        print("")
        time.sleep(2)
        print("You have unlocked Secret Ending X")
        endingX = True
        time.sleep(2)
        menu()

    def ending_f():
        nonlocal endingF
        time.sleep(4)
        print("\n")
        print("A huge hole is in your chest...")
        time.sleep(4)
        print("You feel... dizzy...")
        time.sleep(5)
        print("You are dying slowly")
        time.sleep(3)
        print("As the massive mutation of appendages and flesh lurks over you..")
        time.sleep(3)
        print("You feel dissatisfaction and depression looming over you")
        time.sleep(5)
        print("The horrific weapon approaches you")
        time.sleep(5)
        print("It opens its repulsive jaw, ready to devour you")
        time.sleep(5)
        print("You feel pain then it stops... You have been killed")
        time.sleep(3)
        print("...")
        time.sleep(3)
        print("3 weeks later...")
        time.sleep(4)
        print("TV: As the city becomes infected with this plague")
        time.sleep(3)
        print("TV: The police force has struggled to contain it, there is no signs of military presence ")
        time.sleep(5)
        print("TV: We need urgent hel- *TV switches off*")
        time.sleep(3)
        print("Man: 'What we need you to do...' ")
        time.sleep(2)
        print("Man: 'is to work with us. Captain Chambers' ")
        time.sleep(3)
        print("Man: 'As far as i am aware, the incident never happened did it?' ")
        time.sleep(3)
        print("Man: 'Of course unless you want your family to suffer i think you should co-operate with us' ")
        time.sleep(4)
        print("Man: 'Now tell me, what do you know?' ")
        time.sleep(4)
        print("Josh: 'I don't know anything about the creature or that dead test subject")
        time.sleep(3)
        print("Man: 'Good kid, you are making the right choice'")
        time.sleep(3)
        print("Man: 'At least combat data from that fight between the weapon and him is valuable'")
        time.sleep(3)
        print("Man: 'The money made it all worth it'")
        time.sleep(4)
        print("Man: 'Now i will enjoy my profits while the beast and it's plague kills this pathetic city' ")
        time.sleep(6)
        print("Man: 'However... I think a new test subject will be great for our next weapon' ")
        time.sleep(4)
        print("Man: 'Guards, sedate him' ")
        time.sleep(4)
        print("Josh: 'No-no, please, don't do this, NO. NOOO--' ")
        time.sleep(3)
        print("Man: 'Erase his memory, and preserve him for the next test.' ")
        time.sleep(3)
        print("Man: 'After all what's pudding without breaking a few eggs...'")
        time.sleep(2)
        print("...")
        time.sleep(2)
        print("")
        print("You have concluded with a bad ending")
        time.sleep(4)
        print("You have unlocked Ending F")
        endingF = True
        time.sleep(2)
        menu()

    def ending_e():
        nonlocal endingE
        time.sleep(4)
        print("\n")
        print("A huge hole is in your chest...")
        time.sleep(4)
        print("You feel... dizzy...")
        time.sleep(4)
        print("You are dying slowly")
        time.sleep(3)
        print("As the massive mutation of appendages and flesh consumes your ally...")
        time.sleep(3)
        print("You feel dissatisfaction and depression looming over you")
        time.sleep(4)
        print("The horrific weapon approaches you")
        time.sleep(5)
        print("It opens its repulsive jaw, ready to devour you")
        time.sleep(5)
        print("You feel pain then it stops... You have been killed")
        time.sleep(3)
        print("and the world will be changed... forever")
        time.sleep(3)
        print("")
        print("You have concluded with a bad ending")
        time.sleep(4)
        print("You have unlocked Ending E")
        endingE = True
        time.sleep(2)
        menu()

    def ending_c():
        nonlocal endingC
        time.sleep(4)
        print("\n")
        print("The beast has fallen")
        time.sleep(4)
        print("...but you need to get out")
        time.sleep(3)
        print("You run to the double doors and you open them, very easily")
        time.sleep(5)
        print("leaving the place behind with a fleshy abomination on the floor")
        time.sleep(3)
        print("Then the bright light of a helicopter blinds you")
        time.sleep(5)
        print("Suddenly some people take you down")
        time.sleep(3)
        print("Man 1: 'You are coming with us'")
        time.sleep(3)
        print("Man 1: 'We have detained Subject 7 OVER'")
        time.sleep(3)
        print("Man on radio: 'That's good bring hi-'")
        time.sleep(3)
        print("Man on radio: 'There's been a change of plan'")
        time.sleep(4)
        print("somewhere else...")
        time.sleep(3)
        print("Boss: 'There's been a change of plan")
        time.sleep(5)
        print("Boss: 'Kill him")
        time.sleep(3)
        print("Boss: 'And execute order C6, we cannot allow anyone to discover what happened there'")
        time.sleep(2)
        print("Boss: 'This has hindered us alot, we've lost vital pieces of information' ")
        time.sleep(3)
        print("Boss: 'But not to worry' ")
        time.sleep(3)
        print("Boss: 'There are plenty more facilities and plenty more test subjects at our disposal' ")
        time.sleep(4)
        print("Radio Man: 'Sir, i'm getting reports of gunfire from other people' ")
        time.sleep(4)
        print("Radio Man: 'They seem to be officers at the WCPD'")
        time.sleep(3)
        print("Boss: 'How did they get here????'")
        time.sleep(3)
        print("Boss: 'It seems that they were a search party but we are somehow losing men'")
        time.sleep(3)
        print("Boss: 'Kill them'")
        time.sleep(4)
        print("Radio Man: 'But sir they'd-' ")
        time.sleep(6)
        print("Boss: 'THE COMPANY WILL FIGURE SOMETHING OUT' ")
        time.sleep(4)
        print("Boss: 'Kill them and retrieve whatever data you can from the lab' ")
        time.sleep(4)
        print("Boss: 'We let the beast loose in the labs'")
        time.sleep(3)
        print("Boss: 'But i believe those idiot scientists didn't send every vital piece of data or equipment...'")
        time.sleep(3)
        print("Boss: 'back to the company when we gave the order last week' ")
        time.sleep(2)
        print("Boss: 'Now give them the order to sort the rest of this out' ")
        time.sleep(2)
        print("...")
        time.sleep(3)
        print("")
        print("You have concluded with a neutral ending")
        time.sleep(4)
        print("You have unlocked Ending C")
        endingC = True
        time.sleep(2)
        menu()

    def ending_b():
        nonlocal endingB
        time.sleep(4)
        print("\n")
        print("The beast has fallen, you have killed it")
        time.sleep(4)
        print("...but at the cost of a friend")
        time.sleep(3)
        print("'*cough* *cough* listen.. w-we did it... right?'")
        time.sleep(4)
        print("'But now *cough* you need to leave")
        time.sleep(4)
        print("'Here's the key to the exit'")
        time.sleep(5)
        print("'and here is a tape, a tape proving this place *cough* proving that it's messed up'")
        time.sleep(4)
        print("'I found this after you left, this has the evidence of the whole incident here'")
        time.sleep(4)
        print("'Give this to the WCPD, *cough* talk to a man named Jack Reeves'")
        time.sleep(4)
        print("'Out of all that corrupted police force, he's the only one I trust the most'")
        time.sleep(3)
        print("'Thank you for everything you have done, If only i *cough* made it'")
        time.sleep(4)
        print("'and if you somehow can...'")
        time.sleep(3)
        print("'Tell my sister Ciara and my family that i love them all'")
        time.sleep(3)
        print("'Here is my ID tag and here is my radio'")
        time.sleep(2)
        print("'Now GO, quickly before anyone tied to this place catches you' ")
        time.sleep(3)
        print("You took what he gave you and run towards the double doors")
        time.sleep(3)
        print("Using the key you manage to open them ")
        time.sleep(4)
        print("You run from the cursed place into the forest, without looking back")
        time.sleep(4)
        print("Suddenly you see a helicopter fly over the forest, it hasn't seen you")
        time.sleep(3)
        print("You keep running while hearing gunfire")
        time.sleep(3)
        print("...")
        time.sleep(5)
        print("Exhausted, you are on the edge of the city")
        time.sleep(4)
        print("You decide to use the radio")
        time.sleep(4)
        print("You: 'Is anyone hearing? hello?' ")
        time.sleep(4)
        print("You: 'I said is anyone hearing me???' ")
        time.sleep(4)
        print("Man: 'Who the hell is this? How do you have an officer's radio?'")
        time.sleep(3)
        print("You: 'Are you Jack Reeves??'")
        time.sleep(2)
        print("Jack: 'How do you know me??' ")
        time.sleep(2)
        print("You: 'I need you to come get me, only you' ")
        time.sleep(3)
        print("You: 'Your friend and I have been through a nightmare and you are the only person he trusts'")
        time.sleep(3)
        print("Jack: 'I will get you but where on earth is Josh??@")
        time.sleep(4)
        print("You: I will tell you everything but one thing to note...")
        time.sleep(5)
        print("You: 'Josh and I have went through hell...")
        time.sleep(5)
        print("but i was the only one who came back alive...'")
        time.sleep(3)
        print("...")
        time.sleep(4)
        print("")
        print("You have concluded with a ending that is a twist of the truth")
        time.sleep(4)
        print("You have unlocked Ending B")
        endingB = True
        time.sleep(2)
        menu()

    def ending_a():
        nonlocal endingA
        time.sleep(4)
        print("\n")
        print("The beast has fallen, you have killed it alongside Josh Chambers")
        time.sleep(4)
        print("'Rot in hell, you freak'")
        time.sleep(3)
        print("'Well we did it but the building seems like it will collapses'")
        time.sleep(4)
        print("'That thing has damaged the place alot'")
        time.sleep(4)
        print("Parts of the building start to fall")
        time.sleep(5)
        print("'Let's move!'")
        time.sleep(3)
        print("You run with Josh towards the double doors and he unlocks them with a key")
        time.sleep(4)
        print("'I found the key but I couldn't use it obviously because the Behemoth wasn't dead'")
        time.sleep(5)
        print("'Run towards the forest'")
        time.sleep(3)
        print("You both get out of there and into the cover of the trees")
        time.sleep(4)
        print("then you both hear a helicopter flying over")
        time.sleep(3)
        print("'Duck down, I think it's the chopper being to the scum who own the mansion")
        time.sleep(3)
        print("The helicopter goes past, you both have been left unseen")
        time.sleep(2)
        print("Josh: 'That was close, now tell me, how did you end up in that place' ")
        time.sleep(3)
        print("You: 'I... I don't know'")
        time.sleep(2)
        print("Josh: 'You can't be serio-' ")
        time.sleep(3)
        print("You: 'Why would I lie Josh?! I've just been in the same hell as you'")
        time.sleep(2)
        print("You: 'I HONESTLY do not know why I was there, I woke up in one of the rooms' ")
        time.sleep(3)
        print("You: 'I can't even remember my name...'")
        time.sleep(3)
        print("You: 'I tried to look over the place to discover why I was there'")
        time.sleep(4)
        print("You: 'All i know was that there were a bunch of undead creatures...' ")
        time.sleep(3)
        print("You: 'for some reason, trying to kill the only two living people in there")
        time.sleep(3)
        print("Josh: 'Well you don't look off, you're wearing normal clothing and you look fine")
        time.sleep(5)
        print("Josh: 'Why would a random person like you be here and without any memory of who you are? ")
        time.sleep(6)
        print("You: 'That's what I wanna know but so far i ain't got a damn clue")
        time.sleep(4)
        print("Josh: 'We will need to talk about this later, right now I need to show you something' ")
        time.sleep(4)
        print("You: 'What is that?' ")
        time.sleep(4)
        print("Josh: 'It is a tape, it's the evidence of what was going on here' ")
        time.sleep(3)
        print("You: 'What is on it exactly?'")
        time.sleep(4)
        print("Josh: 'I don't have a clue, I had no way of watching it'")
        time.sleep(4)
        print("Josh: 'But it IS our only chance of getting this place proved to be a lab of illegal human experiments'")
        time.sleep(6)
        print("Josh: 'Look at the name on the side of it'")
        time.sleep(3)
        print("It reads 'Patient 32 mutation: the B1-42 Weaponised Soldier, Subject 7 test data'")
        time.sleep(4)
        print("Josh: 'We went to the mansion to investigate the disappearances'")
        time.sleep(4)
        print("Josh: 'Since these people were said to have disappeared around this area'")
        time.sleep(4)
        print("Josh: 'But there were disappearances in the city, they all add up to 38 people'")
        time.sleep(4)
        print("Josh: 'I can only assume there were up to 32 patients'")
        time.sleep(4)
        print("Josh: 'But then i do not understand what the subjects are.'")
        time.sleep(4)
        print("Josh: 'Were they unsuccessful tests?'")
        time.sleep(4)
        print("Josh: 'Whatever the case may be, we need to investigate this'")
        time.sleep(4)
        print("You: 'We may have all this but where are we going to go with this?'")
        time.sleep(4)
        print("Josh: 'I know only one person who I can trust at the police station'")
        time.sleep(4)
        print("Josh: 'We can meet with him and view this tape'")
        time.sleep(3)
        print("You: 'Let's go then, we can't be waiting around here")
        time.sleep(3)
        print("somewhere else")
        time.sleep(3)
        print("Boss: 'I trust we have detained Subject 7?'")
        time.sleep(3)
        print("Man: 'No sir, we have the footage of him killing the B1-42 and leaving with another man'")
        time.sleep(4)
        print("Man: 'and the mansion is collapsing, we will try t-' *radio shuts*")
        time.sleep(3)
        print("Boss: 'Damn it'")
        time.sleep(4)
        print("Boss: 'I knew you were stubborn but to betray our company?'")
        time.sleep(4)
        print("Boss: 'to try and 'expose' us?'")
        time.sleep(4)
        print("Boss: 'I built a massive company to give us financial security'")
        time.sleep(4)
        print("Boss: 'Instead your 'morals' have blinded you from what could have been'")
        time.sleep(4)
        print("Boss: 'Even when we erased your memory and used you as a test subject...'")
        time.sleep(3)
        print("Boss: 'you survive the ultimate weapon and cause more destruction'")
        time.sleep(3)
        print("Boss: 'A rogue scientist eh?'")
        time.sleep(2)
        print("Boss: 'Well it seems you have become quite an inconvience for me, DR THOMPSON'")
        time.sleep(4)
        print("Boss: 'It is quite a shame your poor wife will never see you alive again...")
        time.sleep(4)
        print("...but fortunately, we can make her forget all about it...'")
        time.sleep(3)
        print("...")
        time.sleep(4)
        print("")
        print("Well Done! You finished the game with the True ending")
        time.sleep(4)
        print("You have unlocked Ending A")
        endingA = True
        time.sleep(2)
        menu()

    #rooms  #they all have a variety of choices and some places will have repetitive enemy encounters
    def locked_door():
        nonlocal inventory
        nonlocal weapon_list
        nonlocal MH_key_taken
        nonlocal survivor_met
        print("")
        time.sleep(2)
        print("You walk into a small hallway")
        time.sleep(3)
        print("There is a vent next to a door to the Main Hall")
        time.sleep(2)
        if survivor_met == True:
            print("THE EXIT OUT OF THIS PLACE")
            time.sleep(2)
            print("This is the final boss' location")
            time.sleep(2)
            print("*You will not be able to go back to any other rooms*")
            time.sleep(2)
        else:
            print("This seems to be the way out")
            time.sleep(2)
        print("It is locked though, you need a key")
        print("What will you do:")
        time.sleep(2)
        print("(1) Bash the door")
        print("(2) Return to the room")
        print("(3) Pull open the vent")
        for weapon in weapon_list:
            if weapon == "Screwdriver":
                print("(4) Open the vent cover using the screwdriver")
        if MH_key_taken == True:
            print("(5) Use the main hall key")
        move = False

        while move == False:
            choice = input("> ")
            if choice == "1":
                time.sleep(1)
                print("You bash the door")
                time.sleep(2)
                print("It still won't open")
            elif choice == "2":
                time.sleep(1)
                print("You return to the other room")
                move = True
                damaged_room()
            elif choice == "3":
                time.sleep(2)
                print("You pull the vent, but it won't budge")
            elif choice == "4":
                for weapon in weapon_list:
                    if weapon == "Screwdriver":
                        time.sleep(1)
                        print("You open the vent cover ")
                        time.sleep(2)
                        print("and go through what seems to be the end...")
                        time.sleep(2)
                        behemoth_fight()
            elif choice == "5" and MH_key_taken == True:
                time.sleep(1)
                print("You unlocked the door.")
                time.sleep(1)
                print("This is the final boss, you enter the room.")
                behemoth_fight()

    def damaged_room():
        nonlocal plant_killed
        time.sleep(1)
        print("You come into a room lit by old lamps")
        time.sleep(2)
        print("Surrounding you is a bunch of corpses and bullet shells")
        time.sleep(3)
        print("It seems someone was killing these monster")
        time.sleep(2)
        print("Stay alert, there may be something lurking around")
        time.sleep(3)
        print("However, you may find alot of useful items you can use")
        time.sleep(3)
        print("What will you do:")
        time.sleep(2)
        print("(1) Search the corpses")
        print("(2) Search the room")
        print("(3) go to another room")

        choice = input("> ")
        if choice == "1":
            time.sleep(1)
            print("You search the corpses")
            time.sleep(2)
            undead("and you get attacked by an undead")
            time.sleep(2)
            print("")
            time.sleep(2)
        elif choice == "2":
            time.sleep(1)
            print("You quickly scavenge the room")
            time.sleep(2)
            print("You find a few items")
        time.sleep(1)
        print("Where would you like to go?")
        time.sleep(2)
        print("(1) Go to through the upper corridor ")
        print("(2) Go to through the lower corridor ")
        print("(3) Go to the room ahead of you")
        if plant_killed == False:
            print("(4) Open the closet")
        move = False

        while move == False:
            choice = input("> ")
            if choice == "1":
                move = True
                corridor_ba()
            elif choice == "2":
                move = True
                corridor_dc()
            elif choice == "3":
                move = True
                locked_door()
            elif choice == "4" and plant_killed == False:
                plant_beast()
                time.sleep(2)
                print("You find a set of keys, they seem to be the main house keys")
                time.sleep(3)
                print("You take them with you")
                inventory.append("Main Hall Key")
                time.sleep(2)
                print("You also find a shotgun")
                shotgun()
                plant_killed = True

    def the_lab():
        nonlocal inventory
        time.sleep(1)
        print("You walk down a narrow white stairway")
        time.sleep(2)
        print("...")
        time.sleep(2)
        print("What has happened???")
        time.sleep(2)
        print("You see a bunch of dead scientists on the ground")
        time.sleep(2)
        print("The pale complexion of the lab painted in blood red")
        time.sleep(3)
        print("There are workstations that are trashed.")
        time.sleep(2)
        print("And large pods, shattered")
        time.sleep(2)
        print("What on earth happened here??")
        time.sleep(2)
        print("The room, a huge mess")
        time.sleep(2)
        print("What will you do?")
        time.sleep(2)
        print("")
        print("(1) Look over the pods")
        print("(2) Search the workstations")
        print("(3) Check the corpses")
        event = 3

        while True:
            choice = input("> ")
            if choice == "1":
                print("You approach the pods and see that they have been smashed")
                time.sleep(3)
                print("However there is something intriguing about the pod in front of you")
                time.sleep(3)
                print("The rest have been completely smashed")
                time.sleep(3)
                print("...yet this one is only smashed from one side")
                time.sleep(2)
                print("Something broke out of it")
                time.sleep(2)
                print("And that thing must've caused a massacre")
                time.sleep(2)
                print("What will you do?")
                event = event - 1
            elif choice == "2":
                print("The workstations are all trashed with documents")
                time.sleep(3)
                print("the computers are all broken")
                time.sleep(3)
                print("You check around to find anything of use")
                time.sleep(3)
                print("you then stumble upon a long rectangular case on top of one of the desks")
                time.sleep(4)
                print("it is made of metal and has a keyboard on it")
                time.sleep(2)
                print("it seems to require a password")
                time.sleep(2)
                print("Do you want to enter a password?")
                if input("> ").startswith("y"):
                    time.sleep(1)
                    print("Enter a password")
                    time.sleep(1)
                    for item in inventory:
                        if item != "Report #14: Project Counter-measure":
                            if input("> ") == "WD.034.Thompson":
                                time.sleep(1)
                                print("You have unlocked the case")
                                time.sleep(1)
                                print("And see a weapon inside")
                                time.sleep(1)
                                print("The 'BWCR V0.8'")
                                time.sleep(2)
                                print("The BioWeapon Countermeasure Rifle")
                                time.sleep(3)
                                BWCR()
                            else:
                                time.sleep(1)
                                print("You have unlocked the case")
                                time.sleep(1)
                                print("And see a weapon inside")
                                time.sleep(1)
                                print("The 'BWCR V0.8'")
                                time.sleep(2)
                                print("The BioWeapon Countermeasure Rifle")
                                time.sleep(3)
                        elif item == "Report #14: Project Counter-measure":
                            time.sleep(1)
                            print("You've read the report and it mentions a countermeasure ")
                            time.sleep(2)
                            print("An experimental rifle, this must be it")
                            time.sleep(2)
                            print("Behind the paper is a code of some sort")
                            time.sleep(1)
                            print("You enter the code WD.034.Thompson")
                            time.sleep(1)
                            print("You have unlocked the case")
                            time.sleep(1)
                            print("And see a weapon inside")
                            time.sleep(1)
                            print("The 'BWCR V0.8'")
                            time.sleep(2)
                            print("'The BioWeapon Countermeasure Rifle'")
                            BWCR()
                            event = event - 1
            elif choice == "3":
                print("You check the bodies")
                time.sleep(3)
                print("they were all maimed and disfigured")
                time.sleep(3)
                print("However, there is one body that remains somewhat distinguishable")
                time.sleep(3)
                print("He wears a lab coat and has a gunshot wound in his head")
                time.sleep(2)
                print("On him is an ID tag, it says 'Project Leader, Ralph Burton")
                time.sleep(2)
                print("He has a casette tape in a recorder on him")
                time.sleep(2)
                print("You play the tape:")
                time.sleep(3)
                print("Man: 'DAMN IT, IS THIS THING WORKING?'")
                time.sleep(2)
                print("Man: 'This is RALPH BURTON, the leader of the behemoth project'")
                time.sleep(3)
                print("Ralph: 'If anyone finds this, the B1-42 has been released, it is destroying this lab'")
                time.sleep(4)
                print("Ralph: 'I don't know if it was that Thompson or what'")
                time.sleep(3)
                print("Ralph: 'He's been missing for a day, i don't know'")
                time.sleep(3)
                print("Ralph: 'But you guys NEED to contain this thing'")
                time.sleep(4)
                print("Ralph: 'I cannot use the countermeasure'")
                time.sleep(3)
                print("Ralph: 'Thompson was the only one who knew the damn password'")
                time.sleep(3)
                print("*horrific monster shriek*")
                time.sleep(5)
                print("Ralph: 'No *gunshot* NOO, I won't let you kill me, we created you' ")
                time.sleep(5)
                print("Ralph: 'You won't harm me... I made you *gunshot*'")
                time.sleep(3)
                print("The tape ends with a massive thud")
                time.sleep(2)
                print("You pick up the tape")
                inventory.append("Ralph's Tape")
                event = event - 1
            if event == 0:
                time.sleep(2)
                print("You notice a giant caved in hole")
                time.sleep(2)
                print("Was this how the creature left the lab, under the ground?")
                time.sleep(3)
                print("Suddenly he ground shakes then an alarm blares")
                time.sleep(3)
                print("Automated message: 'Lockdown Initiated'")
                time.sleep(3)
                print("The door is closing!!")
                time.sleep(2)
                print("You run up the stairs as quick as you can")
                time.sleep(2)
                print("Just as the door closes, you make it past")
                cellar()

    def survivor_event():
        nonlocal inventory
        nonlocal behemoth_info
        nonlocal ally
        nonlocal ally_dead
        nonlocal survivor_met
        time.sleep(1)
        print("You come into the room and...")
        time.sleep(2)
        print("*gun cocks*")
        time.sleep(2)
        print("'Stay where you are! I-I don't want you near me'")
        time.sleep(4)
        print("A survivor! He may know what is going on here")
        time.sleep(1)
        print("but he looks to be on the verge of insanity")
        time.sleep(2)
        print("Choose your words wisely...")
        time.sleep(1)
        print("(1) 'Easy, put the gun down, I won't hurt you")
        print("(2) 'Who are you and what has happened to this whole place?'")
        print("(3) 'Get out of my way or you will die.'")

        while True:
            dialogue = input("> ")
            if dialogue == "1":
                time.sleep(1)
                print("'Oh yeah? Why should i believe you???'")
                time.sleep(2)
                print("'You've seen what's happened! It's a living hell!'")
                time.sleep(2)
                print("'I won't believe that you are not thinking about killing me right now!!!'")
                time.sleep(3)
                print("(1) 'If you kill me, you will have an innocent person's blood on your hands'")
                print("(2) 'I will fight you if I have to, don't make me do it.'")

                while True:
                    dialogue_a = input("> ")
                    if dialogue_a == "1":
                        time.sleep(1)
                        print("He looks at you with anger, but it turns into sadness.")
                        time.sleep(2)
                        print("He drops to his knees, dropping his weapon, ashamed.")
                        time.sleep(3)
                        print("'Look at me, I've turned into a monster!'")
                        time.sleep(2)
                        print("'I'm sorry, I'm so sorry'")
                        time.sleep(2)
                        print("'My squad are all dead, we were trying to do our job.'")
                        time.sleep(2)
                        print("'A weapon they said... a retrieval they said...")
                        time.sleep(2)
                        print("Yet they don't tell us that weapon is a huge satanic beast who murdered us all!!!")
                        time.sleep(3)
                        print("(1) 'A beast killed all your friends? What?'")
                        print("(2) 'This weapon slaughtered you all?'")
                        print("(3) 'Can i please go? I want to get out of here'")
                        if first_encounter_info_found == True:
                            print("(4) 'Wait i think i found one of your guys, was his name Anthony")

                        while True:
                            dialogue_ab = input("> ")
                            if dialogue_ab == "1":
                                time.sleep(1)
                                print("'Yes. We were sent to investigate the disappearances of people'")
                                time.sleep(2)
                                print("'We never got told that there was a HELLISH DEMON involved'")
                                time.sleep(2)
                                print("'It needs to be stopped'")
                                time.sleep(2)
                                print("'You must kill it, please'")
                                time.sleep(1)
                                print("'It must never be unleashed into the world'")
                                time.sleep(2)
                                print("(1) 'If it killed your squad, how could i ever take it down?'")
                                print("(2) 'I will try but you need to tell me all of what you know'")
                                print("(3) 'I won't be able to, I'm sorry but we need to get out'")
                                while True:
                                    dialogue_aba = input("> ")
                                    if dialogue_aba == "1":
                                        time.sleep(1)
                                        print("'What am i thinking'")
                                        time.sleep(2)
                                        print("'How can i send you to your death like that'")
                                        time.sleep(3)
                                        print("...")
                                        time.sleep(2)
                                        print("'It's a weapon you know'")
                                        time.sleep(2)
                                        print("'Under the title of the B1-42 Weaponised Soldier'")
                                        time.sleep(2)
                                        print("'Codename: THE BEHEMOTH'")
                                        time.sleep(2)
                                        print("'I found a set of blueprints'")
                                        time.sleep(2)
                                        print("'Turns out these weapons are going to be used for war'")
                                        time.sleep(2)
                                        print("'Someone was going to sell these weapons and make a profit out of them'")
                                        time.sleep(2)
                                        print("'Good God, It's crazy'")
                                        time.sleep(2)
                                        print("'We need to kill the beast, We need to stop it'")
                                        time.sleep(2)
                                        print("'I will clear the rest of this place'")
                                        time.sleep(2)
                                        print("'Then I will help you kill this thing'")
                                        time.sleep(2)
                                        print("'It is in the main hall: The only way out of this place'")
                                        time.sleep(1)
                                        print("'Take these things and my revolver")
                                        loot()
                                        revolver()
                                        time.sleep(2)
                                        print("'Don't worry, I still have a weapon on me")
                                        time.sleep(3)
                                        print("'By the way...")
                                        time.sleep(2)
                                        print("'I'm Joshua Chambers, captain of the WCPD'S T.W.A.R.S unit'")
                                        time.sleep(3)
                                        print("Best to introduce myself to a kind stranger")
                                        time.sleep(3)
                                        print("Now let's get going")
                                        time.sleep(2)
                                        print("He gives you a report - 'Report #14: Project Counter-measure'")
                                        time.sleep(2)
                                        print("You left Josh Chambers in that room")
                                        time.sleep(2)
                                        print(" * He will join you later *")
                                        time.sleep(2)
                                        inventory.append("Report #14: Project Counter-measure")
                                        ally = True
                                        behemoth_info = True
                                        survivor_met = True
                                        time.sleep(2)
                                        damaged_room()

                                    elif dialogue_aba == "2":
                                        time.sleep(1)
                                        print("'Thank you, I will tell you what I know'")
                                        time.sleep(2)
                                        print("'That monster is a weapon'")
                                        time.sleep(3)
                                        print("'I discovered this when i found these blueprints inside the mansion'")
                                        time.sleep(3)
                                        print("'This is the B1-42 Weaponised Soldier, codename: THE BEHEMOTH'")
                                        time.sleep(3)
                                        print("'It seems that this thing was being created to be sold as a super soldier'")
                                        time.sleep(4)
                                        print("'A war machine that can wipe out any threat'")
                                        time.sleep(3)
                                        print("'It seems there are keen buyers who want a thing like this, good God...'")
                                        time.sleep(3)
                                        print("'This house was being used as a cover up for a testing lab'")
                                        time.sleep(3)
                                        print("'The lab is somewhere in this place, concealed I know it")
                                        time.sleep(3)
                                        print("'Here's a report I have, it may help you find it'")
                                        time.sleep(3)
                                        print("You take Report #14: Project Counter-measure")
                                        inventory.append("Report #14: Project Counter-measure")
                                        time.sleep(3)
                                        print("'I don't know if can be found'")
                                        time.sleep(2)
                                        print("'but about the creature...'")
                                        time.sleep(3)
                                        print("'I believe it is in the main hall: The way to get out'")
                                        time.sleep(2)
                                        print("'So it needs to be killed,'")
                                        time.sleep(2)
                                        print("'Here are some items that may help you")
                                        time.sleep(2)
                                        finding(3)
                                        time.sleep(2)
                                        print("'I'm Joshua Chambers, Captain of the WCPD's T.W.A.R.S unit'")
                                        time.sleep(3)
                                        print("'I must for now block the vent after you leave'")
                                        time.sleep(2)
                                        print("'God knows what other beasts may be lurking around'")
                                        time.sleep(2)
                                        print("'I can't wait to see that thing's dead body'")
                                        time.sleep(1)
                                        print("'Thank you, God be with you and good luck'")
                                        time.sleep(1)
                                        print("You left Cpt Josh Chambers in the room.")
                                        print(" * He may join you later *")
                                        behemoth_info = True
                                        ally = True
                                        survivor_met = True
                                        damaged_room()

                                    elif dialogue_aba == "3":
                                        time.sleep(1)
                                        print("''We' don't need to do anything.'")
                                        time.sleep(1)
                                        print("My squad got killed..")
                                        time.sleep(1)
                                        print("'Trying to help heartless scum like you'")
                                        time.sleep(3)
                                        print("'but you can't even do something for the greater good of humanity'")
                                        time.sleep(2)
                                        print("'Oh and did I tell you? The main hall is the ONLY way out'")
                                        time.sleep(2)
                                        print("and it is blocked by that psychopathic mutant")
                                        time.sleep(2)
                                        print("'NOW GET OUT'")
                                        time.sleep(2)
                                        print("You left a hopeless broken man in pain, inside that room")
                                        print("")
                                        survivor_met = True
                                        damaged_room()

                            elif dialogue_ab == "2":
                                time.sleep(1)
                                print("'Yes. A weapon made from the same people who hired us to 'retreive' it'")
                                time.sleep(3)
                                print("'These evil people created this thing as a weapon of war'")
                                time.sleep(2)
                                print("'You must kill it, please'")
                                time.sleep(1)
                                print("'It is a creature of hell'")
                                time.sleep(2)
                                print("(1) 'If it killed your squad, how could i ever take it down?'")
                                print("(2) 'I will try'")
                                print("(3) 'I won't be able to, I'm sorry but we need to get out'")

                                while True:
                                    dialogue_abb = input("> ")
                                    if dialogue_abb == "1":
                                        time.sleep(1)
                                        print("'It is weak right now, we managed to hurt it'")
                                        time.sleep(2)
                                        print("'But you're right, you don't have to try and kill it'")
                                        time.sleep(3)
                                        print("'If you do encounter that thing, be as well equipped as you can.'")
                                        time.sleep(3)
                                        print("'And make the right choices'")
                                        time.sleep(1)
                                        print("'I will stay here, but take these items, they may help")
                                        time.sleep(2)
                                        print("'After you leave, you won't be able to come back, the vent will be blocked'")
                                        time.sleep(3)
                                        print("'God be with you and good luck'")
                                        time.sleep(1)
                                        print("You left the survivor in that room")
                                        time.sleep(3)
                                        survivor_met = True
                                        damaged_room()

                                    elif dialogue_abb == "2":
                                        time.sleep(1)
                                        print("'Thank you! The behemoth has been hurt so you may have an advantage'")
                                        time.sleep(3)
                                        print("'I believe he is in the main hall: The way to get out'")
                                        time.sleep(2)
                                        print("'Be prepared to fight it'")
                                        time.sleep(2)
                                        print("'I have a report talkinng a about a countermeasure'")
                                        time.sleep(3)
                                        print("You take Report #14: Project Counter-measure")
                                        inventory.append("Report #14: Project Counter-measure")
                                        time.sleep(3)
                                        print("'Here are some items that may help you")
                                        time.sleep(2)
                                        print("'And take my revolver'")
                                        finding(2)
                                        revolver()
                                        time.sleep(2)
                                        print("'I may come to see that devil's corpse'")
                                        time.sleep(3)
                                        print("'I must for now block the vent after you leave")
                                        time.sleep(2)
                                        print("'So that none of the undead can come in'")
                                        time.sleep(2)
                                        print("'Thank you, avenge my friends and may God be with you and good luck'")
                                        time.sleep(1)
                                        print("You left the survivor in the room but he may join you later")
                                        ally = True
                                        behemoth_info = True
                                        survivor_met = True
                                        damaged_room()

                                    elif dialogue_abb == "3":
                                        time.sleep(1)
                                        print("''We' don't need to do anything.'")
                                        time.sleep(3)
                                        print("'Just get out of here and don't come back'")
                                        time.sleep(2)
                                        print("'or else.'")
                                        time.sleep(2)
                                        print("'And watch your back...'")
                                        time.sleep(1)
                                        print("'if the behemoth decides to attack you'")
                                        time.sleep(2)
                                        print("You left a hopeless broken survivor in that room")
                                        survivor_met = True
                                        damaged_room()

                            elif dialogue_ab == "3":
                                time.sleep(1)
                                print("'You want to leave?? LEAVE.")
                                time.sleep(2)
                                print("'But mark my words. You will be finished once the beast gets to you'")
                                time.sleep(3)
                                print("'And nobody will remember or care.'")
                                time.sleep(2)
                                print("'Just like how me and my friends were left here to die'")
                                time.sleep(2)
                                print("'NOW GET OUT.'")
                                time.sleep(2)
                                print("You leave a empty shell of a man in that room")
                                survivor_met = True
                                damaged_room()

                    elif dialogue_a == "2":
                        time.sleep(1)
                        print("'I am not making you do ANYTHING'")
                        time.sleep(1)
                        print("'You want me dead...'")
                        time.sleep(1)
                        print("But that is not going to happen...")
                        survivor_snapped()
                        print("You leave the room with a man dead on the floor")
                        survivor_met = True
                        ally_dead = True
                        damaged_room()

            elif dialogue == "2":
                time.sleep(1)
                print("'WHO AM I???!!'")
                time.sleep(2)
                print("'I am a person who saw their squad get maliciously killed and eaten...'")
                time.sleep(3)
                print("'BY A SATANIC BEHEMOTH.'")
                time.sleep(2)
                print("'An emotionless killing machine.'")
                time.sleep(2)
                print("'A sociopathic assassin.'")
                time.sleep(2)
                print("'A weapon with one purpose to kill.'")
                time.sleep(2)
                print("'A creation from corrupted war mongers'")
                time.sleep(2)
                print("'Who sentenced my squad to dead'")
                time.sleep(2)
                print("'It has to be killed...'")
                time.sleep(2)
                print("'And you will kill it for me'")
                time.sleep(2)
                print("'...otherwise i will end your life.'")
                behemoth_info = True
                time.sleep(2)
                print("(1) 'You kill me and you will be as bad as the creature")
                print("(2) 'Are you willing to kill me, a living person who wants to get hell out of here?'")
                print("(3) 'Get out of my way or you will die.'")
                if first_encounter_info_found == True:
                    print("(4) 'Have you seen what happened to Harvey? He is dead'")

                while True:
                    dialogue_b = input("> ")
                    if dialogue_b == "1":
                        time.sleep(2)
                        print("'DON'T COMPARE ME TO THAT EVIL DEMON!!!'")
                        time.sleep(2)
                        print("'...I'M GONNA END YOU.'")
                        survivor_snapped()
                        time.sleep(2)
                        print("You left the room")
                        survivor_met = True
                        ally_dead = True
                        damaged_room()

                    elif dialogue_b == "2":
                        time.sleep(1)
                        print("He looks at you with anger, but it turns into sadness")
                        time.sleep(2)
                        print("He drops to his knees, dropping his weapons as well")
                        time.sleep(3)
                        print("'All i want is for it to be dead'")
                        time.sleep(2)
                        print("'Please, it is weak from the damage my unit did to it'")
                        time.sleep(2)
                        print("The only way out is through the main hall")
                        time.sleep(3)
                        print("(1) 'I will try to kill this creature'")
                        print("(2) 'Do you have anything to help me with'")
                        print("(3) 'Be safe, I'm going to get out of here'")

                        while True:
                            dialogue_bb = input("> ")
                            if dialogue_bb == "1":
                                time.sleep(1)
                                print("'Thank you, I will tell you what I know about the thing'")
                                time.sleep(1)
                                print("'That monster is a weapon'")
                                time.sleep(3)
                                print("'I discovered this when i found these blueprints inside the mansion'")
                                time.sleep(2)
                                print("'This is the B1-42 Weaponised Soldier, codename: THE BEHEMOTH'")
                                time.sleep(2)
                                print("'They infected someone with a virus to mutate them into this creature'")
                                time.sleep(2)
                                print("'The undead and infected are afflicted with the same virus'")
                                time.sleep(2)
                                print("'Except they do not mutate into these behemoths'")
                                time.sleep(2)
                                print("'Well...'")
                                time.sleep(2)
                                print("'I guess we know why these disappearances have been happening'")
                                time.sleep(2)
                                print("'This house was being used as a cover for their laboratory'")
                                time.sleep(2)
                                print("'The lab is somewhere in this place, concealed I know it'")
                                time.sleep(2)
                                print("'I don't know if can be found'")
                                time.sleep(3)
                                print("'The lab is somewhere in this place, concealed I know it")
                                time.sleep(3)
                                print("'Here's a report I have, it may help you find it'")
                                time.sleep(3)
                                print("You take Report #14: Project Counter-measure")
                                inventory.append("Report #14: Project Counter-measure")
                                time.sleep(3)
                                print("'but about the creature'")
                                time.sleep(3)
                                print("'I believe it is in the main hall: The way to get out'")
                                time.sleep(2)
                                print("'Here are some items that may help you and my revolver'")
                                time.sleep(2)
                                finding(3)
                                revolver()
                                time.sleep(2)
                                print("'I'm Joshua Chambers, Captain of the WCPD's T.W.A.R.S unit''")
                                time.sleep(3)
                                print("'I must for now block the vent after you leave")
                                time.sleep(2)
                                print("'God knows what other beasts may be lurking around'")
                                time.sleep(2)
                                print("'I can't wait to see that thing's dead body'")
                                time.sleep(1)
                                print("'Thank you, God be with you and good luck'")
                                time.sleep(1)
                                print("You left Josh Chambers in the room.")
                                print(" * He may join you later *")
                                ally = True
                                behemoth_info = True
                                survivor_met = True
                                damaged_room()

                            elif dialogue_bb == "2":
                                time.sleep(1)
                                print("'Here, these may help'")
                                finding(2)
                                time.sleep(1)
                                print("'That monster is a weapon'")
                                time.sleep(3)
                                print("'I discovered this when i found these blueprints inside the mansion'")
                                time.sleep(2)
                                print("'This is the B1-42 Weaponised Soldier, codename: THE BEHEMOTH'")
                                time.sleep(2)
                                print("'They infect someone with a virus to mutate them into this creature'")
                                time.sleep(2)
                                print("'The undead and infected are afflicted with the same virus'")
                                time.sleep(2)
                                print("'Except they do not mutate into these behemoths'")
                                time.sleep(2)
                                print("'Well...'")
                                time.sleep(2)
                                print("'I guess we know why these disappearances have been happening'")
                                time.sleep(3)
                                print("'This house was being used as a cover for their laboratory'")
                                time.sleep(3)
                                print("'The lab is somewhere in this place, concealed I know it")
                                time.sleep(3)
                                print("'I don't know if can be found'")
                                time.sleep(3)
                                print("'The lab is somewhere in this place, concealed I know it")
                                time.sleep(3)
                                print("'Here's a report I have, it may help you find it'")
                                time.sleep(3)
                                print("You take Report #14: Project Counter-measure")
                                inventory.append("Report #14: Project Counter-measure")
                                time.sleep(3)
                                print("'but about the creature'")
                                time.sleep(3)
                                print("'I believe the beast may be in the main hall: The way out of this place'")
                                time.sleep(3)
                                print("'After you leave, you won't be able to come back, the vent will be blocked'")
                                time.sleep(2)
                                print("'God be with you.'")
                                time.sleep(1)
                                print("You left the survivor in that room")
                                survivor_met = True
                                damaged_room()


                            elif dialogue_bb == "3":
                                time.sleep(1)
                                print("'There is no safety if that thing isn't dead.'")
                                time.sleep(3)
                                print("'But go then...'")
                                time.sleep(2)
                                print("'The only exit is through the main hall.'")
                                time.sleep(2)
                                print("'The vent will be blocked, don't come back'")
                                time.sleep(2)
                                print("'Goodbye'")
                                time.sleep(2)
                                print("You leave hopeless man in that room")
                                survivor_met = True
                                damaged_room()

                    elif dialogue_b == "3":
                        time.sleep(1)
                        print("So be it... you filthy snake")
                        survivor_snapped()
                        print("You left the room")
                        survivor_met = True
                        ally_dead = True
                        damaged_room()

                    elif dialogue_b == "4" and first_encounter_info_found == True:
                        time.sleep(1)
                        print("His eyes widen")
                        time.sleep(2)
                        print("'Harvey? You found one of my friends?'")
                        time.sleep(2)
                        print("'Where is he??'")
                        time.sleep(2)
                        print("(1) 'He is in one of the hallways, he was undead when I found him'")
                        print("(2) 'Dead, as you shall be'")

                        while True:
                            dialogue_bd = input("> ")
                            if dialogue_bd == "1":
                                time.sleep(1)
                                print("'Oh my God...")
                                time.sleep(2)
                                print("'He was a tough guy'")
                                time.sleep(3)
                                print("'...but I guess all it took was a nightmare like this to do him in'")
                                time.sleep(2)
                                print("''")
                                time.sleep(2)
                                print("'The only way out is through the main hall'")
                                time.sleep(1)
                                print("'That monster is a weapon'")
                                time.sleep(3)
                                print("'I discovered this when i found these blueprints inside the mansion'")
                                time.sleep(2)
                                print("'This is the B1-42 Weaponised Soldier, codename: THE BEHEMOTH'")
                                time.sleep(2)
                                print("'They infect someone with a virus to mutate them into this creature'")
                                time.sleep(2)
                                print("'The undead and infected are afflicted with the same virus'")
                                time.sleep(2)
                                print("'Except they do not mutate into these behemoths'")
                                time.sleep(2)
                                print("'Well...'")
                                time.sleep(2)
                                print("'I guess we know why these disappearances have been happening'")
                                time.sleep(3)
                                print("'This house was being used as a cover for their laboratory'")
                                time.sleep(3)
                                print("'The lab is somewhere in this place, concealed I know it")
                                time.sleep(3)
                                print("'I don't know if can be found'")
                                time.sleep(3)
                                print("'The lab is somewhere in this place, concealed I know it")
                                time.sleep(3)
                                print("'Here's a report I have, it may help you find it'")
                                time.sleep(3)
                                print("You take Report #14: Project Counter-measure")
                                inventory.append("Report #14: Project Counter-measure")
                                time.sleep(3)
                                print("'but about the creature'")
                                time.sleep(3)
                                print("'I believe the beast may be in the main hall: The way out of this place'")
                                time.sleep(3)
                                print("'After you leave, you won't be able to come back, the vent will be blocked'")
                                time.sleep(2)
                                print("'I will come help you, just let me clear up this place'")
                                time.sleep(2)
                                print("'And take my revolver and these medkits")
                                revolver()
                                finding(2)
                                print("'Thank you, I will meet you there'")
                                time.sleep(1)
                                print("'I can't wait to see that thing's dead body'")
                                time.sleep(2)
                                print("You left Josh Chambers in the room.")
                                print(" * He may join you later *")
                                ally = True
                                behemoth_info = True
                                survivor_met = True
                                damaged_room()

                            elif dialogue_bd == "2":
                                time.sleep(1)
                                print("You won't kill me.")
                                survivor_snapped()
                                print("You left the room")
                                survivor_met = True
                                ally_dead = True
                                damaged_room()

            elif dialogue == "3":
                time.sleep(1)
                print("'YOU WON'T KILL ME IF YOU ARE DEAD")
                survivor_snapped()
                print("You left the room")
                survivor_met = True
                ally_dead = True
                damaged_room()

    def cellar():
        nonlocal cellar_enemies_dead
        nonlocal inventory
        nonlocal lab_locked
        nonlocal SR_key_taken
        num_choice = 3
        if cellar_enemies_dead == False:
            time.sleep(1)
            print("It's a cellar")
            time.sleep(1)
            print("You can go down the cellar")
            time.sleep(2)
            print("...")
            time.sleep(3)
            animal("A mutant dog leaps at you!")
            time.sleep(1)
            print("It seems that animals can become undead too")
            time.sleep(3)
            print("As you turn around...")
            time.sleep(2)
            undead("An undead lunges at you")
            time.sleep(1)
            print("Under the undead corpse, you find something.")
            pistol()
            time.sleep(1)
            print("You try to open the door but it's locked")
            time.sleep(2)
            print("You may need a key")
            time.sleep(1)
            print("What will you do now")
        elif cellar_enemies_dead == True:
            time.sleep(1)
            print("You return to the cellar")
            if lab_locked == True:
                print("and ir seems you cannot re-enter the lab")
        time.sleep(2)
        print("What will you do now")
        time.sleep(2)
        print("(1) Return to the previous room")
        print("(2) Search for another way in")
        print("(3) Bash the door in")
        for item in inventory:
            if item == "Storage Key":
                print("(4) Use the Storage Key")
        move = False

        while move == False:
            choice = input("> ")
            if choice == "1":
                move = True
                first_encounter()

            elif choice == "2":
                time.sleep(1)
                print("You look around")
                time.sleep(1)
                print("but you cannot find anything")
                num_choice = num_choice - 1
                move = False
            elif choice == "3":
                time.sleep(1)
                print("You bash the door")
                time.sleep(1)
                print("It still won't open")
                num_choice = num_choice - 1
                move = False
            elif choice == "4" and SR_key_taken == True:
                for item in inventory:
                     if item == "Storage Key":
                        print("You hear a click, the door is unlocked")
                        time.sleep(2)
                        print("You open the door...")
                        move = True
                        survivor_event()
            if num_choice == 0 and lab_locked == False:
                time.sleep(2)
                print("You notice something")
                time.sleep(2)
                print("There is a panel coming loose from the wall")
                time.sleep(2)
                print("You go up to it and tear it off")
                time.sleep(2)
                print("There is a mechanical door")
                time.sleep(2)
                print("There is also a numpad next to it")
                time.sleep(4)
                print("It requires a 4 digit combination")
                time.sleep(5)
                print("Do you want to input a passcode?")
                for item in inventory:
                    if item != "Letter 13/12/98":
                        if input("> ") == "1312":
                            time.sleep(1)
                            print("You have open the door")
                            time.sleep(1)
                            print("You go inside...")
                            the_lab()
                        elif input("> ") == "x" or input("> ") == "X":
                            time.sleep(1)
                            print("You leave the keypad")
                            time.sleep(1)
                            print("and return to the previous room")
                            time.sleep(1)
                            first_encounter()
                    elif item == "Letter 13/12/98":
                        time.sleep(1)
                        print("The letter has a date on it")
                        time.sleep(2)
                        print("The writer of the letter said it was his son's birthday")
                        time.sleep(2)
                        print("It's the only thing you've got")
                        time.sleep(1)
                        print("You enter 1312.")
                        time.sleep(1)
                        print("The door lifts up")
                        time.sleep(2)
                        print("You have open the door")
                        time.sleep(2)
                        print("You go inside...")
                        the_lab()

    def corridor_ba():
        nonlocal inventory
        nonlocal letter_taken
        if letter_taken == False:
            time.sleep(1)
            print("You open the door and see a letter on the floor")
            time.sleep(2)
            print("It is dated 13/12/98")
            time.sleep(1)
            print("You read it...")
            time.sleep(2)
            print("13/12/98:")
            print("'To my wife and son,")
            print("If you read this, I'm sorry. I'm so sorry")
            print("They made me experiments, they made me do things to innocent people")
            print("Please Carley, don't come to me, forget all about")
            print("I wasn't good enough for you, I wasn't a great husband")
            print("But I need you to listen to me if you get this")
            print("You need to take Daniel and leave Wallow City")
            print("No boy should go through this, especially on his birthday")
            print("but you need to =--/;L;.|@")
            time.sleep(25)
            print("The letter was smudged and left incomplete")
            time.sleep(2)
            time.sleep(2)
            print("* You have learnt key information and take the letter *")
            inventory.append("Letter 13/12/98")
            letter_taken = True
        else:
            time.sleep(1)
            print("You go through the corridor")
            time.sleep(2)
            print("You are cautious")
        time.sleep(2)
        print("")
        chance = random.randint(0, 2)
        if chance == 0:
            animal("A mutant dog breaks through the window")
        elif chance == 1:
            undead("An undead breaks through the window")
        time.sleep(1)
        print("You get to the end of the corridor")
        view_stats()
        first_encounter()

    def corridor_ab():
        nonlocal inventory
        nonlocal letter_taken
        chance = random.randint(0, 2)
        time.sleep(1)
        print("You go through the corridor")
        time.sleep(2)
        print("You are cautious")
        print("")
        time.sleep(2)
        if chance == 0:
            animal("A mutant dog breaks through the window")
        elif chance == 1:
            undead("An undead breaks through the window")
        time.sleep(1)
        print("You get to the end of the corridor")
        if letter_taken == False:
            time.sleep(2)
            print("There is a letter dated 13/12/98")
            time.sleep(2)
            print("You read it...")
            time.sleep(2)
            print("13/12/98:")
            print("'To my wife and son,")
            print("If you read this, I'm sorry. I'm so sorry")
            print("They made me experiments, they made me do things to innocent people")
            print("Please Carley, don't come to me, forget all about")
            print("I wasn't good enough for you, I wasn't a great husband")
            print("But I need you to listen to me if you get this")
            print("You need to take Daniel and leave Wallow City")
            print("No boy should go through this, especially on his birthday")
            print("but you need to =--/;L;.|@")
            time.sleep(25)
            print("The letter was smudged and left incomplete")
            time.sleep(2)
            print("* You have learnt key information and take the letter *")
            inventory.append("Letter 13/12/98")
            letter_taken = True
            time.sleep(2)
            print("You open the door into the next room")
        view_stats()
        damaged_room()

    def corridor_dc():
        nonlocal SR_key_taken
        nonlocal inventory
        chance = random.randint(0, 2)
        time.sleep(1)
        print("You go through the corridor")
        time.sleep(2)
        print("You are cautious")
        print("")
        time.sleep(2)
        if chance == 0:
            animal("A mutant dog breaks through the window")
        elif chance == 1:
            undead("An undead breaks through the window")
        time.sleep(1)
        print("You get to the end of the corridor")
        if SR_key_taken == False:
            time.sleep(2)
            print("..then you stumble upon a key")
            time.sleep(2)
            print("it has a label saying 'storage'")
            time.sleep(2)
            print("You take the Storage Key")
            inventory.append("Storage Key")
            SR_key_taken = True
        view_stats()
        first_item()

    def corridor_cd():
        nonlocal inventory
        nonlocal SR_key_taken
        chance = random.randint(0, 2)
        if SR_key_taken == False:
            time.sleep(1)
            print("You go through the corridor")
            time.sleep(2)
            print("..then you stumble upon a key")
            time.sleep(2)
            print("it has a label saying 'storage'")
            time.sleep(2)
            print("You take the Storage Key")
            inventory.append("Storage Key")
            SR_key_taken = True
        time.sleep(2)
        print("You go down")
        time.sleep(2)
        print("...")
        if chance == 0:
            animal("A mutant dog breaks through the window")
        elif chance == 1:
            undead("An undead breaks through the window")
        time.sleep(1)
        print("You get to the end and go into the next room")
        time.sleep(2)
        view_stats()
        damaged_room()

    def first_encounter():
        nonlocal first_encounter_event
        nonlocal first_encounter_return
        nonlocal inventory
        nonlocal survivor_met
        if first_encounter_return == False:
            time.sleep(1)
            print("You walk into a room")
            time.sleep(2)
            print("There is a door straight ahead")
            time.sleep(2)
            print("...and a door to the right ")
            time.sleep(2)
            print("by the door, there is a corpse")
        elif first_encounter_return == True:
            time.sleep(1)
            print("You return into the room")
            time.sleep(2)
            print("The body lays there")
        if first_encounter_return == False:
            print("(1) Go through the door straight ahead")
            print("(2) Go past the corpse through the door on the right")
            print("(3) Search the corpse")
        elif first_encounter_return == True:
            print("(1) Go through the door to where you start")
            print("(2) Go through the door by the body")
            print("(3) Go through the door to the corridor")
        time.sleep(2)
        print("What shall you do")
        move = False

        while move == False:
            choice = input("> ")
            if choice == "1" and first_encounter_return == False:
                time.sleep(2)
                print("You walk towards the door and go into another room")
                view_stats()
                corridor_ab()
                first_encounter_return = True
                move = True
            elif choice == "2" and first_encounter_return == False:
                time.sleep(2)
                print("You go towards the door without a second thought")
                time.sleep(2)
                print("as you try to open the door...")
                time.sleep(1)
                if first_item_event == True:
                    undead("The undead attacks")
                else:
                    first_undead()
                time.sleep(1)
                print("You continue into the next room")
                view_stats()
                cellar()
                move = True
                first_encounter_event = True
                first_encounter_return = True
            elif choice == "3" and first_encounter_return == False:
                time.sleep(2)
                print("You bend down to search the corpse's body")
                time.sleep(2)
                print("but then...")
                time.sleep(1)
                first_undead()
                time.sleep(1)
                print("You search the body")
                time.sleep(2)
                print("There is some ID on the corpse")
                time.sleep(2)
                print("He is a member of 'T.W.A.R.S'")
                time.sleep(2)
                print("'Tactical Weapons and Rescue Squad'")
                time.sleep(2)
                print("His name is Harvey Reynolds")
                time.sleep(2)
                print("Why was this police guy trying to kill you?")
                time.sleep(2)
                print("and why was his skin all rotten")
                time.sleep(2)
                print("* You have learn key information and take his ID tag *")
                inventory.append("Harvey's ID")
                time.sleep(2)
                print("He is laying next to something")
                time.sleep(2)
                finding(2)
                knife()
                first_encounter_event = True
                pass
                if choice == "1" and first_encounter_return == False:
                    time.sleep(2)
                    print("You walk towards the door and go into another room")
                    view_stats()
                    corridor_ab()
                    first_encounter_return = True
                    move = True
                elif choice == "2" and first_encounter_return == False:
                    time.sleep(2)
                    print("You go towards the door without a second thought")
                    time.sleep(2)
                    print("as you try to open the door...")
                    time.sleep(1)
                    if first_item_event == True:
                        undead("The undead attacks")
                    else:
                        first_undead()
                    time.sleep(1)
                    print("You continue into the next room")
                    view_stats()
                    cellar()
                    first_encounter_event = True
                    first_encounter_return = True
                    move = True
                elif choice == "3" and first_encounter_return == False:
                    time.sleep(2)
                    print("You bend down to search the corpse's body")
                    time.sleep(2)
                    print("but then...")
                    time.sleep(1)
                    first_undead()
                    time.sleep(1)
                    print("You search the body")
                    time.sleep(2)
                    print("There is some ID on the corpse")
                    time.sleep(2)
                    print("He is a member of 'T.W.A.R.S'")
                    time.sleep(2)
                    print("'Tactical Weapons and Rescue Squad'")
                    time.sleep(2)
                    print("His name is Harvey Reynolds")
                    time.sleep(2)
                    print("Why was this police guy trying to kill you?")
                    time.sleep(2)
                    print("and why was his skin all rotten")
                    time.sleep(2)
                    print("* You have learn key information and take his ID tag *")
                    inventory.append("Harvey's ID")
                    time.sleep(2)
                    print("He is laying next to something")
                    time.sleep(2)
                    finding(2)
                    knife()
                    first_encounter_event = True
                    pass
            if choice == "1" and first_encounter_return == True:
                    time.sleep(2)
                    print("You go through the door")
                    view_stats()
                    start()
                    move = True
            elif choice == "2" and first_encounter_return == True:
                    time.sleep(2)
                    if first_encounter_event == False:
                        print("You go towards the door without a second thought")
                        time.sleep(2)
                        print("as you try to open the door...")
                        time.sleep(1)
                        undead("The corpse attacks you")
                        first_encounter_event = True
                    time.sleep(1)
                    view_stats()
                    if survivor_met == True:
                        print("You open the door to see that you cannot go back down anymore")
                        time.sleep(2)
                        print("The stairway is blocked by debris from the ceiling")
                    else:
                        cellar()
                        move = True
                    time.sleep(2)
            elif choice == "3" and first_encounter_return == True:
                time.sleep(2)
                print("You go through the door")
                view_stats()
                corridor_ab()
            print("What shall you do")
            time.sleep(2)
            print("(1) Go through the other door")
            print("(2) Go through this door by the body")
            print("(3) Return to the previous room")
            move = False

            while move == False:
                choice_2 = input("> ")
                if choice_2 == "1":
                    time.sleep(1)
                    print("You go towards that door and into the next room")
                    view_stats()
                    corridor_ab()
                    move = True
                    first_encounter_return = True
                    time.sleep(2)
                elif choice_2 == "2":
                    time.sleep(1)
                    print("You head straight through the door")
                    first_encounter_return = True
                    view_stats()
                    if survivor_met == True:
                        print("You open the door to see that you cannot go back down anymore")
                        time.sleep(2)
                        print("The stairway is blocked by debris from the ceiling")
                    else:
                        cellar()
                        move = True
                elif choice_2 == "3":
                    print("You return to the previous room")
                    first_encounter_return = True
                    view_stats()
                    start()
                    move = True

    def first_item():
        nonlocal first_item_return
        nonlocal first_item_event
        if first_item_return == False:
            time.sleep(1)
            print("You step into a compact yet spacious room")
            time.sleep(2)
            print("The room does not have too much but it may be worth a search")
            time.sleep(3)
            print("What will you do?")
            time.sleep(2)
            print("(1) Search the room lightly")
            print("(2) Search this room thoroughly")
            print("(3) Move on to another room")

            choice = input("> ")
            if choice == "1":
                time.sleep(1)
                print("You look over the room lightly")
                time.sleep(1)
                print("and find something that may be useful")
                time.sleep(1)
                screwdriver()
            elif choice == "2":
                time.sleep(1)
                print("You take the time to turn the place over")
                time.sleep(1)
                print("You have found some items")
                finding(2)
                time.sleep(1)
                print("You see a slivering corpse coming out of a vent!")
                time.sleep(2)
                if first_encounter_event == True:
                    undead("There is an undead coming out of a vent")
                else:
                    first_undead()
                    print("That is strange, what is going on?")
                first_item_event = True

        elif first_item_return == True:
            time.sleep(1)
            print("You return to the small room")
            time.sleep(2)
            if first_encounter_event == True or first_item_event == True:
                undead("There is an undead ready to attack you")
            else:
                first_undead()
                print("That is strange, what is going on?")

        print("Where shall you go now?")
        time.sleep(2)
        print("(1) Go to the starting room")
        print("(2) Go to the corridor")
        move = False

        while move == False:
            choice_2 = input("> ")
            if choice_2 == "1":
                time.sleep(1)
                print("You go towards that door to where you started")
                time.sleep(2)
                view_stats()
                start()
            elif choice_2 == "2":
                print("You head off to the corridor")
                view_stats()
                corridor_cd()


    def view_stats(): # can view stats when you are about to leave a room
        nonlocal hp
        nonlocal atk
        nonlocal weapon_list
        nonlocal medkits
        nonlocal inventory
        time.sleep(2)
        print("Do you wish to view your inventory?")
        if input("> ").startswith("y"):
            print("HP:", hp)
            print("Atk: ", atk)
            print("Current weapon: ", weapon_list)
            print("Medkits:", medkits)
            print("Items:", inventory)
            for item in inventory:
                if item == "Letter 13/12/98":
                    print("Do you wish to read Letter 13/12/98")
                    if input("> ").startswith("y"):
                        print("13/12/98:")
                        print("'To my wife and son,")
                        print("If you read this, I'm sorry. I'm so sorry")
                        print("They made me experiments, they made me do things to innocent people")
                        print("Please Carley, don't come to me, forget all about")
                        print("I wasn't good enough for you, I wasn't a great husband")
                        print("But I need you to listen to me if you get this")
                        print("You need to take Daniel and leave Wallow City")
                        print("No boy should go through this, especially on his birthday")
                        print("but you need to =--/;L;.|@")
                    else:
                        pass
                elif item == "Report #14: Project Counter-measure":
                    print("Do you wish to read Report #14: Counter-measure Failsafe")
                    if input("> ").startswith("y"):
                        print("Project :")
                        print("'To my wife and son,")
                        print("If you read this, I'm sorry. I'm so sorry")
                        print("They made me experiments, they made me do things to innocent people")
                        print("Please Carley, don't come to me, forget all about")
                        print("I wasn't good enough for you, I wasn't a great husband")
                        print("But I need you to listen to me if you get this")
                        print("You need to take Daniel and leave Wallow City")
                        print("No boy should go through this, especially on his birthday")
                        print("but you need to =--/;L;.|@")
                    else:
                        pass
            print("Type 'x' to exit")
            if input("> ").startswith("x"):
                print("Shutting inventory")
                pass
        else:
            pass


    def start(): #ending x is found here
        nonlocal past_start
        if past_start == False:
            num_choice = 4
            time.sleep(3)
            print("")
            print("You get up...")
            time.sleep(2)
            print("and see you have 2 ways of leaving")
            time.sleep(2)
            print("(1) Go forth through the door ahead")
            print("(2) Head off through the door on your right")
            move = False

            while move == False:
                choice = input("> ")
                if choice == "1":
                    move = True
                    past_start = True
                    first_encounter()
                elif choice == "2":
                    move = True
                    past_start = True
                    first_item()
                else:
                    time.sleep(1)
                    print("You must make a valid choice")
                    num_choice = num_choice - 1
                    move = False
                if num_choice == 0:
                    ending_f()

        elif past_start == True:
            time.sleep(2)
            print("")
            print("You return to where you began")
            time.sleep(2)
            print("Where will you go?")
            time.sleep(1)
            print("(1) Go forth through the door ahead")
            print("(2) Head off through the door on your right")
            move = False

            while move == False:
                choice = input("> ")
                if choice == "1":
                    first_encounter()
                    move = True
                elif choice == "2":
                    first_item()
                    move = True

    def prologue(): #context as to why you are here
        print("")
        time.sleep(1)
        print("You awaken to find yourself in an empty mansion")
        time.sleep(3)
        print("with no memory of how you ended up inside")
        time.sleep(3)
        print("Something has happened here but what?")
        time.sleep(2)
        print("Will you escape?")
        time.sleep(2)
        print("or will you not live to tell the tale?")
        time.sleep(2)
        print("You will find out yourself...")
        print("")
        tips()

    def tips(): #gives the player some basic hints as to what to do in the game
        time.sleep(2)
        print("This game is a turn-based RPG")
        time.sleep(1)
        print("* You will need to think carefully during battles and save your medkits *")
        time.sleep(3)
        print("* Not all enemies will be easy to fight through *")
        time.sleep(3)
        print("* There are multiple endings that you can discover, including secret endings *")
        time.sleep(3)
        print("* Loot may be hard to obtain so it may be necessary to escape some enemies*")
        time.sleep(5)
        print("* There is 1 unavoidable boss encounter...")
        time.sleep(2)
        print("* and another 2 encounters that may be triggered by your choices *")
        time.sleep(3)
        print("* The other enemies will be common types *")
        time.sleep(3)
        print("")
        print("Type 'x' to start the game")
        if input("> ").startswith("x"):
            time.sleep(2)
            print("* If you die, you will have to start from the beginning *")
            time.sleep(3)
            print("*...it wasn't going to be easy now, was it? *")
            time.sleep(2)
            print("")
            print("")
            print("You are entering the world of horror survival")
            start()

    def menu():
        nonlocal endingA
        nonlocal endingB
        nonlocal endingC
        nonlocal endingE
        nonlocal endingF
        nonlocal endingX
        print(">>=====================<<")
        print("|| T H E   H O R R O R ||") #title screen
        print("||     W I T H I N     ||")
        print(">>=====================<<")
        print("")
        print("[-A short RPG by Yousuf-]") #made by me :)
        print("")
        time.sleep(3)
        print(" (1) Start Game") #play the game
        print(" (2) Unlockables") #see unlocked endings
        print(" (3) Help & Tips") #see the help and tips
        print(" (4) Exit Game") #exit the game
        set = False

        while set == False:
            choice = input("> ")
            if choice == "1":
                set = True
                prologue()
            elif choice == "2":
                set = True
                time.sleep(1)
                print("Endings:")
                time.sleep(1)
                if endingA is True:
                    print("Ending A  - Unlocked")
                else:
                    print("Ending ? - Locked")
                if endingB is True:
                    print("Ending B  - Unlocked")
                else:
                    print("Ending ? - Locked")
                if endingC is True:
                    print("Ending C  - Unlocked")
                else:
                    print("Ending ? - Locked")
                if endingE is True:
                    print("Ending E  - Unlocked")
                else:
                    print("Ending ? - Locked")
                if endingF is True:
                    print("Ending F  - Unlocked")
                else:
                    print("Ending ? - Locked")
                if endingX is True:
                    print("Secret Ending X  - Unlocked")
                else:
                    print("Secret Ending ? - Locked")
                print("")
                print("To view an ending, type in its letter to view it")
                print("or to go to the menu, press q")
                time.sleep(2)
                choice2 = input("> ")
                if choice2 == "a" or choice2 == "A" and endingA == True:
                    ending_a()
                elif choice2 == "b" or choice2 == "B" and endingB == True:
                    ending_b()
                elif choice2 == "c" or choice2 == "C" and endingC == True:
                    ending_c()
                elif choice2 == "e" or choice2 == "E" and endingE == True:
                    ending_e()
                elif choice2 == "f" or choice2 == "F" and endingF == True:
                    ending_f()
                elif choice2 == "x" or choice2 == "X" and endingX == True:
                    ending_x()
                else:
                    menu()

            elif choice == "3":
                print("This game is a turn-based RPG where your actions can matter")
                print("* You will need to think carefully during battles and save your medkits *")
                print("* Not all enemies will be easy to fight through *")
                print("* There are multiple endings that you can discover, including secret endings *")
                print("* Loot may be hard to obtain so it may be necessary to escape some enemies*")
                print("* There is 1 unavoidable boss encounter...")
                print("* and another 2 encounters that may be triggered by your choices *")
                print("* The other enemies will be common types *")
                print("* If you die, you will have to start from the beginning *")
                print("")
                print("Type X to go back to the menu?")
                choice = input("> ")
                if choice.startswith('x') == True:
                    menu()
                else:
                    menu()

            elif choice == "4":
                time.sleep(1)
                print("Are you sure you want to quit?")
                choice = input("> ")
                if choice.startswith('y') == True:
                    set = True
                    exit(0)
                else:
                    menu()

    menu()

game()



