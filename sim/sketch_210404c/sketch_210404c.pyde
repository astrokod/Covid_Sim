NUMBER_OF_ENTITIES = 100
INFACTION_RATIO = 35
INFECT_RATIO = 20
ENTIT_VELO = 5
HEALING_RATIO = 10
DIE_ORATIO = 2
BIRTH_RATE = 20
DEATH_COUNT = 0
HEALING_COUNT = 0
FRAME_COUNT = 0

def setup():
    global entities
    size(500, 500)
    
    entities = [Entity(infected=random(100) < INFACTION_RATIO, risk=10 if random(100) < 20 else 0) for _ in range(NUMBER_OF_ENTITIES)]
    
def draw():
    global DEATH_COUNT, HEALING_COUNT, FRAME_COUNT
    background(52)
    INFECTED_COUNT = 0
    for i in range(len(entities) - 1, -1, -1):
        entities[i].move()
        entities[i].show()
        entities[i].infect(entities)
        if entities[i].healing():
            HEALING_COUNT += 1
        if entities[i].die():
            del entities[i]
            DEATH_COUNT += 1
            
    if random(100) < BIRTH_RATE:
        entities.append(Entity(infected=False))
    
    it = 0
    for ent in entities:
        if ent.infected:
            it += 1
            
    if it == 0:
        noLoop()
        print(FRAME_COUNT)
        #print(DEATH_COUNT, HEALING_COUNT, len(entities), len(entities) - 200 + DEATH_COUNT)
        
    #print(100 * INFECTED_COUNT/len(entities))
    
    FRAME_COUNT += 1
    textSize(32);
    fill(0, 255, 0)
    text("Olen sayisi={}".format(DEATH_COUNT), 0, 32)
    """with open("no_lock_down.dat", "a") as file:
        file.write("{}, {}\n".format(FRAME_COUNT, 100 * INFECTED_COUNT/len(entities)))"""
    

class Entity:
    def __init__(self, pos=None, infected=False, risk=0):
        self.r = 5
        self.pos = pos or PVector(random(0, width), random(0, height))
        self.vel = PVector().random2D().setMag(ENTIT_VELO)
        self.infected = infected
        self.infection_days = 0
        self.risk = DIE_ORATIO + risk
        self.can_move = True
        self.infection_risk = INFECT_RATIO
        
    def show(self):
        if self.infected:
            self.infection_days += 1
            
            
        if self.infected:
            if self.risk == DIE_ORATIO:
                fill(255, 0, 0, 255)
            else:
                fill(255, 255, 0, 255)
        else:
            if self.risk == DIE_ORATIO:
                fill(0, 255, 0, 255)
            else:
                fill(0, 255, 255, 255)
            
        noStroke()
        circle(self.pos.x, self.pos.y, self.r * 2)
        
    def move(self):
        #if not 150 < FRAME_COUNT%500 < 175:
        self.bouce()
        self.pos.add(self.vel)
    
    def bouce(self):
        if not self.r < self.pos.x < width - self.r:
            self.vel.x = -self.vel.x
            self.pos.x = self.r + 1 if self.pos.x < self.r else width - (self.r + 1)
            
        if not self.r < self.pos.y < height - self.r:
            self.vel.y = - self.vel.y
            self.pos.y = self.r + 1 if self.pos.y < self.r else height - (self.r + 1)
            
    def infect(self, others):
        for other in others:
            if other is not self:
                d = dist(self.pos.x, self.pos.y, other.pos.x, other.pos.y)
                if d <= self.r + other.r:
                    self.vel = PVector().random2D().setMag(ENTIT_VELO)
                    other.vel = PVector().random2D().setMag(ENTIT_VELO)
                    
                    if self.infected and not other.infected:
                        other.infected = random(100) < self.infection_risk
                        other.infection_risk /= 2
                        if not other.infected:
                            other.infection_days = 0
                        
                    if not self.infected and other.infected:
                        self.infected = random(100) < self.infection_risk
                        self.infection_risk /= 2
                        if not self.infected:
                            self.infection_days = 0
                            
    def healing(self):
        if self.infected:
            if self.infection_days > 100:
                self.infected = not(random(100) < HEALING_RATIO)
            elif self.infection_days > 150:
                self.infected = not(random(100) < HEALING_RATIO + 10)
            elif self.infection_days > 200:
                self.infected = not(random(100) < HEALING_RATIO + 20)
            elif self.infection_days > 250:
                self.infected = False
                
            if not self.infected:
                self.infection_days = 0
                return True

            return False
                
    def die(self):
        if self.infected:
            if self.infection_days > 30:
                return random(100) < self.risk
            elif self.infection_days > 100:
                return random(100) < self.risk + 2
            elif self.infection_days > 150:
                return random(100) < self.risk + 4
            
        return False
        
        
        
        
        
        
