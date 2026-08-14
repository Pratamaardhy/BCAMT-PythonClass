# class Animal:
#     def __init__(self, name, species, age, color):
#         self.name = name
#         self.__species = species
#         self.age = age
#         self.color = color
#     def get_species(self):
#         return self.__species
#     def set_species(self, species):
#         self.__species = species

# class kucing(Animal):
#     pass

# animal1 = Animal("Buddy", "cat", 5, "Brown")
# print(f"Animal Name: {animal1.name}, Species: {animal1.get_species()}, Age: {animal1.age}, Color: {animal1.color}")

# kucing1 = kucing("Whiskers", "cat", 2, "Gray")
# print(f"Kucing Name: {kucing1.name}, Species: {kucing1.get_species()}, Age: {kucing1.age}, Color: {kucing1.color}")


class Kendaraan:
    def __init__(self, merk, tipe, tahun):
        self.merk = merk
        self.tipe = tipe
        self.tahun = tahun

    def info(self):
        return f"{self.merk} {self.tipe} ({self.tahun})"
    

class Mobil(Kendaraan):
    def __init__(self, merk, tipe, tahun, jumlah_pintu):
        super().__init__(merk, tipe, tahun)
        self.jumlah_pintu = jumlah_pintu

    def info(self):
        return f"{super().info()} - Jumlah Pintu: {self.jumlah_pintu}"
    
    def majukan(self):
        print(f"drive {self.merk} {self.tipe} maju")

class Motor(Kendaraan):
    def __init__(self, merk, tipe, tahun, jenis_motor):
        super().__init__(merk, tipe, tahun)
        self.jenis_motor = jenis_motor

    def info(self):
        return f"{super().info()} - Jenis Motor: {self.jenis_motor}"

    def majukan(self):
        print(f"drive {self.merk} {self.tipe} maju")

print("=== Informasi Kendaraan ===")
mobil1 = Mobil("Toyota", "Avanza", 2020, 4)
print(mobil1.info())
mobil1.majukan()

motor1 = Motor("Honda", "CBR", 2021, "Sport")
print(motor1.info())
motor1.majukan()    


