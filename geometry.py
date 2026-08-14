import math

# --- PERSEGI ---
def luas_persegi(sisi):
    """Menghitung luas persegi: sisi x sisi"""
    return sisi * sisi

def keliling_persegi(sisi):
    """Menghitung keliling persegi: 4 x sisi"""
    return 4 * sisi


# --- PERSEGI PANJANG ---
def luas_persegi_panjang(panjang, lebar):
    """Menghitung luas persegi panjang: panjang x lebar"""
    return panjang * lebar

def keliling_persegi_panjang(panjang, lebar):
    """Menghitung keliling persegi panjang: 2 x (panjang + lebar)"""
    return 2 * (panjang + lebar)


# --- LINGKARAN ---
def luas_lingkaran(jari_jari):
    """Menghitung luas lingkaran: pi x r^2"""
    return math.pi * (jari_jari ** 2)

def keliling_lingkaran(jari_jari):
    """Menghitung keliling lingkaran: 2 x pi x r"""
    return 2 * math.pi * jari_jari