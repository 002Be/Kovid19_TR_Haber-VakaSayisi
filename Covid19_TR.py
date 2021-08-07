#Import
import re
import time
import urllib
import requests
from bs4 import BeautifulSoup

def covidVakaVeriCekimi():
    #Dosya
    file = open("Covid19_KayitDosyasi.txt","w",encoding="utf-8")
    #Web sayfası
    url = 'https://news.google.com/covid19/map?hl=tr&gl=TR&ceid=TR%3Atr'
    html = requests.get(url).content
    soup = BeautifulSoup(html, "html.parser")
    list = soup.find_all("tr",{"class":"sgXwHf wdLSAe YvL7re"})
    list2 = soup.find_all("div",{"class":"UvMayb"})
    l1 = list2[0].text
    l2 = list2[1].text
    l3 = list2[2].text

    print(f"\nTüm dünyada: Toplam vaka sayısı {l1} | Yeni vaka sayısı (14 gün) {l2} | Vefat sayısı {l3}\n")

    #Site içi arama
    for i in list:
        #Ülke isimleri
        ulkeAdi = i.find("div",{"class":"pcAJd"})
        ulkeAdi = ulkeAdi.text

        #Hasta sayısı
        toplamVakaSayisi = i.find_all("td")
        t1 = toplamVakaSayisi[0].text
        t2 = toplamVakaSayisi[1].text
        t3 = toplamVakaSayisi[-2].text
        t4 = toplamVakaSayisi[-1].text

        #Kayıt
        file.write(f"{ulkeAdi} | Toplam vaka sayısı: {t1} | Yeni vakalar: {t2} | 1 milyon kişi başına vaka sayısı: {t3} | Vefat sayısı: {t4} \n")
    file.close()

    print("Çıkış yapmak için 'q' tuşunu tuşlayınız.")

    #Arama
    while True:
        dosyaAra = open("Covid19_KayitDosyasi.txt", "r", encoding ="utf-8")
        aranan = input("Aramak istediğiniz ülkeyi giriniz ➢  ").capitalize()
        arananBurada = dosyaAra.read().find(aranan)
        dosyaAra.close()
        if arananBurada != -1:
            dosyaAra1  = open("Covid19_KayitDosyasi.txt", "r", encoding ='utf-8')
            aramaS = dosyaAra1.read()
            arananOge = re.findall(aranan+".*$",aramaS,re.MULTILINE)
            dosyaAra1.close()
            for aramaX in arananOge:
                print(aramaX,"\n")
        elif aranan == "Q":
            break
        else:
            print("Hatalı ülke ismi!\n")

    from os import remove
    remove("Covid19_KayitDosyasi.txt")

def covidHaberVeriCekimi():
    url = 'https://news.google.com/rss/search?q=kovid%2019&hl=tr&gl=TR&ceid=TR%3Atr'
    ayim = urllib.request.urlopen(url)
    sayfa = ayim.read()
    ayim.close()
    sayfaVeri = BeautifulSoup(sayfa,"xml")
    kaynak = sayfaVeri.findAll("item")

    zamanAyari = int(input("1 saniye ve üstünde tam sayı değeri giriniz\nHaberin kaç saniye ekranda kalacağını ayarlayınız ➢  "))

    for bilgi in kaynak:
        haberZamani = bilgi.pubDate.text
        haberBasligi = bilgi.title.text
        haberLinki = bilgi.link.text
        haberAyiraci = 100 * "▁"
        time.sleep(zamanAyari)
        print(f"Haber başlığı: {haberBasligi} \nHaber zamanı: {haberZamani} \nHaber linki: {haberLinki} \n {haberAyiraci} \n")

while True:
    select = input("1- Kovid 19 ile ilgili haberler \n2- Ülkelere göre kovid 19 vaka sayıları \n3- Çıkış\n\n ➢  ")
    if select == "1":
        covidHaberVeriCekimi()
    elif select == "2":
        covidVakaVeriCekimi()
    else:
        print("Çıkış")
        break