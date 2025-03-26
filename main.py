import random
import linecache
import os

class GameState:
    def __init__(self):
        self.floor: int = 0
        self.gold: int = 100
        self.health: int = 100
        self.defense: int = 0
        self.attack: int = 5
        self.potion_cost: int = 10
        self.base_cost: int = 100
        self.inflation: int = 0
        self.receive_dialog: bool = False

game_state = GameState()

""" Speed beats Power, Power beats Technical, Technical beats Speed """
attack_types = ["Power", "Speed", "Technical"]

""" Gnomes Prioritize Technical, Goblins Prioritize Power, Skeletons Prioritize Speed """
enemy_types = ["Gnome", "Goblin", "Skeleton"]

def player_continue():
    input("Press Enter to Continue...")
    os.system('clear')

def handle_purchase(cost, success_message, attribute, increment):
    if game_state.gold < cost:
        print(f"You are {cost - game_state.gold} gold short")
    else:
        user_input = input("Purchase? (y/n = default)")
        if user_input.lower() == 'y':
            setattr(game_state, attribute, getattr(game_state, attribute) + increment)
            game_state.gold -= cost
            print(success_message)

def shopkeeper(dialog):
    print(dialog)
    match shop_event:
        case 2:
            handle_purchase(game_state.base_cost + game_state.inflation, "You upgraded your armour!", 'defense', 3)
        case 3:
            handle_purchase(game_state.base_cost + game_state.inflation, "You purchased an upgraded weapon!", 'attack', 3)
        case 4:
            if game_state.health == 100:
                print("But your health is already full")
            else:
                handle_purchase(game_state.potion_cost + game_state.inflation, "You purchased a health potion!", 'health', 50)
                if game_state.health > 100:
                    game_state.health = 100
        case _:
            handle_purchase(1000, "Extracted successfully", 'gold', -1000)
            exit()
    if game_state.floor < 5:
        print("Extraction available after 5th floor")
    player_continue()

def enemy_roll():
    return random.randint(1, 5) == 1

def enemy_attack(enemy_type, enemy_health):
    print("You encountered a", enemy_type)
    print("You have 3 attack types")
    while True:
        for i, attack in enumerate(attack_types):
            print(attack)
        print(f"Your Health: {game_state.health}\nEnemy Health: {enemy_health}")
        player_strat = input("What type of attack will you use (p, s, t): ").lower()
        if (player_strat == "p" and enemy_type == "Gnome"
                or player_strat == "s" and enemy_type == "Goblin"
                or player_strat == "t" and enemy_type == "Skeleton"):
            attack_damage = random.randint(0 + (game_state.attack - 5), game_state.attack)
            enemy_health -= max(0, attack_damage)
            print(f"You did {attack_damage} damage")
            player_continue()
        else:
            enemy_damage = random.randint(0, 10 + (game_state.floor * 2))
            game_state.health -= max(0, enemy_damage - (game_state.defense * 2))
            print(f"You took {enemy_damage} damage!")
            player_continue()
        if enemy_roll():
            enemy_type = random.choice(enemy_types)
        if enemy_health <= 0:
            print("You took down the", enemy_type)
            player_continue()
            break
        if game_state.health <= 0:
            os.system('clear')
            print("You Died")
            player_continue()
            exit()
    reward = random.randint(5 + (game_state.floor * 5), 45 + (game_state.floor * 5))
    print(f"Gold Earned = {reward}")
    return reward

# Game Initialization
start_setting = input("Do you want to play with dialog on? (y, n = default): ")
game_state.receive_dialog = start_setting.lower() == 'y'
shop_event = random.randint(2, 3)
shopkeeper(linecache.getline('dialog.txt', shop_event))
print("Entering into the dungeon")

# Active Game Loop
while True:
    game_state.floor += 1
    player_continue()
    game_state.gold += enemy_attack(random.choice(enemy_types), 25 + (game_state.floor * 2))
    game_state.inflation += random.randint(0, 15)
    shop_event = random.randint(2, 5 if game_state.floor > 4 else 4)
    shopkeeper(linecache.getline('dialog.txt', shop_event))
