"""
CSSE1001 Assignment 2
Semester 2, 2020
"""
from a2_support import *

# Fill these in with your details
__author__ = "{{Gunit Singh}} ({{s4642570}})"
__email__ = "gunit.singh@uqconnect.edu.au"
__date__ = "27/09/2020"

# Write your code here

class GameLogic:
    """ Initialises the Game Logic class. """
    def __init__(self, dungeon_name="game1.txt"):
        """Constructor of the GameLogic class.

        Parameters:
            dungeon_name (str): The name of the level.
        """
        self._dungeon = load_game(dungeon_name)
        self._dungeon_size = len(self._dungeon)

        #you need to implement the Player class first.
        self._player = Player(GAME_LEVELS[dungeon_name])

        #you need to implement the init_game_information() method for this.
        self._game_information = self.init_game_information()

        self._win = False

    def get_positions(self, entity):
        """ Returns a list of tuples containing all positions of a given Entity
             type.

        Parameters:
            entity (str): the id of an entity.

        Returns:
            )list<tuple<int, int>>): Returns a list of tuples representing the 
            positions of a given entity id.
        """
        positions = []
        for row, line in enumerate(self._dungeon):
            for col, char in enumerate(line):
                if char == entity:
                    positions.append((row,col))

        return positions

    # Write your code here
    def get_dungeon_size(self):
        """ Returns the width of the dungeon as an integer.
            Return:
               self._dungeon_size(int): The width of the dungeon. """
        return self._dungeon_size
    
    def init_game_information(self):
        """ Returns a dictionary with postion and corresponding Entity as the key
            and values respectively. Also set's the Player's position.
            Return:
                self.game_information(dict): A dictionary containing the position and it's
                entity as the key's and values. """
        self.game_information = {}
        
        wall_positions = self.get_positions(WALL)
        key_position = self.get_positions(KEY)
        door_position = self.get_positions(DOOR)
        player_position = self.get_positions(PLAYER)
        move_increase_position = self.get_positions(MOVE_INCREASE)

        self._player.set_position(player_position[0])
        self.get_player().get_position()


        self.game_information.update({key_position[0]: (Key())})
        self.game_information.update({door_position[0]: (Door())})
        for locations in wall_positions:
            self.game_information.update({locations: (Wall())})

        if move_increase_position != []:
            self.game_information.update({move_increase_position[0]: (MoveIncrease())})
        
        return self.game_information
                
    def get_game_information(self):
        """ Returns adictionary containing the position and the corresponding Entity,
            as the keys and values, for thecurrent dungeon.
            Return:
                self._game_information(dict): A dictionary containing the position and it's
                entity as the key's and values. """
        return self._game_information

    def get_player(self):
        """ This method returns the Player object within the game.
            Return:
                self._player(Entity): The representation of the player object. """
        return self._player

    def get_entity(self, position):
        """ Returns an Entity at a given position in the dungeon. If the position is off map,
            then returns None.
            Paramters:
                position(tuple<int, int>): The given position to be tested if entity exists from it.
            Returns:
                entity_in_position(Entity): Entity in the given position.
                None if no Entity in given position. """
        for location in self.game_information:
            if position == location:
                entity_in_position = self.game_information.get(position, None)
                return entity_in_position

    def get_entity_in_direction(self, direction):
        """ Returns an Entity at a given position in the dungeon. If the position is off map,
            then returns None.
            Paramters:
                direction(str): Diirection of the player (see DIRECTIONS)
            Returns:
                entity_in_direction(Entity): The entity in the given direction of player."""
        player_position = self.get_player().get_position()
        coordinate = DIRECTIONS.get(direction)
        position1 = player_position[0]+coordinate[0]
        position2 = player_position[1]+coordinate[1]
        entity_in_direction = self.get_entity((position1, position2))
        return entity_in_direction
        
    def collision_check(self, direction):
        """ Returns ​False​ if a player cantravel in the given direction, they won’t collide. ​
            Returns True if they will collide.
            Parameters:
                direction(str): Diirection of the player (see DIRECTIONS)
            Returns:
                True if Entity can collide.
                False if it can not,"""
        if str(self.get_entity_in_direction(direction)) == str(Wall()):
            return True
        else:
            return False
        

    def new_position(self, direction):
        """ Returns a tuple of integers that represents the new position given the direction.
            Parameters:
                direction(str): Diirection of the player (see DIRECTIONS)
            Returns:
                new_position(tuple<int, int>): Tuple of integers representing the new position
                                                given the direction. """
        player_position = self.get_player().get_position()
        coordinate = DIRECTIONS.get(direction)
        position1 = player_position[0]+coordinate[0]
        position2 = player_position[1]+coordinate[1]
        new_position = (position1, position2)
        
        return new_position


    def move_player(self, direction):
        """ Updates the Player’s position to place them one position in the given direction.
            Parameters:
                direction(str): Diirection of the player (see DIRECTIONS) """
        position = self.new_position(direction)
        self._player.set_position(position)

    def check_game_over(self):
        """ Return True if the game has been ​lost and False otherwise.
            Return:
                True (bool) if game lost.
                False (bool) if not game lost. """
        player_position = self.get_player().get_position()
        player_inventory = self.get_player().get_inventory()
        moves_remain = self.get_player().moves_remaining()
        if player_position == self.get_positions(DOOR) and player_inventory == [str(Key())]:
            return True
        elif moves_remain == 0:
            return True
        else:
            return False

    def set_win(self, win):
        """ Set the game’s win state to be True or False.
            Parameters:
                win(bool): Game's state, either True or False. """
        self._win = win

    def won(self):
        """ Return game’s win state.
            Returns:
                self._win(bool): The win state."""
        return self._win
        

    
class GameApp(object):
    """ Comunicator between GameLogic and the Display classes. """
    def __init__(self):
        """ Initialises GameApp object. """
        self._game = GameLogic()

        
    def play(self):
        """ Handles the player interaction. """
        while self._game.get_player().moves_remaining() > 0: #checks if moves remaining is not 0.

            self.draw() #draws the game dingeon
            action = input("Please input an action: ") #promts user input
            while action not in "WSAD": #checks if HElP, QUIT or invalid input are called
                if action == HELP:
                    print(HELP_MESSAGE)
                    self.draw()
                    action = input("Please input an action: ")

                elif action == QUIT:
                    to_quit = input("Are you sure you want to quit? (y/n): ")
                    if to_quit == 'y':
                        return
                    else:
                        self.draw()
                        action = input("Please input an action: ")

                elif action[0:2] == "I " and action[2] in "WASD" and len(action)==3: #accounts for the investigate command
                        entity = self._game.get_entity_in_direction(action[2])
                        print(str(entity) + f" is on the {action[2]} side.")
                        self._game.get_player().change_move_count(-1) #decreases move count by one
                        if self._game.get_player().moves_remaining() == 0:
                             print(LOSE_TEST)
                             return
                        self.draw()
                        action = input("Please input an action: ")

                else:
                    print(INVALID)
                    self.draw()
                    action = input("Please input an action: ")


            if self._game.collision_check(action) == True:   #checks if player move does not collide
                self._game.get_player().change_move_count(-1)
                print(INVALID)
                if self._game.get_player().moves_remaining() == 0:
                    print(LOSE_TEST)
                    return
                
            else:
                try:
                    self._game.get_entity_in_direction(action).on_hit(self._game)  #handles interactions between Player and Entity's if collided
                except AttributeError:
                    pass
                
                self._game.get_player().set_position(self._game.new_position(action)) #set's new position
                self._game.get_player().change_move_count(-1)
                
            if self._game.won() == True:  #checks if game has been won
                print(WIN_TEXT)
                return
        
        print(LOSE_TEST) #if the the game has not been won after the while loop


    def draw(self):
        """ Displays the dungeon with all Entities in their positions. ​Also displays the player’s remaining move count. """
        display = Display(self._game.get_game_information(), self._game.get_dungeon_size())
        display.display_game(self._game.get_player().get_position())
        display.display_moves(self._game.get_player().moves_remaining())


class Entity(object):
    """ A generic Entity within the game. """
    def __init__(self):
        """ Initialises an Entity instance. """
        self._id = "Entity"
        self._collidable = True
        self._type = 'Entity'

    def get_id(self):
        """ Returns a string representing the Entity's ID.
            Returns:
                self._id(str): String representing Entity's ID. """
        return self._id

    def set_collide(self, other):
        """ Sets the collisiton state for the Entity to be True.
            Parameters:
                other(bool): The collision state of Entity. """
        self._collidable = other

    def can_collide(self):
        """ Returns True if the Entity can be collided with (anotherEntity
            can share the position that this one is in) and False otherwise.
            Returns:
                self._collidable(bool): The collision state of Entity."""
        return self._collidable
        
    def __str__(self):
        """ Returns the string representation of the Entity. """
        return self._type+"('" + self._id + "')"

    def __repr__(self):
        """ Returns the string representation of the Entity. """
        return self.__str__()

class Wall(Entity):
    """ A special type of an Entity. """
    def __init__(self):
        """ Initialises the Wall's instance. Methods inherited from Entity class. """
        self._collidable = False
        self._id = WALL
        self._type = 'Wall'

class Item(Entity):
    """ Special type of Enitity within the game. It is an abstract class. """
    def __init__(self):
        """ Initialise's an instance of an Item Entity. """
        self._collidable = True
        self._id = 'Entity'
        self._type = 'Item'

    def on_hit(self, game):
        """ Raises the NotImplementedError.
            Parameters:
                game(class): Class containing game information and how it should play out. """
        raise NotImplementedError

class Key(Item):
    """ A special type of Item. """
    def __init__(self):
        """ Initialises an instance of the Key Entity. Methods inherited from Item. """
        self._collidable = True
        self._id = KEY
        self._type = 'Key'

    def on_hit(self, game):
        """ Adds the Key to PLayer's Inventory and rmeoves it from the dungeon.
            Parameters:
                game(class): Class containing game information and how it should play out. """
        game.get_player().add_item(self)
        key_position = game.get_positions(KEY)[0]
        game._game_information.pop(key_position)
        
class MoveIncrease(Item):
    """ MoveIncrease is a special type of Item. """
    def __init__(self, moves=5):
        """ Intialises an instance of the MoveIncrease Entity. Methods inherited from Item.
            Parameters:
                moves(int): The number of moves a player is allowed. Default at 5. """
        self._collidable = True
        self._id = MOVE_INCREASE
        self._type = 'MoveIncrease'
        self._moves = moves
        
    def on_hit(self, game):
        """ Increases the number of moves for the player and removes the item from the game.
            Parameters:
                game(class): Class containing game information and how it should play out. """
        game.get_player().change_move_count(self._moves)
        move_increase_position = game.get_positions(MOVE_INCREASE)[0]
        game._game_information.pop(move_increase_position)
        

class Door(Entity):
    """ A Door is a special type of an Entity. """
    def __init__(self):
        """ Intialises the instance of a Door Entity. Methods inherited from Entity class. """
        self._collidable = True
        self._id = DOOR
        self._type = 'Door'
        
    def on_hit(self, game):
        """ Set's 'game over' state to be true id player's inventory contains the key. Else, print's
            "You don't have the key!".
            Parameters:
                game(class): Class containing game information and how it should play out."""
        if game.get_player().get_inventory() != []:
            game.set_win(True)
        else:
            print("You don't have the key!")


class Player(Entity):
    """ A special type of Entity. """
    def __init__(self, move_count):
        """ Initialise a Player Instance.
            Paramters:
                move_count(int): Represents the moves a Player can have for given dungeon."""
        super().__init__()
        self._collidable = True
        self._id = PLAYER
        self._type = 'Player'
        self._move_count = move_count
        self._inventory = []
        self._position = None
        
    def set_position(self, position):
        """ Sets the position of  the Player.
            Parameters:
                position(tuple<int, int>): The position required to set for player. """
        self._position = position

    def get_position(self):
        """ Returns a tuple of ints representing the position of the Player. If the Player’s position
            hasn’t been set yet then, returns None.
            Returns:
                self._position(tuple<int, int>): The position of the player.
                None if no position has been set yet. """
        return self._position

    def change_move_count(self, number):
        """ Adds number to the Player's move count.
            Parameters:
                number(int): Number to be added to player's move count. """
        self._move_count += number

    def moves_remaining(self):
        """ Returns an int representing how many moves thePlayer has left before they reach the maximum
            move count.
            Returns:
                self._move_count(int): The Player's move remaining before reaching maximam move count."""
        return  self._move_count

    def add_item(self, item):
        """ Adds the item to the Player’s Inventory.
            Parameters:
                item(Entity): An entity to be added to Player's Inventory."""
        self._inventory.append(item)

    def get_inventory(self):
        """ Returns a list that represents the Player’s inventory. If the Player has nothing in their
            inventory, returns an empty list.
            Returns:
                self._inventory(List): A list that represents the Player's inventory (could be empty)."""
        return self._inventory 

def main():
    """ Calls functions defined in the classes above. """
    GameApp().play()


if __name__ == "__main__":
    main()
