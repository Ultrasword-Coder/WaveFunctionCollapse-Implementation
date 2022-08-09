import random
from queue import deque, PriorityQueue


class Tile2D:
    def __init__(self, id, left, top, right, bottom):
        # valid neighbors
        self.id = id
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
    
    def check_valid(self, levelgenerator, x, y):
        """Checks if the nearby tiles allow for this tile"""
        # check if tile to the left can accept its right
        if x>0:
            ntile = levelgenerator.grid[y][x-1]
            if not ntile.can_accept_tile(levelgenerator, self, 2):
                return 0
        # check right
        if x+1<levelgenerator.area[0]:
            ntile = levelgenerator.grid[y][x+1]
            if not ntile.can_accept_tile(levelgenerator, self, 0):
                return 0
        # check top
        if y>0:
            ntile = levelgenerator.grid[y-1][x]
            if not ntile.can_accept_tile(levelgenerator, self, 3):
                return 0
        # check bottom
        if y+1<levelgenerator.area[1]:
            ntile = levelgenerator.grid[y+1][x]
            if not ntile.can_accept_tile(levelgenerator, self, 1):
                return 0
        return 1


class WCFTile:
    DIRECTION = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def __init__(self, levelgenerator, x, y):
        self.entropy = len(levelgenerator.tiles)
        self.possible_states = [i for i in range(1, self.entropy+1)]
        self.state = 0
        self.pos = (x, y)
        # add self to the queue
        levelgenerator.queue.append((self.entropy, self.pos[0], self.pos[1]))
        self.collapsed = False

    def can_accept_tile(self, levelgenerator, tile, direction):
        """
        Checks if a tile can accept a certain tile in a certain direction
        direction: [left=0, top=1, right=2, bottom=3]
        """
        if direction == 0:
            for p in self.possible_states:
                if not p: continue
                if tile.id in levelgenerator.tiles[p-1].left:
                    return True
            return False
        elif direction == 1:
            for p in self.possible_states:
                if not p:
                    continue
                if tile.id in levelgenerator.tiles[p-1].top:
                    return True
            return False
        elif direction == 2:
            for p in self.possible_states:
                if not p:
                    continue
                if tile.id in levelgenerator.tiles[p-1].right:
                    return True
            return False
        else:
            for p in self.possible_states:
                if not p:
                    continue
                if tile.id in levelgenerator.tiles[p-1].bottom:
                    return True
            return False

    def collapse(self):
        p = []
        for i in self.possible_states:
            if not i: continue
            p.append(i)
        self.entropy = 0
        self.state = 0
        if p:
            self.state = random.choice(p)
        for x in range(len(self.possible_states)):
            self.possible_states[x] = 0
        print(f"collapsed: {self.pos} = {self.state} from {p}")
        self.possible_states[self.state-1] = self.state
        self.collapsed = True
    
    def propagate_changes(self, levelgenerator):
        q = PriorityQueue()
        q.put((self.entropy, 0, self.pos[0], self.pos[1]))
        while not q.empty():
            o = q.get()
            pos = (o[2], o[3])
            tile = levelgenerator.grid[pos[1]][pos[0]]
            if levelgenerator.vis[pos[1]][pos[0]]: 
                print(f"{pos} has been vis")
                continue
            levelgenerator.vis[pos[1]][pos[0]] = True
            # ------------ optimization ---------------- #
            # ------------------------------------------ #
            # actually do some brain stuff
            print(f"Checking: {pos}")
            levelgenerator.check_valid_state_tiles(tile, pos)
            print(tile.possible_states)
            # check nearby tiles
            for dx, dy in WCFTile.DIRECTION:
                nx, ny = pos[0]+dx, pos[1]+dy
                if nx < 0 or nx >= levelgenerator.area[0]:
                    continue
                if ny < 0 or ny >= levelgenerator.area[1]:
                    continue
                if levelgenerator.grid[ny][nx].collapsed or levelgenerator.vis[ny][nx]:
                    continue
                # we find next tile
                print(f'add {nx}, {ny}')
                q.put((levelgenerator.grid[ny][nx].entropy, o[1]+1, nx, ny))
        print('q is not empty' if q else 'q is empty')
    
    def get_state(self):
        if self.entropy > 0:
            return 0
        return self.state


class LevelGenerator2D:
    """
    Level Generator 2D
    - utilizes Wave Function Collapse to generate 2D levels given:
        - world (engine.world.World)
        - tiles (a list of [Tile2D])
        - width (int)
        - height (int)
    """
    def __init__(self, world, tiles, width, height):
        self.world = world
        self.tiles = tiles
        self.queue = deque()
        self.area = (width, height)
        self.grid = [[WCFTile(self, x, y) for x in range(width)] for y in range(height)]
        self.vis = [[False for x in range(width)] for y in range(height)]

        # stats
        self.stats = {"checks": 0, "area": self.area}

    def check_valid_state_tiles(self, tile, pos):
        self.stats["checks"]+=1
        for pstate in tile.possible_states:
            if not pstate:
                continue
            # current tile, check nearby tiles, if they can accept current tile, otherwise
            if not self.tiles[pstate-1].check_valid(self, pos[0], pos[1]):
                tile.possible_states[pstate-1] = 0

    def collapse(self):
        # start from center
        while self.queue:
            # reset vis array
            for x in range(self.area[0]):
                for y in range(self.area[1]):
                    self.vis[y][x] = False
            self.queue = deque(sorted(self.queue, key=lambda x: (x[0], x[1], x[2])))
            # collect tile
            o = self.queue.popleft()
            tid = o[0]
            tile = self.grid[o[2]][o[1]]
            # print(o)
            tile.collapse()
            tile.propagate_changes(self)
            print(tile.possible_states)
        print(self.stats)
    
    def iter_collapse(self):
        if not self.queue:
            print(self.stats)
            return
        # reset vis array
        for x in range(self.area[0]):
            for y in range(self.area[1]):
                self.vis[y][x] = False
        self.queue = deque(sorted(self.queue, key=lambda x: (x[0], x[1], x[2])))
        # collect tile
        o = self.queue.popleft()
        tid = o[0]
        tile = self.grid[o[2]][o[1]]
        # print(o)
        print(tile.possible_states)

        tile.collapse()
        tile.propagate_changes(self)





