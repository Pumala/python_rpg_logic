"""
Added a store. The hero can now buy a tonic or a sword. A tonic will add 2 to the hero's health wherease a sword will add 2 power.
"""
import random
import time

class Character(object):
    def __init__(self):
        self.name = '<undefined>'
        self.health = 10
        self.power = 5
        self.coins = 20

    def alive(self):
        return self.health > 0

    def attack(self, enemy):
        if not self.alive():
            return
        print "%s attacks %s" % (self.name, enemy.name)
        enemy.receive_damage(self.power)
        time.sleep(1.5)

    def receive_damage(self, points):
        self.health -= points
        print "%s received %d damage." % (self.name, points)
        if self.health <= 0:
            print "%s is dead." % self.name

    def print_status(self):
        print "%s has %d health and %d power." % (self.name, self.health, self.power)

class Hero(Character):
    def __init__(self):
        self.name = 'hero'
        self.health = 10
        self.power = 5
        self.coins = 20
        self.armour = 0
        self.armour_usage = 0
        self.evade = 0
        self.tonic_pts = 0
        self.swap_power_count = 0
        self.resources = []
        # self.resources = []

    def swap_power(self, enemy):
        # if self.swap_power:
        #     print "Would you like to swap powers? (Y or N)"
        #     answer = raw_input("> ").upper()
            # if answer == "Y":
        temp_power = enemy.power
        enemy.power = hero.power
        hero.power = temp_power

    def use_tonic(self):
        if self.tonic_pts:
            print "Do you want to use your tonic now?"
            print "It will increase your health by %d." % self.tonic_pts
            answer = raw_input("(Y or N): ").upper()
            if answer == "Y":
                health_before = self.health
                self.health += self.tonic_pts
                self.tonic_pts = 0
                print "The %s's health increased from %d to %d." % (self.name, health_before, self.health)
            else:
                pass

    def tonic(self):
        health_before = self.health
        self.health += 2
        self.tonic_pts -= 2
        print "The %s's health increased from %d to %d." % (self.name, health_before, self.health)

    def use_resources(self):
        if len(self.resources) >= 1:
            answer = raw_input("Do you want to use any of your resources now (Y or N)? ").upper()
            if answer == "Y":
                counter = 1
                for item in self.resources:
                    print "%d. %d %s" % (counter, item[1], item[0])
                answer = int(raw_input("> "))
                item = self.resources[answer - 1][0]
                if self.resources[answer - 1][1] >= 1:
                    self.resources[answer - 1][1] -= 1
                    if self.resources[answer - 1][1] == 0:
                        del self.resources[answer - 1]
                        print self.resources
                print item
                if item == "tonic":
                    # self.use_tonic()
                    self.tonic()
                elif item == "swap power":
                    self.swap_power()
                # del self.resources[answer - 1]
                # counter = 1
                # for item, count in self.resources.items():
                #     print "%d. %d %s" % (counter, count, item)
                #     counter += 1

                # answer = int(raw_input("> "))
                # item = self.resources[answer - 1]
                # if item == "tonic":
                #     # self.use_tonic()
                #     self.tonic()
                # elif item == "swap power":
                #     self.swap_power()
                # del self.resources[answer - 1]

                # for i in range(0, len(self.resources)):
                #     print "%d. %s" % (i + 1, self.resources[i])
                # answer = int(raw_input("> "))
                # item = self.resources[answer - 1]
                # if item == "tonic":
                #     # self.use_tonic()
                #     self.tonic()
                # elif item == "swap power":
                #     self.swap_power()
                # del self.resources[answer - 1]
            else:
                print "Maybe next time"

    def attack(self, enemy):
        super(Hero, self).attack(enemy)
        if not enemy.alive():
            self.coins += enemy.bounty
            print "The %s collected %d bounty." % (self.name, enemy.bounty)

    def receive_damage(self, points):
        if self.evade > 0:
            evade_prob = float((5 + (5 * (self.evade / 2.0))) / 100)
            if random.random() < evade_prob:
                print "The %s evaded the attack." % self.name
                return
        # if len(self.resources) >= 1:
        #     print "Do you want to use any of your resources now?"
        self.use_resources()
        # self.use_tonic()
        if self.armour:
            self.armour_usage -= 1
            armour_pts = self.armour
            print "The armour protects the %s." % self.name
            print "The attack power is reduced by %d points." % self.armour
        if random.random() > 0.2:
            super(Hero, self).receive_damage(points - self.armour)
        else:
            super(Hero, self).receive_damage((points * 2) - self.armour )
            print "The %s was delivered 2 blows." % (self.name)
        if self.armour_usage == 0:
            self.armour = 0

    def restore(self):
        self.health = 10
        print "Hero's heath is restored to %d!" % self.health
        time.sleep(1)

    def buy(self, item):
        self.coins -= item.cost
        item.apply(hero)

class Medic(Character):
    def __init__(self):
        self.name = "medic"
        self.health = 9
        self.power = 4
        self.bounty = 5

    def receive_damage(self, points):
        super(Medic, self).receive_damage(points)
        if self.alive():
            if random.random() > 0.2:
                self.health += 2
                print "The %s regained 2 health points." % (self.name)
        else:
            pass

class Shadow(Character):
    def __init__(self):
        self.name = "shadow"
        self.health = 1
        self.power = 2
        self.bounty = 7

    def receive_damage(self, points):
        if random.random() > 0.10:
            print "The %s evaded the attack." % (self.name)
            return
        else:
            super(Shadow, self).receive_damage(points)

class Goblin(Character):
    def __init__(self):
        self.name = 'goblin'
        self.health = 6
        self.power = 2
        self.bounty = 5

class Wizard(Character):
    def __init__(self):
        self.name = 'wizard'
        self.health = 8
        self.power = 1
        self.bounty = 6

    def attack(self, enemy):
        swap_power = random.random() > 0.5
        if swap_power:
            print "%s swaps power with %s during attack" % (self.name, enemy.name)
            self.power, enemy.power = enemy.power, self.power
        super(Wizard, self).attack(enemy)
        if swap_power:
            self.power, enemy.power = enemy.power, self.power

class Battle(object):
    def do_battle(self, hero, enemy):
        print "====================="
        print "Hero faces the %s" % enemy.name
        print "====================="
        while hero.alive() and enemy.alive():
            hero.print_status()
            enemy.print_status()
            time.sleep(1.5)
            print "-----------------------"
            print "What do you want to do?"
            print "1. fight %s" % enemy.name
            print "2. do nothing"
            print "3. flee"
            print "> ",
            input = int(raw_input())
            if input == 1:
                hero.attack(enemy)
            elif input == 2:
                pass
            elif input == 3:
                print "Goodbye."
                exit(0)
            else:
                print "Invalid input %r" % input
                continue
            enemy.attack(hero)
        if hero.alive():
            print "You defeated the %s" % enemy.name
            return True
        else:
            print "YOU LOSE!"
            return False

class Tonic(object):
    cost = 5
    name = 'tonic'
    def apply(self, character):
        while True:
            print "Do you want to use it now or save for later?"
            print "1. Use tonic now"
            print "2. Save tonic for later"
            answer = int(raw_input("> "))
            if answer == 1:
                character.health += 2
                print "%s's health increased to %d." % (character.name, character.health)
                break
            elif answer == 2:
                character.tonic_pts += 2
                # character.resources.update("tonic": (character.tonic_pts / 2))
                # character.resources["tonic"] = character.tonic_pts / 2
                # character.resources.append({"tonic": character.tonic_pts / 2})
                counter = 0
                has_tonic = False
                for item in character.resources:
                    if item[0] == "tonic":
                        item[1] += 1
                        has_tonic = True
                    else:
                        pass
                if has_tonic == False:
                    character.resources.append(["tonic", character.tonic_pts / 2])
                    print "%s's tonic has been stored in the weaponry." % (character.name)
                break
            else:
                print "Invalid answer."

class SuperTonic(object):
    cost = 8
    name = 'supertonic'
    def apply(self, character):
        character.health += 10
        print "%s's health increased to %d." % (character.name, character.health)

class Sword(object):
    cost = 10
    name = 'sword'
    def apply(self, hero):
        hero.power += 2
        print "%s's power increased to %d." % (hero.name, hero.power)

class Armour(object):
    cost = 10
    name = 'armour'
    def apply(self, hero):
        hero.armour = 2
        hero.armour_usage = 3
        print "%s's armour increased to %d." % (hero.name, hero.armour)

class Evade(object):
    cost = 8
    name = 'evade'
    def apply(self, hero):
        hero.evade += 2
        print "%s's evade increased to %d." % (hero.name, hero.evade)

class SwapPower(object):
    cost = 5
    name = 'swap power'
    def apply(self, hero):
        hero.swap_power_count += 1
        print "%s's swap power count has increased to %d." % (hero.name, hero.swap_power_count)

class Store(object):
    # If you define a variable in the scope of a class:
    # This is a class variable and you can access it like
    # Store.items => [Tonic, Sword]
    items = [Tonic, SuperTonic, Sword, Armour, Evade, SwapPower]
    def do_shopping(self, hero):
        while True:
            print "====================="
            print "Welcome to the store!"
            print "====================="
            print "You have %d coins." % hero.coins
            print "What do you want to do?"
            for i in xrange(len(Store.items)):
                item = Store.items[i]
                print "%d. buy %s (%d)" % (i + 1, item.name, item.cost)
            print "10. leave"
            input = int(raw_input("> "))
            if input == 10:
                break
            else:
                ItemToBuy = Store.items[input - 1]
                item = ItemToBuy()
                hero.buy(item)

hero = Hero()
enemies = [Goblin(), Shadow(), Medic(), Wizard()]
battle_engine = Battle()
shopping_engine = Store()

for enemy in enemies:
    hero_won = battle_engine.do_battle(hero, enemy)
    if not hero_won:
        print "YOU LOSE!"
        exit(0)
    shopping_engine.do_shopping(hero)

print "YOU WIN!"
