import numpy as np
from ecc_editor import *

def noise_in_treak(case,pe):
    """Шум в линии передачи
    Вход:
    case - передоваемая последовательность
    pe - вероятность ошибки 
    Выход
    out - длинная последоваетльность с вкраплёнными ошибками
    ВАЖНО! данная функция использует np.random 
    """
    out = case.copy()
    err_mas = np.random.random(len(case))
    for i in range(len(case)):
        if err_mas[i] < pe:
            if out[i] == 1:
                out[i] = 0
            else:
                out[i] = 1
    return out
    
    
class decod_atacl(ecc_strem):
    def decoding_work(self,mas_in):
        mas_1 = []
        mas_2 = []
        
        for x in mas_in:
            pol,kol_err = self.decoding_blok(x)
            mas_1.append(pol)
            mas_2.append(kol_err)
            
        return np.array(mas_1),np.array(mas_2)
    
       
    def decoding_blok(self,value):
        n = 0
        work_p = polinom(value,self.n_cod)
        ost = work_p % self.g_x
        
        if sum(ost.main_mas) != 0:       
            while self.t_cod < sum(ost.main_mas):
                n += 1
                work_p = work_p << 1
                ost = work_p % self.g_x
                
                if n > self.n_cod: 
                    break
                
            work_p = work_p + ost
            work_p = work_p >> n
             
        long_pol = work_p / self.g_x
        return polinom(long_pol.main_mas[(self.n_cod - self.k_cod):],self.k_cod).main_mas , sum(ost.main_mas)
    
    def chek_error_blok(self,value):
        n = 0
        work_p = polinom(value,self.n_cod)
        ost = work_p % self.g_x
        
        if sum(ost.main_mas) != 0:       
            while self.t_cod < sum(ost.main_mas):
                n += 1
                work_p = work_p << 1
                ost = work_p % self.g_x
                
                if n > self.n_cod: 
                    break
                
            ost = ost >> n
            work_p = work_p >> n
             
        out = []
        for i in range(len(work_p.main_mas)):
            if ost.main_mas[i] == 1:
                out.append(work_p.main_mas[i])
        return out
    
    def chek_err_work(self,mas_in):
        return [self.chek_error_blok(x) for x in mas_in]
 

    
#Пара временных функция для тестов статистики     
def stat_test(mas):
    print("M   => ",np.mean(mas))
    print("D   => ",np.var(mas))
    print("Med => ",np.median(mas))
    print("std => ",np.std(mas))
    
    print(end="|")
    for i in range(1,10):
        print(str(i*10)+"% =",np.percentile(mas,i*10),end="|")
    print()

    
def test_bin(from_link):
    print("Стат параметры")
    print("Вероятность встретить 0 => ",sum(from_link == 0) / len(from_link))
    print("Вероятность встретить 1 => ",sum(from_link == 1) / len(from_link))

    X1 = from_link == 1
    X2 = from_link == 0

    print("Вероятности переходов")
    print("1 to 1 => ",sum(X1[:-1]&X1[1:]) / sum(X1))
    print("1 to 0 => ",sum(X1[:-1]&X2[1:]) / sum(X1))

    print("0 to 0 => ",sum(X2[:-1]&X2[1:]) / sum(X2))
    print("0 to 1 => ",sum(X2[:-1]&X1[1:]) / sum(X2))

    
    
def auto_kor_for_step(value,step=1):
    if step == 0 :
        out = 1
    else:
        out = np.corrcoef(value[:-step],value[step:])[0][1]
    return out

def auto_kor(value,delta_max = 10):
    return np.array([auto_kor_for_step(value,x) for x in range(delta_max)])