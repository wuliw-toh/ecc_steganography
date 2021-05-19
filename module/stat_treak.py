import math
import ecc_library as e_lib

#функции для подбора полинома
def kol_fix_need(n,p):
    """Определение числа исправлений
    Вход:
    n - длинна блока 
    p - вероятность ошибки
    Выход:
    Nerr - число исправлений для 99,7% пакетов
    """
    M = p * n
    std = math.sqrt(p * n * (1-p))
    return M + 6*std

def find_g_x(n,Nerr):
    """Поиск полиномов в библиотеке 
    Вход:
    n - длинна блока
    Nerr - необходимое число исправлений 
    Выход:
    Имя подходящего полинома из библиотеки
    """
    for i in e_lib.lib_g_x.keys():
        chek = i.split("_")
        if int(chek[0]) == n:
            if int(chek[2]) >= Nerr:
                return i
    
def selection_g_x(p,excess = 1):
    """Функция выбора оптимального полинома
    Вход: 
    p - Вероятность ошибки 
    Выход:
    out - имя кода в библиотеке 
    lib_g_x[out] - определение полинома в 10-тичном формате
    """
    pol = []
    for x in e_lib.long_array:
        vrem = find_g_x(x,kol_fix_need(x,p) + excess)#тут +1 это запас под секрет! 
        if vrem != None:
            pol.append(vrem)
    
    out = ""
    max_speed = 0
    
    for i in pol:
        spl = i.split("_")
        real_sped = int(spl[1]) / int(spl[0])
        
        if real_sped > max_speed:
            max_speed = real_sped
            out = i
            
    return out,e_lib.lib_g_x[out]
 
    
    
#функции расчёта искуственной вероятности
def synthetic_p(p,n,Ne):
    """Расчёт синтетической вероятности 
    Вход:
    p - вероятность естественной ошибки
    n - длинна блока
    Ne - число исправлений 
    Выход:
    ps - искуственная вероятнсоть 
    """
    t_1 = (3*math.sqrt(n*(9*n*p**2+4*n*p*Ne+18*n*p-4*Ne**2+4*n*Ne+9*n)))/2
    t_2 = n**2*p-(9*n)/2 +(9*n*p)/2-n*Ne
    return -((t_1 + t_2)/(n*(n+9)))


def norm_p(bp,n):
    """Функция для вычисления реальной вероятности 
    Вход:
    bp - сокращение от "большая вероятность" уменьшаемое значение
    n - длинна блока 
    Выход:
    rp - реальная вероятность искуственной ошибки
    """
    top = -(n*bp**2)+n*bp+1
    return bp - (2*(2*bp+math.sqrt(top) - 1))/(n+4)

def selection_sintetik_p(p,name_cod):
    """Функция расчёта вероятности секретного бита
    Вход:
    p - вероятность естественной ошибки 
    name_cod - имя кода в библиотеке (к примеру 7_4_1)
    Выход:
    ps - вероятность секретного бита
    """
    mas = list(map(int,name_cod.split("_")))
    work_p = synthetic_p(p,mas[0],mas[2]) * 2
    return norm_p(work_p,mas[0])