import random
import sqlite3


class Pioche:
    def __init__(self):
        conn = sqlite3.connect('city.db')
        cursor = conn.cursor()
        self.pioche = []
        
        cursor.execute("SELECT name, how_many FROM users")
        list_pioche = cursor.fetchall()
        
        for name, count in list_pioche:
            self.pioche.extend([name] * count)  # Ajoute la carte 'count' fois
        
        conn.close()
        self.defausse = []

    def pioche_aleatoire(self):
        if not self.pioche:
            self.pioche = self.defausse[:]
            self.defausse = []
        
        item = random.choice(self.pioche)
        self.pioche.remove(item)
        return item


pioche = Pioche()


class Player:
    def __init__(self, name):
        self.deck = []        
        self.city = []        
        self.point = 0        
        self.name = name      

    def piocher(self, cmb):
        for _ in range(cmb):
            if len(self.deck) >= 12:
                print("Limite de cartes atteinte.\n")
                return
            item = pioche.pioche_aleatoire()
            self.deck.append(item)

    def build(self, carte):
        if carte not in self.deck:
            print(f"Tu n'as pas la carte {carte} !")
            return

        conn = sqlite3.connect('city.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT price, reduction_if, can_build_if FROM users WHERE name = ?",
                (carte,)
            )
            result = cursor.fetchone()
            if result is None:
                print(f"La carte {carte} n'existe pas.")
                return

            price, reduction_if, can_build_if = result

            if can_build_if and can_build_if not in self.city:
                print(f"Tu dois construire {can_build_if} avant de construire {carte} !")
                return

            if reduction_if in self.city and price > 0:
                price -= 1

            # Vérifie si on a assez de cartes pour payer
            if price + 1 > len(self.deck):
                manque = (price + 1) - len(self.deck)
                print(f"Tu n'as pas assez de cartes. Il te manque {manque} carte(s).")
                return

            print(f"Tu dois utiliser {price} carte(s) pour construire {carte}.")
            for i, c in enumerate(self.deck):
                if c != carte:
                    print(f"{i}: {c}")

            try:
                choix = input("Entre les numéros : ").split()
                indices = list(map(int, choix))
            except ValueError:
                print("Entrée invalide.")
                return

            if len(indices) != price:
                print(f"{len(indices)} carte(s) sélectionnées, mais {price} requises.")
                return

            # Ajouter les cartes utilisées à la défausse
            cartes_utilisées = [self.deck[i] for i in indices]
            for i in sorted(indices, reverse=True):
                pioche.defausse.append(self.deck[i])
                del self.deck[i]

            # Enlève la carte construite du deck et ajoute à la ville
            self.deck.remove(carte)
            self.city.append(carte)
            print(f"Carte {carte} construite avec succès.")
            print(f"Cartes utilisées : {', '.join(cartes_utilisées)}")

        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            conn.close()

    def calc_score(self):
        self.point = 0
        try:
            conn = sqlite3.connect('city.db')
            cursor = conn.cursor()
            for card in self.city:
                cursor.execute("SELECT points, color FROM users WHERE name = ?", (card,))
                result = cursor.fetchone()
                if not result:
                    continue

                points, color = result
                self.point += points

                # Appliquer les effets spéciaux selon la couleur
                if color == "green":
                    for c in self.city:
                        cursor.execute("SELECT special_green FROM users WHERE name = ?", (c,))
                        bonus = cursor.fetchone()
                        if bonus and bonus[0]:
                            self.point += int(bonus[0])
                elif color == "red":
                    for c in self.city:
                        cursor.execute("SELECT special_red FROM users WHERE name = ?", (c,))
                        bonus = cursor.fetchone()
                        if bonus and bonus[0]:
                            self.point += int(bonus[0])
                elif color == "blue":
                    for c in self.city:
                        cursor.execute("SELECT special_blue FROM users WHERE name = ?", (c,))
                        bonus = cursor.fetchone()
                        if bonus and bonus[0]:
                            self.point += int(bonus[0])

        except Exception as e:
            print(f"Erreur dans le calcul des points : {e}")
        finally:
            conn.close()

    def calc_money(self):
        money = 0
        try:
            conn = sqlite3.connect('city.db')
            cursor = conn.cursor()
            for card in self.city:
                cursor.execute("SELECT money, color FROM users WHERE name = ?", (card,))
                result = cursor.fetchone()
                if not result:
                    continue

                base_money, color = result
                money += base_money

                if color == "green":
                    for c in self.city:
                        cursor.execute("SELECT special_green FROM users WHERE name = ?", (c,))
                        bonus = cursor.fetchone()
                        if bonus and bonus[0]:
                            money += int(bonus[0])
                elif color == "red":
                    for c in self.city:
                        cursor.execute("SELECT special_red FROM users WHERE name = ?", (c,))
                        bonus = cursor.fetchone()
                        if bonus and bonus[0]:
                            money += int(bonus[0])
                elif color == "blue":
                    for c in self.city:
                        cursor.execute("SELECT special_blue FROM users WHERE name = ?", (c,))
                        bonus = cursor.fetchone()
                        if bonus and bonus[0]:
                            money += int(bonus[0])
        except Exception as e:
            print(f"Erreur dans le calcul de l'argent : {e}")
        finally:
            conn.close()
        return money





