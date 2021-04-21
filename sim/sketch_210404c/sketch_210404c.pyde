# Ayarlar
# Birey sayısı
NUMBER_OF_ENTITIES = 100
# Bir bireyin hastalıklı olma olasılığı
INFACTION_RATIO = 35
# Bireylerin hastalığı yayma olasılığı
INFECT_RATIO = 20
# Bireylerin hızı
ENTIT_VELO = 5
# Bireylerin iyileşme olasılığı
HEALING_RATIO = 10
# Bireylerin iyileşme olasılığı
DIE_ORATIO = 2
# Riskli olma olasılığı
RISL_RATIO = 20
# Doğum olasılığı
BIRTH_RATE = 20
# Ölüm sayısı
DEATH_COUNT = 0
# İyileşme sayısı
HEALING_COUNT = 0
# Kare sayısı
FRAME_COUNT = 0

# Setup fonksiyonu
def setup():
    # global scope değişkenleri
    global entities
    # Pencere boyutu
    size(500, 500)
    # Birey listesi oluşturma
    # RISL_RATIO ihtimalle riskli, INFACTION_RATIO olasılığınca hastalıklı, NUMBER_OF_ENTITIES kadar birey oluşturma
    entities = [Entity(infected=random(100) < INFACTION_RATIO, risk=10 if random(100) < RISL_RATIO else 0) for _ in range(NUMBER_OF_ENTITIES)]
    
# draw fonksiyonu
def draw():
    # global scope değişkenleri
    global DEATH_COUNT, HEALING_COUNT, FRAME_COUNT
    # Arka alanı koyu gri yap
    background(52)
    # Hastalıklı sayısı değişkeni.
    INFECTED_COUNT = 0
    # Tüm bireylerde dönen döngü
    for i in range(len(entities) - 1, -1, -1):
        # n. bireyi hareket ettir
        entities[i].move()
        # n. bireyi göster
        entities[i].show()
        # n. bireyin diğer bireylerle etkileşip hastalanma durumunu incele
        entities[i].infect(entities)
        
        # n. bireyin iyileşme olasılığına göre iyileştir.
        # iyileşitse iyileşme sayısını bir arttır
        if entities[i].healing():
            HEALING_COUNT += 1
        # n. bireyin ölme olasılığına göre öldür (Bireyler listesinden çıkar).
        # ölürse ölüm sayısını bir arttır
        if entities[i].die():
            del entities[i]
            DEATH_COUNT += 1
    # BIRTH_RATE ihtimalince bir birey doğsun (Bireyler listesine bir birey ekle)
    if random(100) < BIRTH_RATE:
        entities.append(Entity(infected=False))
    
    # Tüm bireyleri kontrol edin hasta birey saysını bul
    it = 0
    for ent in entities:
        if ent.infected:
            it += 1
    
    # Eğer hasta birey sayısı sıfır ise, simülasyonu durdur
    if it == 0:
        noLoop()
        print(FRAME_COUNT)
        #print(DEATH_COUNT, HEALING_COUNT, len(entities), len(entities) - 200 + DEATH_COUNT)
        
    # Ekrana Ölen birey saısını yaz
    FRAME_COUNT += 1
    textSize(32);
    fill(0, 255, 0)
    text("Olen sayisi={}".format(DEATH_COUNT), 0, 32)
    
    # Hastalıklı birey sayısının toplam nüfusa oranını bir dosyaya yaz
    """with open("no_lock_down.dat", "a") as file:
        file.write("{}, {}\n".format(FRAME_COUNT, 100 * INFECTED_COUNT/len(entities)))"""
    

# Birey sınıfı
class Entity:
    # constructor metod
    # pozisyon, hastalıklı olma durumu ve riskli olma durumunu seçimli olarak alır
    def __init__(self, pos=None, infected=False, risk=0):
        # Birey göstermek için çizilecek dairenin yarıçapı
        self.r = 5
        # Pozisyon bilgisi geldiyse al yoksa rastgele oluştur
        self.pos = pos or PVector(random(self.r, width - self.r), random(self.r, height - self.r))
        # Rastgele yönde ve ENTIT_VELO şiddetinde bir hız vektörü oluştur
        self.vel = PVector().random2D().setMag(ENTIT_VELO)
        # Enfekte olup olmadığı bilgisi
        self.infected = infected
        # Enfekte olarak geçirilen süre
        self.infection_days = 0
        # Bireyin toplam riski
        self.risk = DIE_ORATIO + risk
        # Enfkte edebilme oranı
        self.infection_risk = INFECT_RATIO
        
    # Bireyi gösterme metodu
    def show(self):
        # Eğer birey enfekte ise
        if self.infected:
            # Enfekte olarak geçirilen süreyi bir arttır
            self.infection_days += 1
            
            if self.risk == DIE_ORATIO:
                # Eğer risk grubunda değil ise yeşi olarak göster
                fill(255, 0, 0, 255)
            else:
                # Eğer risk grubunda ise sarı olarak göster
                fill(255, 255, 0, 255)
        else:
            # Eğer birey enfekte değilse
            if self.risk == DIE_ORATIO:
                # Eğer risk grubunda değil ise yeşi olarak göster
                fill(0, 255, 0, 255)
            else:
                # Eğer risk grubunda ise turkuaz olarak göster
                fill(0, 255, 255, 255)
            
        # Çerçeve çizme
        noStroke()
        # x ve y pozisyonunda 2r çapında bir daire çiz
        circle(self.pos.x, self.pos.y, self.r * 2)
        
    # Bireyi hareket ettirme metodu
    def move(self):
        # 150. ile 175. kareler arasında hareket ettirme
        if not 150 < FRAME_COUNT%500 < 175:
            # Kenarlardan sek
            self.bouce()
            # Hız miktarınca hareket et
            self.pos.add(self.vel)
        
    # Kenarlardan sekme metodu
    def bouce(self):
        # Eğer x ekseninde ekranda değilse
        if not self.r < self.pos.x < width - self.r:
            # Hızı ters çevir
            self.vel.x *= -1
            # Bireyi ekranın içine ışınla
            self.pos.x = self.r + 1 if self.pos.x < self.r else width - (self.r + 1)
            
        # Eğer y ekseninde ekranda değilse
        if not self.r < self.pos.y < height - self.r:
            # Hızı ters çevir
            self.vel.y = - self.vel.y
            # Bireyi ekranın içine ışınla
            self.pos.y = self.r + 1 if self.pos.y < self.r else height - (self.r + 1)
            
    # Etkileşme sonucu bireylerin hastalığı yayma metodu
    def infect(self, others):
        # Tüm bireylerde bir döngü oluştur
        for other in others:
            # Eğer listedeki diğer birey şu anki birey değilse
            if other is not self:
                # İki birey arasındaki uzaklığı hesapla
                d = dist(self.pos.x, self.pos.y, other.pos.x, other.pos.y)
                # Eğer iki birey çarpıştıysa
                if d <= self.r + other.r:
                    # Her iki bireyin rastgele bir göne sektir
                    self.vel = PVector().random2D().setMag(ENTIT_VELO)
                    other.vel = PVector().random2D().setMag(ENTIT_VELO)
                    
                    # Eğer bu birey enfekte ve diğeri değilse
                    if self.infected and not other.infected:
                        # Diğer birey infection_risk olasılığınca enfekte olsun
                        other.infected = random(100) < self.infection_risk
                        # Diğerin enfekte riskini yarıya indir. Böylece bir bireyin tekrar enfekte olma olasılığı düşer
                        other.infection_risk /= 2
                        # Eper enfekte edilmediyse enfekte olarak geçirilen süreyi sıfırla
                        if not other.infected:
                            other.infection_days = 0
                        
                    # Önceki blokla yanı şey sadece bu birey ve diğer birey yer değiştimiş
                    if not self.infected and other.infected:
                        self.infected = random(100) < self.infection_risk
                        self.infection_risk /= 2
                        if not self.infected:
                            self.infection_days = 0
                         
    # Bireyin iyileşme metodu   
    def healing(self):
        # Eğer birey enfekte ise
        if self.infected:
            # 250 gün üzeri için tamamen iyileşsin
            if self.infection_days > 250:
                self.infected = False
            # 200 gün üzeri için %HEALING_RATIO + 20 ihtimalle iyileştir
            elif self.infection_days > 200:
                self.infected = not(random(100) < HEALING_RATIO + 20)
            # 150 gün üzeri için %HEALING_RATIO + 10 ihtimalle iyileştir
            elif self.infection_days > 150:
                self.infected = not(random(100) < HEALING_RATIO + 10)
            # 100 gün üzeri için %HEALING_RATIO ihtimalle iyileştir
            elif self.infection_days > 100:
                self.infected = not(random(100) < HEALING_RATIO)
                
            # İyileştiyse enfekte olarak geçirilen süreyi sıfırla
            if not self.infected:
                self.infection_days = 0
                # İyileştiğine dair bilgi ver
                return True

        # İyileşmediğine dair bilgi ver
        return False
                
    # Bireyin ölme metodu  
    def die(self):
        # Eğer birey enfekte ise
        if self.infected:
            # 150 gün üzeri için ölme ihtimali self.risk + 4
            if self.infection_days > 150:
                return random(100) < self.risk + 4
            # 150 gün üzeri için ölme ihtimali self.risk + 2
            elif self.infection_days > 100:
                return random(100) < self.risk + 2
            # 150 gün üzeri için ölme ihtimali self.risk
            elif self.infection_days > 30:
                return random(100) < self.risk
            
        # Ölmediğine dair bilgi ver
        return False
        
        
        
        
        
        
