

class Cell:
    def __init__(self) -> None:
        self.position: tuple = ()
        self.color = None
        self.is_obstacle: bool = False
        self.is_starting_point: bool = False
        self.is_target: bool = False
        self.g_cost: int = 0
        
    def set_target(self):
        self.is_target = True
        self.color = (255, 0, 0)  # Red for target
        
    def set_obstacle(self):
        self.is_obstacle = True
        self.color = (0, 0, 0)  # Black for obstacle
        
        
if __name__ == "__main__":
    c = Cell()
    print(c.position, c.color, c.is_obstacle, c.is_starting_point, c.is_target, c.g_cost)