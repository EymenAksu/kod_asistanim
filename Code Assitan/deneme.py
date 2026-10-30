import random
import time
import sys

class Karakter:
    def __init__(self, isim, sinif):
        self.isim = isim
        self.sinif = sinif
        self.seviye = 1
        self.tp = 0
        self.altin = 50
        self.iksir = 2
        
        if sinif == "Savaşçı":
            self.maks_can = 120
            self.can = 120
            self.hasar = 18
            self.savunma = 5
        elif sinif == "Büyücü":
            self.maks_can = 80
            self.can = 80
            self.hasar = 25
            self.savunma = 2
        elif sinif == "Okçu":
            self.maks_can = 100
            self.can = 100
            self.hasar = 21
            self.savunma = 3

    def durum_goster(self):
        print(f"\n=== {self.isim} ({self.sinif}) - Seviye {self.seviye} ===")
        print(f"Can: {self.can}/{self.maks_can} | Hasar: {self.hasar} | Savunma: {self.savunma}")
        print(f"Altın: {self.altin} | Pot: {self.iksir} | TP: {self.tp}/100")
        print("========================================\n")

    def can_yenile(self):
        self.can = self.maks_can
        print(f"\n[HİLE] Canınız tamamen yenilendi! Mevcut Can: {self.can}/{self.maks_can}")

    def guc_ver(self):
        self.hasar += 100
        print(f"\n[HİLE] İlahi bir güç elinize ulaştı! Hasarınız +100 artırıldı. Yeni Hasar: {self.hasar}")

    def boss_isinla(self):
        self.seviye = 3
        self.maks_can += 50
        self.can = self.maks_can
        self.hasar += 30
        self.altin += 500
        print("\n[HİLE] Zamanı büktünüz! Seviyeniz 3 yapıldı, can ve hasar değerleriniz artırıldı ve Ejderha İnine ışınlanıyorsunuz!")

    def seviye_kontrol(self):
        if self.tp >= 100:
            self.seviye += 1
            self.tp -= 100
            self.maks_can += 20
            self.can = self.maks_can
            self.hasar += 5
            print(f"\n🎉 TEBRİKLER! Seviye Atladınız! Yeni Seviye: {self.seviye} 🎉")
            print("Canınız tamamen dolduruldu, gücünüz arttı!")

class Dusman:
    def __init__(self, isim, can, hasar, tp_odulu, altin_odulu):
        self.isim = isim
        self.can = can
        self.maks_can = can
        self.hasar = hasar
        self.tp_odulu = tp_odulu
        self.altin_odulu = altin_odulu

def hile_menusu(oyuncu):
    print("\n--- GİZLİ HİLE KONSOLU ---")
    print("Kullanabileceğiniz hile kodları:")
    print("  -> 'guc_ver' : Saldırı gücünü +100 artırır.")
    print("  -> 'can_yenile' : Canı tamamen doldurur.")
    print("  -> 'boss_isinla' : Direkt seviye 3 yapar ve finale ışınlar.")
    kod = input("Hile kodunu girin (veya çıkmak için Enter'a basın): ").strip()
    
    if kod == "guc_ver":
        oyuncu.guc_ver()
    elif kod == "can_yenile":
        oyuncu.can_yenile()
    elif kod == "boss_isinla":
        oyuncu.boss_isinla()
        return "boss"
    elif kod == "":
        print("Hile konsolu kapatıldı.")
    else:
        print("Geçersiz hile kodu!")
    return None

def savas(oyuncu, dusman):
    print(f"\n⚔️ vahşi bir {dusman.isim} ile karşılaştın! ⚔️")
    
    while dusman.can > 0 and oyuncu.can > 0:
        print(f"\n{dusman.isim} Canı: {dusman.can}/{dusman.maks_can}")
        print(f"Senin Canın: {oyuncu.can}/{oyuncu.maks_can} | Pot: {oyuncu.iksir}")
        secim = input("Eylem Seçin (1: Saldır, 2: İksir İç, 'hile': Hile Konsolu): ").strip().lower()
        
        if secim == "hile":
            sonuc = hile_menusu(oyuncu)
            if sonuc == "boss":
                return "boss_isinlanma"
            continue
        elif secim == "1":
            hasar = random.randint(oyuncu.hasar - 4, oyuncu.hasar + 4)
            dusman.can -= hasar
            print(f"\n🗡️ {dusman.isim} düşmanına {hasar} hasar verdin!")
        elif secim == "2":
            if oyuncu.iksir > 0:
                oyuncu.can = min(oyuncu.maks_can, oyuncu.can + 40)
                oyuncu.iksir -= 1
                print(f"\n🧪 İksir içtin! 40 can yenilendi. Kalan can: {oyuncu.can}/{oyuncu.maks_can}")
            else:
                print("\nHepsi bitti! Hiç iksirin kalmadı!")
                continue
        else:
            print("Kararsızlıktan dolayı sıranı kaybettin!")

        if dusman.can <= 0:
            break

        # Düşman sırası
        dusman_hasari = max(1, random.randint(dusman.hasar - 2, dusman.hasar + 2) - oyuncu.savunma)
        oyuncu.can -= dusman_hasari
        print(f"💥 {dusman.isim} sana vurdu! {dusman_hasari} hasar aldın.")

    if oyuncu.can <= 0:
        print(f"\n💀 {dusman.isim} tarafından mağlup edildin... Macera sona erdi.")
        return False
    else:
        print(f"\n🏆 {dusman.isim} düşmanını yendin!")
        print(f"Kazanılan ödüller: +{dusman.tp_odulu} TP, +{dusman.altin_odulu} Altın!")
        oyuncu.tp += dusman.tp_odulu
        oyuncu.altin += dusman.altin_odulu
        oyuncu.seviye_kontrol()
        return True

def market(oyuncu):
    while True:
        print(f"\n=== KASABA MARKETİ (Altın: {oyuncu.altin}) ===")
        print("1. Sağlık İksiri (20 Altın) [+40 Can Yeniler]")
        print("2. Silah Bileme Taşı (30 Altın) [Kalıcı +3 Hasar]")
        print("3. Marketten Çık")
        secim = input("Almak istediğiniz ürünün numarasını girin: ").strip()
        
        if secim == "1":
            if oyuncu.altin >= 20:
                oyuncu.altin -= 20
                oyuncu.iksir += 1
                print("\n🧪 Bir Sağlık İksiri satın aldın!")
            else:
                print("\nYetersiz altın!")
        elif secim == "2":
            if oyuncu.altin >= 30:
                oyuncu.altin -= 30
                oyuncu.hasar += 3
                print("\n⚔️ Silahını biledin! Hasarın kalıcı olarak +3 arttı.")
            else:
                print("\nYetersiz altın!")
        elif secim == "3":
            break

def oyun_baslat():
    print("=== KRALLIĞIN KADERİ: HİLELİ RPG ===")
    isim = input("Kahramanınızın ismi nedir?: ")
    print("\nSınıfınızı Seçin:")
    print("1. Savaşçı (Yüksek Can ve Defans)")
    print("2. Büyücü (Yüksek Hasar, Düşük Can)")
    print("3. Okçu (Dengeli Güç)")
    
    sinif_secimi = input("Sınıf numarası seçin (1-3): ").strip()
    sinif_adi = "Savaşçı"
    if sinif_secimi == "2":
        sinif_adi = "Büyücü"
    elif sinif_secimi == "3":
        sinif_adi = "Okçu"
        
    oyuncu = Karakter(isim, sinif_adi)
    print(f"\nHoş geldin, Seviye {oyuncu.seviye} {oyuncu.sinif} {oyuncu.isim}!")

    dusmanlar = [
        ("Lağım Faresi", 30, 8, 40, 15),
        ("Haydut", 50, 12, 60, 25),
        ("Kara Kurt", 40, 10, 50, 20),
        ("Orman Trolü", 75, 15, 80, 40)
    ]

    hileli_boss_tetiklendi = False

    while oyuncu.can > 0:
        if oyuncu.seviye >= 3 or hileli_boss_tetiklendi:
            # Boss Savaşı
            print("\n🔥 GÖKLER KARARIYOR VE YER SARSILIYOR... 🔥")
            print("Karanlık mağaranın derinliklerinde kadim bir kükreme duyuluyor.")
            print("KADİM EJDERHA KRALI uykusundan uyandı!")
            time.sleep(1.5)
            
            boss = Dusman("Kadim Ejderha Kralı", 250, 28, 500, 1000)
            sonuc = savas(oyuncu, boss)
            
            if sonuc == "boss_isinlanma":
                hileli_boss_tetiklendi = True
                continue
            elif sonuc:
                print(f"\n👑 TEBRİKLER KAHRAMAN! 👑")
                print(f"{oyuncu.isim}, Kadim Ejderha Kralı'nı yenerek krallığı ebedi karanlıktan kurtardı!")
                print("Oyunu başarıyla bitirdiniz. Efsaneniz dilden dile dolaşacak...")
            else:
                print("\nKrallık ejderhanın alevleri altında yok oldu...")
            break
            
        oyuncu.durum_goster()
        print("Ne yapmak istersiniz?")
        print("1. Keşfe Çık (Savaşa Git)")
        print("2. Kasaba Marketine Git")
        print("3. Dinlen (+15 Can yeniler - 10 Altın)")
        print("4. Hile Konsolunu Aç")
        print("5. Oyundan Çık")
        
        secim = input("Seçiminiz: ").strip()
        
        if secim == "1":
            secilen_dusman_bilgi = random.choice(dusmanlar)
            dusman = Dusman(*secilen_dusman_bilgi)
            sonuc = savas(oyuncu, dusman)
            if sonuc == "boss_isinlanma":
                hileli_boss_tetiklendi = True
        elif secim == "2":
            market(oyuncu)
        elif secim == "3":
            if oyuncu.altin >= 10:
                oyuncu.altin -= 10
                oyuncu.can = min(oyuncu.maks_can, oyuncu.can + 15)
                print(f"\n🛌 Han odasında dinlendiniz. Canınız {oyuncu.can} oldu.")
            else:
                print("\nYetersiz altın!")
        elif secim == "4":
            sonuc = hile_menusu(oyuncu)
            if sonuc == "boss":
                hileli_boss_tetiklendi = True
        elif secim == "5":
            print("\nOyundan ayrılıyorsunuz. Hoşça kalın!")
            break
        else:
            print("\nGeçersiz seçim!")

oyun_baslat()