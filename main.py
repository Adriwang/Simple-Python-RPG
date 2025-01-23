import random
import linecache
import os
import math

floor: int = 0
gold:int = 100
health:int = 100
defense:int = 0
attack:int = 5
potion_cost:int = 10
base_cost:int = 100
inflation:int = 0

""" Speed beats Power, Power beats Technical, Technical beats Speed """
attack_types: list[str] = ["Power", "Speed", "Technical"]
""" Gnomes Prioritize Technical, Goblins Prioritize Power, Skeletons Prioritize Speed """
enemy_types: list[str] = ["Gnome","Goblin","Skeleton"]

def player_continue():
    input("Press Enter to Continue...")
    os.system('clear')

def shopkeeper(dialog: str):
    global gold
    global floor
    global shop_event
    global potion_cost
    global base_cost
    global inflation
    global attack
    global defense
    global health
    if receive_dialog:
        linecache.getline('dialog.txt', random.randint(7,11))
        player_continue()
    print(dialog)
    match shop_event:
        case 2:
            print("Armor Upgrade Cost = %d gold coins" % (base_cost + inflation))
            print("Current Gold =",gold)
            if gold < (base_cost + inflation):
                print("You are %d gold short" % (-1 * (gold - (base_cost + inflation))))
            else:
                user_input = input("Purchase? (y/n = default)")
                if user_input == "y" or user_input == "Y":
                    defense += 3
                    gold -= base_cost + inflation
                    print("You upgraded your armour!")
        case 3:
            print("Weapon Upgrade Cost = %d gold coins" % (base_cost + inflation))
            print("Current Gold =",gold)
            if gold < (base_cost + inflation):
                print("You are %d gold short" % (-1 * (gold - (base_cost + inflation))))
            else:
                user_input = input("Purchase? (y/n = default)")
                if user_input == "y" or user_input == "Y":
                    attack += 3
                    gold -= base_cost + inflation
                    print("You Purchased an upgraded Weapon!")
        case 4:
            if health == 100:
                print("But your health is already full")
            else:
                if gold < potion_cost + inflation:
                    print("You are %d gold short" % (-1 * (gold - (potion_cost + inflation))))
                    print("You don't have enough gold")
                else:
                    print("Health Potion Cost = %d gold coins" % (potion_cost + inflation))
                    print("Current Gold =",gold)
                    user_input = input("Purchase? (y/n = default)")
                    if user_input == "y" or user_input == "Y":
                        health += 50
                        gold -= potion_cost + inflation
                        if health > 100: #Clamp Health so it will not exceed 100
                            health = 100
        case _:
            print("Extraction avaliable for 1000 gold coins")
            print("Current Gold = %d" % (gold))
            if gold < 1000:
                print("You are %d gold short" % (-1 * (gold - 1000)))
            else:
                user_input = input("Purchase? (y/n = default)")
                print("Extracted Succesfully")
                exit() #Fix Extraction Later
    if floor < 5:
        print("Extraction Avaliable After 5th Floor")
    player_continue()

def enemy_roll():
    roll = random.randint(1,5)
    return roll == 1

#Random Enemy encounter
def enemy(enemy_type: str):
    global health
    global attack
    global defense
    global attack_types
    global receive_dialog
    original_type: str = enemy_type
    enemy_health: int = 25 + (floor * 2)
    if receive_dialog:
        match enemy_type:
            case "Gnome":
                linecache.getline('dialog.txt', random.randint(22,25))
            case "Goblin":
                linecache.getline('dialog.txt', random.randint(22,25))
            case "Skeleton":
                linecache.getline('dialog.txt', random.randint(18,20))
        player_continue()
    print("You Encountered a %s" % (enemy_type))
    print("You Have 3 Attack Types")
    while True:
        for i in range(len(attack_types)):
            print(attack_types[i])
        print("Your Health: %d\nEnemy Health: %d" % (health,enemy_health))
        player_strat = input("What type of attack will you use(p,s,t)")
        if (player_strat == "p" and enemy_type == "Gnome" or player_strat == "P" and enemy_type == "Gnome"
        or player_strat == "s" and enemy_type == "Goblin" or player_strat == "S" and enemy_type == "Goblin"
        or player_strat == "t" and enemy_type == "Skeleton" or player_strat == "T" and enemy_type == "Skeleton"):
            print("It's your chance to attack") #Player Attack
            input("Press Enter to Attack!")
            attack_damage = random.randint(0 + (attack - 5),attack)
            if attack_damage == 0:
                print("You Missed")
            else:
                enemy_health -= attack_damage
                print("You did %d damage" % (attack_damage))
            if attack_damage == attack:
                print("It's a critical hit")
            player_continue()
        else: #Enemy Attack
            enemy_attack = random.randint(0,10 + (floor * 2))
            if enemy_attack == 0:
                print("The enemy missed")
            else:
                health -= (enemy_attack - (defense * 2)) #Enemy Attack damage
                print("You took %d damage!" % (enemy_attack))
            player_continue()
        # 1 in 5 chance the enemy will switch strategies every turn
        if enemy_roll():
            enemy_type = enemy_types[random.randint(0,2)]
        if enemy_health <= 0:
            print("You took down the", original_type)
            player_continue()
            break
        if health <= 0:
            os.system('clear')
            print("You Died")
            player_continue()
            exit()
    reward = random.randint(5 + (floor * 5),45 + (floor * 5)) #Gold drops increase as you progress
    print("Gold Earned = %d" % (reward))
    return reward

#Game Start
start_setting = input("Do you want to play with dialog on? (y,n = default)")
receive_dialog = start_setting == "y" or start_setting == "Y"
shop_event: int = random.randint(2,3)
shopkeeper(linecache.getline('dialog.txt', shop_event))
print("Entering into the dungeon")
#Game Loop
while True:
    floor += 1
    player_continue()
    gold += enemy(enemy_types[random.randint(0,2)])
    inflation += random.randint(0,15)
    if floor > 4:
        shop_event = random.randint(2,5)
    else:
        shop_event = random.randint(2,4)
    shopkeeper(linecache.getline('dialog.txt', shop_event))