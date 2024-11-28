from domain.physics.vector2D import Vector2D

class Camera:
    def __init__(self, viewport_width: int, viewport_height: int, world_bounds: tuple):
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.world_x = 0
        self.world_y = 0
        self.world_bounds = world_bounds  # (min_x, min_y, max_x, max_y)
        
    def follow(self, target_position: Vector2D):
        self.world_x = target_position.x - (self.viewport_width / 2)
        self.world_y = target_position.y - (self.viewport_height / 2)
        
        self.world_x = max(self.world_bounds[0], 
                          min(self.world_x, 
                              self.world_bounds[2] - self.viewport_width))
        self.world_y = max(self.world_bounds[1], 
                          min(self.world_y, 
                              self.world_bounds[3] - self.viewport_height))
    
    def world_to_screen(self, world_pos: Vector2D) -> Vector2D:
        screen_x = world_pos.x - self.world_x
        screen_y = world_pos.y - self.world_y
        return Vector2D(screen_x, screen_y)
    
    def is_in_view(self, position: Vector2D, width: float, height: float) -> bool:
        return (position.x + width >= self.world_x and
                position.x <= self.world_x + self.viewport_width and
                position.y + height >= self.world_y and
                position.y <= self.world_y + self.viewport_height)