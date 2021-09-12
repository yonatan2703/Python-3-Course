from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


print("\n\n")

# Create black magic
fire = Spell("Fire", 20, 600, "black")
thunder = Spell("Thunder", 20, 600, "black")
blizzard = Spell("Blizzard", 35, 1200, "black")
meteor = Spell("Meteor", 40, 1500, "black")
quake = Spell("Quake", 60, 2500, "black")

# Create white magic
cure = Spell("Cure", 15, 620, "white")
cura = Spell("Cura", 30, 1500, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 500 HP", 500)
hipotion = Item("Hi-Potion", "potion", "Heals 1000 HP", 1000)
superpotion = Item("Super Potion", "potion", "heals 1500 HP", 1500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
hielixir = Item("Mega-Elixir", "elixir", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 2000)

player_magic = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 5},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixir, "quantity": 5},
                {"item": hielixir, "quantity": 5},
                {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Valos:", 3260, 150, 300, 34, player_magic , player_items)
player2 = Person("Nick: ", 4160, 150, 320, 34, player_magic , player_items)
player3 = Person("Robot:", 3089, 150, 280, 34, player_magic , player_items)
enemy = Person("Ork  ", 11000, 100, 525, 25, [], [])

players = [player1, player2, player3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("==============================")

    print("\n\n")
    print("NAME                  HP                                     MP")
    for player in players:
        player.get_stats()
        
    print("\n")

    enemy.get_enemy_stats()
    
    for player in players:

        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print("You attacked for", dmg, "points of damage. Enemy HP:", enemy.get_hp())
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)

            elif (spell.type == "black"):
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg), "points of damage" + bcolors.ENDC)

        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + "heals for", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "elixir":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp

                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + "fully restores HP/MP", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + "deals", str(item.prop), "points of damage" + bcolors.ENDC)

    enemy_choice = 1
    target = random.randrange(0,3)
    enemy_dmg = enemy.generate_damage()

    players[target].take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg)


    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + "you win!" + bcolors.ENDC)
        running = False
    elif player.get_hp() == 0:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)


    # running = False