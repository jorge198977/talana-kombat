import json

class Player:
    def __init__(self, name, attack_moves, attack_damage):
        self.name = name
        self.attack_moves = attack_moves
        self.attack_damage = attack_damage
        self.energy = 6
    
    def special_moves(self):
        special_moves = ""
        if self.name == "Tonyn Stallone":
            special_moves= {
                "DSDP": 3,   # Taladoken - Movimientos: DSD, Golpe: P
                "SDK": 2,   # Remuyuken - Movimientos: SD, Golpe: K
                "P": 1,   # Puño: Golpe: P
                "K": 1   # Puño: Golpe: K
            }
        if self.name == "Arnaldor Shuatseneguer":
            special_moves= {
                "SAK": 3,   # Remuyuken - Movimientos: SA, Golpe: K
                "ASAP": 2,   # Taladoken - Movimientos: ASA, Golpe: P
                "P": 1,   # Puño: Golpe: P
                "K": 1   # Puño: Golpe: K
            }    
        return special_moves
    

    def execute_special_move(self, combo, damage):
        special_moves = self.special_moves()
        combo_key = combo + str(damage)
        if combo_key in special_moves:
            return special_moves[combo_key]

        if combo in self.attack_moves:
            index = self.attack_moves.index(combo)
            self.attack_moves.pop(index)
            damage_str = self.attack_damage.pop(index)  # Obtener el golpe como cadena
            if damage_str.isdigit():  # Verificar si es un número válido
                return int(damage_str)  # Convertir a entero

        return 1
    
    def attack(self, opponent):
        if not self.attack_moves or not self.attack_damage:
            return f"{self.name} no puede atacar, se ha quedado sin movimientos o golpes."

        attack_move = self.attack_moves[0]        
        if len(attack_move)>3:
            attack_move = attack_move[-3:]
        attack = self.attack_damage[0]
        damage = self.attack_damage[0]
        if not attack:
            attack = "M"
            damage = 0
        else:
            damage = self.execute_special_move(attack_move, damage) 
        opponent.receive_damage(damage)
        return attack_move, attack, damage, self.name 
    
    def receive_damage(self, damage):
        self.energy -= damage
        self.energy = max(0, self.energy)

    def is_alive(self):
        return self.energy > 0
    
class Kombat:
    def __init__(self, player1_data, player2_data):
        self.player1 = Player("Tonyn Stallone", player1_data["movimientos"], player1_data["golpes"])
        self.player2 = Player("Arnaldor Shuatseneguer", player2_data["movimientos"], player2_data["golpes"])


    def _choose_starting_player(self):
        combo1 = self.player1.attack_moves[0] + str(self.player1.attack_damage[0])
        combo2 = self.player2.attack_moves[0] + str(self.player2.attack_damage[0])

        combos = [combo1, combo2]
        players = [self.player1, self.player2]

        for combo, player in zip(combos, players):
            if len(combo) < len(combos[1]):
                return player, players[1]
            elif len(combo) > len(combos[1]):
                return players[1], player

        return players[0], players[1]
    
    def fight(self):
        fight_log = []
        player1_turn, player2_turn = self._choose_starting_player()

        while player1_turn.is_alive() and player2_turn.is_alive() and player1_turn.attack_moves and player2_turn.attack_moves:
            if player1_turn.is_alive():
                log = player1_turn.attack(player2_turn)
                fight_log.append(log)

            if player2_turn.is_alive():
                log = player2_turn.attack(player1_turn)
                fight_log.append(log)

        return fight_log, self.get_winner()

    def get_winner(self):
        if self.player1.is_alive():
            return self.player1.name
        else:
            return self.player2.name

# Leer json con data
def read_data_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

# Relatar la pelea
def narrate_fight(fight_log):
    narration = []
    for move, attack, damage, name in fight_log:
        if(damage > 1):
            narration.append(f"➢ {name} conecta un {convert_special_move_to_narrate(name, damage)}")    
        else:
            move_narration, atack_narration = convert_move_to_narrate(move, attack)
            narration.append(f"➢ {name} {move_narration} y {atack_narration} ")

    return "\n".join(narration)

def convert_special_move_to_narrate(name, damage):
    # Es ataque especial
    if name == "Tonyn Stallone":
        special_moves= {
            3: "Taladoken",  
            2: "Remuyuken"   
        }
    if name == "Arnaldor Shuatseneguer":
        special_moves= {
            3: "Remuyuken",   
            2: "Taladoken"
        }    
    return special_moves[damage]

def convert_move_to_narrate(move, attack):
    move_narrate = {
        "W": "Salta",
        "S": "Retrocede",
        "A": "Baja",
        "D": "Avanza"
    }
    attack_narrate = {
        "P": "da un puño",
        "K": "da una patada",
    }

    move_description = move_narrate.get(move, f"realiza el movimiento desconocido {move}")
    attack_description = attack_narrate.get(attack, "")

    return move_description, attack_description

if __name__ == "__main__":
    data = read_data_from_json("data.json")
    kombat = Kombat(data["player1"], data["player2"])
    fight_log, winner = kombat.fight()

    narration = narrate_fight(fight_log)
    print(narration)

    print(f"{winner} gana la pelea y aun le queda {kombat.player2.energy} de energía.")