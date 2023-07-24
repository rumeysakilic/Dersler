import sqlite3

# Veritabanı bağlantısı kurulur.
con = sqlite3.connect('bankaa.db')
crs = con.cursor()

# Tablo oluşturulur.
crs.execute('''CREATE TABLE IF NOT EXISTS kullanici
            (tc_no INT NOT NULL PRIMARY KEY,
             parola TEXT,
             bakiye INT)''')

def menuye_don():
    don = input("Menüye dönmek istiyorsanız 'E' ye basınız!")
    if don == 'E':
       menu()

def menu():
    print("1 => GOSTER          ")
    print("2 => NAKİT EKLE      ")
    print("3 => NAKİT ÇEK       ")
    print("4 => NAKİT GÖNDER    ")
    print("5 => ÇIKIŞ           ")
    secim = input("Birini Seçiniz: ")

    # Kullanıcının tc sini al
    tc_no = input("TC kimlik numaranızı giriniz: ")

    # Kullanıcıyı veri tabanından getir
    kullanici = kullanici_getir(tc_no)       #fetchone ile demet şeklinde alır
    if kullanici:
        bakiye = kullanici[2]
    else:
        bakiye = 0

    if   secim == '1':
        print(f"Hoş Geldiniz, {tc_no}! Mevcut bakiyeniz {bakiye:.2f} TL.\n")
        menuye_don()

    elif secim == '2':
        ekle = float(input("Ne kadar eklemek istiyorsunuz?: "))
        bakiye += ekle
        print(f"{ekle:.2f} TL hesabınıza eklendi.\n")
        with con:
            crs.execute("UPDATE kullanici SET bakiye=? WHERE tc_no=?", (bakiye, tc_no))
        menuye_don()

    elif secim == '3':
        cek = int(input("Ne kadar nakit çekmek istiyorsunuz?: "))
        if bakiye >= cek:
            bakiye -= cek
            print(f"{cek:.2f} TL hesabınızdan başarı ile çekildi\n")
            with con:
                crs.execute("UPDATE kullanici SET bakiye=? WHERE tc_no=?", (bakiye, tc_no))
        else :
            print("Mevcut bakiye yetersiz. En fazla çekebileceğiniz miktar {}".format(kullanici[2]))
        menuye_don()

    elif secim == '4':
        nakit_gonder = int(input("Gondermek istediğiniz miktarı giriniz: "))

        if bakiye >= nakit_gonder:
            alıcı = int(input("Gönderilecek kişinin TC kimlik no'sunu giriniz: "))
            kullanici = kullanici_getir(alıcı)
            alıcı_bakiye = kullanici[2]
            bakiye -=nakit_gonder
            alıcı_bakiye +=nakit_gonder
            print("Para başarı ile gönderildi!!!")
            with con:
                crs.execute("UPDATE kullanici SET bakiye=? WHERE tc_no=?", (bakiye, tc_no))
                crs.execute("UPDATE kullanici SET bakiye=? WHERE tc_no=?", (alıcı_bakiye, alıcı))

        else:
            print("Mevcut bakiye yetersiz!! En fazla çekebileceğiniz miktar{}".format(kullanici[2]))
        menuye_don()

    elif secim == '5':
        ana_ekran()

def ana_ekran():
    print("1 => GİRİŞ")
    print("2 => KAYIT OL ")
    secim = input("Birini Seçiniz: ")

    if   secim == "1":
        giris()
    elif secim == "2":
        kayit_ol()
    else:
        print("Hatalı Seçim!!!")
        ana_ekran()

def giris():
    tc_no  = input("TC kimlik numaranızı giriniz: ")
    parola = input("Parolanızı giriniz: ")
    crs.execute("SELECT * FROM kullanici WHERE tc_no = ? AND parola = ? ",(tc_no,parola,))
    kullanici = crs.fetchone()

    if kullanici is None:
        print("Kullanıcı adı veya parola hatalı!!!")
        ana_ekran()
    else:
        print("Bankamıza Hoş Geldiniz!")
        menu()

def kayit_ol():
    tc_no  = int(input("TC kimlik numaranızı giriniz: "))
    parola = input("Parolanızı giriniz: ")
    bakiye = int(input("Bakiyenizi giriniz: "))
    crs.execute("INSERT INTO kullanici VALUES(?,?,?)",(tc_no,parola,bakiye))
    con.commit()

    print("Kayt başarılı bir şekilde gerçekleşti!")
    menu()

# Kullanıcı bilgilerini veritabanından getirir
def kullanici_getir(tc_no):
    crs.execute("SELECT * FROM kullanici WHERE tc_no=?", (tc_no,))
    return crs.fetchone()

ana_ekran()

con.close()