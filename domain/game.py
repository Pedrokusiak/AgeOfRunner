from typing import List
from domain.entity.ground_segment import GroundSegment
from domain.menu import Menu
from domain.entity.player import Player
from domain.entity.game_object import GameObject
from domain.game_state import GameState
from domain.physics.vector2D import Vector2D
from ports.clock_port import ClockPort
from ports.event_port import EventPort
from ports.renderer_port import RendererPort
from ports.physics_port import PhysicsPort

class Game:
    def __init__(self, 
                 renderer: RendererPort, 
                 event_handler: EventPort, 
                 clock: ClockPort,
                 physics: PhysicsPort):
        self.renderer = renderer
        self.event_handler = event_handler
        self.clock = clock
        self.physics = physics  # Nova porta de física
        self.state = GameState.MENU
        self.game_objects: List[GameObject] = []
        self.menu = self.create_menu()
        
    def create_menu(self) -> Menu:
        menu = Menu(self.renderer)
        menu.add_item("Start Game", self.start_game)
        menu.add_item("Options", self.show_options)
        menu.add_item("Exit", self.exit_game)
        return menu
    
    def init_game_objects(self):
        # Passa a porta de física para os objetos
        player = Player(
            physics=self.physics,
            position=Vector2D(20, 250)
        )
        
        ground = GroundSegment(
            physics=self.physics,
            position=Vector2D(0, 300),
            width=800
        )

        
        self.game_objects.append(player)
        self.game_objects.append(ground)
        
    def start_game(self):
        self.state = GameState.PLAYING
        self.init_game_objects()
        
    def show_options(self):
        pass
        
    def exit_game(self):
        self.event_handler.quit()
        
    def handle_input(self):
        if self.state == GameState.MENU:
            if self.event_handler.is_key_pressed("jump"):
                self.menu.select_previous()
            elif self.event_handler.is_key_pressed("down"):
                self.menu.select_next()
            elif self.event_handler.is_key_pressed("return"):
                self.menu.activate_selected()
        elif self.state == GameState.PLAYING:
            for obj in self.game_objects:
                if isinstance(obj, Player):
                    obj.handle_input(self.event_handler)
                    break
                
    def update(self):
        delta_time = self.clock.get_delta_time()
        
        if self.state == GameState.PLAYING:
            self.physics.update(delta_time)
            
            for obj in self.game_objects:
                obj.update(delta_time)
            
    def render(self):
        self.renderer.clear()
        
        if self.state == GameState.MENU:
            self.menu.render()
        elif self.state == GameState.PLAYING:
            for obj in self.game_objects:
                obj.render(self.renderer)
                
        self.renderer.present()
            
    def run(self):
        running = True
        while running:
            running = self.event_handler.poll_events()
            self.handle_input()
            self.update()
            self.render()
            self.clock.update()
            
        if hasattr(self.physics, 'cleanup'):
            self.physics.cleanup()
        self.event_handler.quit()


   

if __name__ == "__main__":
    game = create_game()
    game.run()