import math

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
    return M + 3*std

def find_g_x(n,Nerr):
    """Поиск полиномов в библиотеке 
    Вход:
    n - длинна блока
    Nerr - необходимое число исправлений 
    Выход:
    Имя подходящего полинома из библиотеки
    """
    for i in lib_g_x.keys():
        chek = i.split("_")
        if int(chek[0]) == n:
            if int(chek[2]) >= Nerr:
                return i
    
def selection_g_x(p):
    """Функция выбора оптимального полинома
    Вход: 
    p - Вероятность ошибки 
    Выход:
    out - имя кода в библиотеке 
    lib_g_x[out] - определение полинома в 10-тичном формате
    """
    pol = []
    for x in long_array:
        vrem = find_g_x(x,kol_fix_need(x,p))
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
            
    return out,lib_g_x[out]
 
    
    
#функции расчёта искуственной вероятности
