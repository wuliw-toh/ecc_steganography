import numpy as np
import ecc_library as e_lib

#общие функции
def dec_to_bin(value):
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

def scotch_global(value):
    """Универсальная функция склеивания"""
    out = np.array([],int)
    for i in value:
        out = np.concatenate((out,i),0)
    return out




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
    
    
    
class precoder:

    def __init__(self,t):
        """
        Принимает длинну информационной последовательности
        """
        self.t = t


    def long_cut(self,mas):
        """
        Нарезает длинный битовый массиф на кусочки для кодирования
        Вход:
        mas - длинный массив 
        t - число информационных символов в кодовой системе
        Вывод:
        Массив массивов нужных длинн
        """
        long_ost = len(mas) % self.t

        if long_ost != 0:
            dop = np.zeros((self.t - long_ost),int)
            mas = np.concatenate((mas,dop),0)

        num = len(mas) / self.t
        return np.split(mas,num)

    def long_cutoff(self,mas,chek_stop):
        """
        Фуекция преднозначена для отсечки лишних символов секретного сообщения
        Вход:
        mas - длинная последовательность 
        chek_stop - когда эта последовательность найдена работа прекращается
        Выход:
        out - Укороченный масиив кодовых символов

        """
        long_mas = self.long_cut(mas)
        out = []
        for i in long_mas:
            if (sum(i == chek_stop)/self.t) > 0.95:
                break
            out.append(i)
        return out
                

class ecc_strem:
    #параметры кода 
    g_x = None #Пораждающий полином 
    n_cod = 0 #Длинна блока 
    k_cod = 0 #Длинна информационной последовательности 
    t_cod = 0 #Число испровляемых ошибок. 
    
    def __init__(self,n,k,t):
        """
        Инициализирует поток кодирования
        Принимает 3 параметра кода:
        n - длинна блока 
        k - число информационных символов 
        t - число исправляемых ошибок 
        Внимание! Код должен существовать в библиотеке!
        """
        self.n_cod = n
        self.k_cod = k
        self.t_cod = t
        
        vrem = str(n) + "_" + str(k) + "_" + str(t)
        self.g_x = polinom(dec_to_bin(e_lib.lib_g_x[vrem]),self.n_cod)
    
    def coding_work(self,mas_in):
        """
        Основной рабочий цикл кодирования 
        Вход - битовый массив из прекодера. 
        Выход - закодированный массив 
        """
        
        return np.array([self.coding_blok(x) for x in mas_in])
    
    def coding_blok(self,value):
        """
        Кодировник одного блока 
        Вход - Информационная последовательность
        Выход - Кодированное слово 
        """
        u_cod = polinom(value,self.n_cod)
        out = u_cod * self.g_x
        return out.main_mas
    
    
    def decoding_work(self,mas_in):
        """
        Основной цикл декодирования
        Вход - нарезанная битовая последовательность
        Выход - массив полиномов 
        """
        return np.array([self.decoding_blok(x) for x in mas_in])
    
       
    def decoding_blok(self,value):
        """
        Декодирование одного блока с исправлением ошибок
        Вход - массив коэфицентов длинной N
        Выход - полином длинной K
        """
        f_log = open("/home/wuliw/Рабочий стол/ВКР/Logs/log_ecc_decoding.txt","w")
        f_log.write("Старт декодирования\n")
        n = 0
        work_p = polinom(value,self.n_cod)
        f_log.write(str(work_p.main_mas)+ "\n")
        ost = work_p % self.g_x
        f_log.write(str(ost.main_mas)+ "\n")
        f_log.write("Проверка остатка и старт цикла\n")
        if sum(ost.main_mas) != 0:       
            while self.t_cod < sum(ost.main_mas):
                n += 1
                work_p = work_p << 1
                f_log.write("p"+str(work_p.main_mas)+ "\n")
                ost = work_p % self.g_x
                f_log.write("o"+str(ost.main_mas)+ "\n")
                
                if n > self.n_cod:
                    f_log.write(f"Выполнение выхода при n = {n}\n")
                    break
            f_log.write("конец цикла\n")
            work_p = work_p + ost
            f_log.write("полином после сложения\n")
            f_log.write(str(work_p.main_mas)+ "\n")
            work_p = work_p >> n
            f_log.write("полином после сдвига\n")
            f_log.write(str(work_p.main_mas)+ "\n")

        long_pol = work_p / self.g_x
        f_log.write("итог\n")
        f_log.write(str(long_pol.main_mas) + "\n")

        f_log.close()
        return polinom(long_pol.main_mas[(self.n_cod - self.k_cod):],self.k_cod).main_mas
    
    
class ecc_editor:
    
    def __init__(self,name_cod):
        """Принимает имя кода"""
        mas = list(map(int,name_cod.split("_"))) 
        self.ecc_work = ecc_strem(mas[0],mas[1],mas[2])
        self.n = mas[0]
        self.k = mas[1]
        self.t = mas[2]
        
    def cod_work(self,treak):
        """Принимает путь к файлу"""
        fail = FailBin(treak)
        precod = precoder(self.k)  
        mas_word = precod.long_cut(fail.read_bin())        
        out =  self.ecc_work.coding_work(mas_word)
        return scotch_global(out)
    
    def decoding_work(self,long_bin,stop_point = None,cut = False):
        """Принимает длинную кодовую комбинацию"""
        precod = precoder(self.n)
        if not(cut):
            mas = precod.long_cut(long_bin)
        else:
            mas = precod.long_cutoff(long_bin,stop_point)
            
        out = self.ecc_work.decoding_work(mas)
        return scotch_global(out)
