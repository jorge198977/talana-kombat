import json

class Character:
    def __init__(self, name, attack_moves, attack_damage):
        self.name = name
        self.attack_moves = attack_moves
        self.attack_damage = attack_damage
        self.energy = 6

    def execute_special_move(self, combo, damage):
        if combo in self.attack_moves:
            index = self.attack_moves.index(combo)
            self.attack_moves.pop(index)
            self.attack_damage.pop(index)
            return damage
        return 1

    def attack(self, opponent):
        attack_move = self.attack_moves.pop(0)
        damage = self.attack_damage.pop(0)
        damage = self.execute_special_move(attack_move, damage)
        opponent.receive_damage(damage)
        return f"{self.name} conecta un {attack_move}, quita {damage} de energia a {opponent.name}"
    
    def receive_damage(self, damage):
        self.energy -= damage
        self.energy = max(0, self.energy)

    def is_alive(self):
        return self.energy > 0
    

def read_data_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    
    # Convertir los golpes a enteros
    for player_data in data.values():
        player_data["golpes"] = [int(damage) if damage.isdigit() else 1 for damage in player_data["golpes"]]

    return data


if __name__ == "__main__":
    data = read_data_from_json("data.json")

    print(data)