import numpy as np

class FailBin: 
    """Класс для специфической работы с файлами"""
    def __init__(self, treak):
        self.treak = treak
        
    def fuul_bait(self,value):
        """
        Преобразует число INT от 0 до 255 в массив длонной 8
        """
        mas_1 = dec_to_bin(value)
        mas_2 = np.zeros((8 - len(mas_1)),int)
        return np.concatenate((mas_2,mas_1),0)
     
    def scotch(self,value):
        """Переводит первоначальный документ в битовую последовательность"""
        out = np.array([],int)
        for i in value:
            out = np.concatenate((out,self.fuul_bait(i)),0)
        return out
     
    def dec_to_bin(self,value):
        """
        Вход - число типа int(10)
        Выход - Массив numpy в бинарном формате
        Дополнение. Если формат не DEC то можно пользоваться встроенной записью
        Для OCT - 0o.....
        Для HEX - 0x.....
        """
        vrem = bin(value)[2:]
        return np.array([int(x) for x in vrem])
    
    def bin_to_dec(self,value):
        """
        Вход - Массив numpy бинарного формата
        Выход - Число int(10)
        """
        work_mas = np.flip(value)
        out = 0
        for i in range(len(work_mas)):
            if work_mas[i] == 1:
                out += 2**i
        return out
    
    def read_bin(self):
        """Читат файл и переводит его в битовую последовательность (numpy.array)"""
        fail = open(self.treak,"rb")
        text = fail.read()
        fail.close()
        
        return self.scotch(text)
    
    def write_bin(self,value):
        """Принимает длинную битовую послеовательность и записывает в файл"""
        kol_bit = (len(value) // 8)
        ost = len(value) % 8
        if ost != 0:
            bit_text = np.array_split(value[:-ost],kol_bit)
        else:
            bit_text = np.array_split(value,kol_bit)
            
        fout = open(self.treak,"wb")
        for i in bit_text:
            fout.write(self.bin_to_dec(i).to_bytes(1,"big"))
        fout.close()
        
        
        
class polinom:
    #Блок переменных 
    main_mas = None #массив коэфицентов
    main_poli = None #Массив полиномов
    n_long = None
    
    #Блок основных функций
    def __init__(self,value,n = None):
        """
        Вход 
        value - Биннайрный массив numpy
        n - максимальна длинна полинома, если не указанна то это длинна массива 
        """
        if n == None : n = len(value)
        self.n_long = n
        
        self.main_mas = np.concatenate((np.zeros(n - len(value),int),value),0)
        self.main_poli = np.poly1d(value)
        
    def __str__(self):
        #Переписать перед релизом
        return str(self.main_poli)
    
    def __add__(self, other):
        vrem = self.main_poli + other.main_poli
        return self.new_pol(np.poly1d(vrem.coef % 2))
    
    def __mul__(self, other):
        vrem = self.main_poli * other.main_poli
        return self.new_pol(np.poly1d(vrem.coef % 2))
    
    def __truediv__(self, other):
        vrem = self.main_poli / other.main_poli
        return self.new_pol(np.poly1d(abs(vrem[0].coef) % 2))
    
    def __mod__(self, other):
        vrem = self.main_poli / other.main_poli
        return self.new_pol(np.poly1d(abs(vrem[1].coef) % 2))
    
    #Функции здвигов. ВНИМАТЕЛЬНО! 
    def __lshift__(self, n):
        return self.new_pol(np.poly1d(np.roll(self.main_mas, -n)))
    
    def __rshift__(self, n):
        return self.new_pol(np.poly1d(np.roll(self.main_mas, n)))
 
    #Блок вспомогательных функций 
    def new_pol(self,value):
        out = polinom(value.coef,self.n_long)
        return out
