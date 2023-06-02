import random
import datetime
import time


class Arena:
    def __init__(self, player):
        self.player = player
        self.boss_health = 200
        self.battle_started = False

    def start_battle(self):
        self.battle_started = True
        print("Битва началась! Вы сражаетесь с белкой.")

    def fight_boss(self):
        if self.player.alcohol_level != 0:
            if not self.battle_started:
                self.start_battle()

            while True:
                command = input("Введите (бить) для борьбы с белкой: ")

                if command == "бить":
                    damage = random.randint(10, 20)
                    self.boss_health -= damage
                    print(f"Вы нанесли удар боссу и нанесли {damage} урона.")
                    print(f"Здоровье босса: {self.boss_health}")

                    boss_damage = random.randint(10, 20)
                    self.player.health -= boss_damage
                    print(f"Босс нанес вам удар и нанес {boss_damage} урона.")
                    print(f"Ваше здоровье: {self.player.health}")

                    if self.player.health <= 0:
                        self.battle_started = False
                        print("Вы погибли. Игра окончена.")
                        break

                    if self.boss_health <= 0:
                        self.battle_started = False

                        reward = random.randint(100, 500)
                        self.player.add_money(reward)
                        print(f"Вы победили босса и получили {reward} монет.")
                        self.player.heal_after_battle()
                        break
                elif command == "выход":
                    break
                else:
                    print("Неизвестная команда.")
        else:
            print("Вы не можете сражаться с боссом в непьяном состоянии.")


class Drinking:
    def __init__(self):
        self.beers_drunk = 0
        self.wine_drunk = 0
        self.vodka_drunk = 0
        self.bonuses = 0
        self.alcohol_level = 0
        self.health = 100
        self.blood_volume = 5.0
        self.world_explored = False
        self.inventory = []
        self.money = 0

        self.drinks = [
            {"name": "Пиво", "alcohol_level": 0.05,
                "volume": 0.5, "counter": "beers_drunk"},
            {"name": "Вино", "alcohol_level": 0.12,
                "volume": 0.2, "counter": "wine_drunk"},
            {"name": "Водка", "alcohol_level": 0.4,
                "volume": 0.1, "counter": "vodka_drunk"}
        ]

        self.status_message = ""

    def start(self):
        while True:
            command = input("Введите команду: ")

            if command == "пить":
                self.drink()
            elif command == "исследовать":
                self.explore_world()
            elif command == "статус":
                self.print_status()
            elif command == "арена":
                arena = Arena(self)
                arena.fight_boss()
            elif command == "бить":
                print("Вы не можете бить вне арены.")
            elif command == "инвентарь":
                self.print_inventory()
            elif command.startswith("использовать"):
                item = command.split(" ")[1]
                self.use_item(item)
            elif command == "выход":
                break
            else:
                print("Неизвестная команда.")

    def drink(self):
        drink = random.choice(self.drinks)
        max_volume = self.blood_volume * 0.1 - self.alcohol_level
        liters = random.uniform(0.3, max_volume)
        setattr(self, drink["counter"], getattr(self, drink["counter"]) + 1)
        self.bonuses += 1
        self.alcohol_level += drink["alcohol_level"] * liters
        self.alcohol_level = min(self.alcohol_level, self.blood_volume * 0.2)
        print(f"Выпито: {drink['name']}, объем: {liters:.2f} литров.")
        print(
            f"Уровень пьянства: {self.alcohol_level / (self.blood_volume * 0.1) * 100:.1f}%")
        print(
            f"Промилле в крови: {self.alcohol_level / self.blood_volume * 10:.2f}")
        if self.alcohol_level >= self.blood_volume * 0.1:
            self.status_message = "Вы достигли предельного уровня пьянства!"
            print("Вы достигли предельного уровня пьянства!")
        else:
            self.status_message = ""

    def explore_world(self):
        if self.world_explored:
            print("Вы уже исследовали этот мир.")
        else:
            print("Вы отправились исследовать мир...")
            while not self.world_explored:
                current_time = datetime.datetime.now()
                print(f"Текущее время: {current_time}")
                self.update_state()
                self.check_antidote()
                time.sleep(10)
                print("**")

    def update_state(self):
        self.alcohol_level -= 0.01
        if self.alcohol_level < 0:
            self.alcohol_level = 0
        print(
            f"Уровень пьянства: {self.alcohol_level / (self.blood_volume * 0.1) * 100:.1f}%")
        print(
            f"Промилле в крови: {self.alcohol_level / self.blood_volume * 10:.2f}")
        # self.print_inventory()

    def check_antidote(self):
        if random.random() < 0.1:
            self.world_explored = True
            print("Вы нашли антидот! Поздравляем!")
            self.inventory.append("Антидот")

    def print_status(self):
        print(
            f"Выпито пива: {self.beers_drunk} кружек, {self.beers_drunk * 0.5:.2f} литров.")
        print(
            f"Выпито вина: {self.wine_drunk} бокалов, {self.wine_drunk * 0.2:.2f} литров.")
        print(
            f"Выпито водки: {self.vodka_drunk} стопок, {self.vodka_drunk * 0.1:.2f} литров.")
        print(f"Бонусов: {self.bonuses}")
        print(
            f"Уровень пьянства: {self.alcohol_level / (self.blood_volume * 0.1) * 100:.1f}%")
        print(
            f"Промилле в крови: {self.alcohol_level / self.blood_volume * 10:.2f}")
        if self.status_message:
            print(self.status_message)

    def print_inventory(self):
        if len(self.inventory) == 0:
            print("Инвентарь пуст.")
        else:
            print("Инвентарь:")
            for item in self.inventory:
                print(item)

    def use_item(self, item):
        if item in self.inventory:
            if item == "Антидот":
                self.alcohol_level = 0
                self.inventory.remove(item)
                print("Вы использовали антидот. Уровень пьянства обнулен.")
                self.print_inventory()
            else:
                print("Вы не можете использовать этот предмет.")
        else:
            print("У вас нет такого предмета.")

    def add_money(self, amount):
        self.money += amount


    def heal_after_battle(self):
        if self.health < 100:
            amount = random.randint(10, 30)
            self.health = min(self.health + amount, 100)
            print(
                f"Вы восстановили здоровье на {amount}. Текущее здоровье: {self.health}")
        else:
            print("Ваше здоровье уже полное.")


if __name__ == "__main__":
    process = Drinking()
    process.start()
