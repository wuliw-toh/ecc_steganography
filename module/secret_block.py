import hashlib
import numpy as np



class rand:
    
    def __init__(self,key):
        """в качестве входного параметра принимает ключ"""
        self.key = key
        self.config()
        
    def config(self):
        """Функция для сброса настроек генератра к исходному состоянию"""
        my_str = hashlib.md5(self.key).hexdigest()
        self.seed_key = int(my_str[:16],16)
        self.nu_key = int(my_str[4:20],16)
        self.a_key =  int(my_str[16:],16)
        
        self.hs_key = my_str
        
        
    def rand(self,size):
        """
        Функция рандом без памяти, тоесть если вы 
        два раза запутите эту функцию получите одинаковые значения
        """
        m = (2**31) - 1
        out = np.zeros(size,float)     
        old_value = self.seed_key
        
        for i in range(size):
            work_value = ((self.a_key*old_value) + self.nu_key) % m
            out[i] = work_value / m
            old_value = work_value  
            
        return out
    
    def rand_with_memory(self,size):
        """Функция очень похожа на rand но она запоминает последнее 
        стотяние и проождает с того же места, тоесть два вызова будут 
        разные последовательности."""
        m = (2**31) - 1
        out = np.zeros(size,float)     
        old_value = self.seed_key
        
        for i in range(size):
            work_value = ((self.a_key*old_value) + self.nu_key) % m
            out[i] = work_value / m
            old_value = work_value  
         
        self.seed_key = old_value
        return out
    
    
    
    
    
class secret_editor:
      
    def __init__(self,key):
        """Принимает секретный ключ в исходной форме.
        Инициализирует два рандомайзера с разными настройками
        """
        self.rand_main = rand(key)
        self.rand_dop = rand(self.rand_main.hs_key.encode())
        
    def gen_mask(self,size,p):
        """Функция для генерация маски
        Вход:
        size - размер маски 
        p - вероятность секретного бита
        Выход:
        out - маска
        """
        noise_arrya = self.rand_main.rand_with_memory(size)
        out = np.zeros(size,int)

        for i in range(size):
            if noise_arrya[i] < p:
                            out[i] = 1
        return out
        
    def mail_to_inside(self,case,mail,mask):
        """
        Вход 
        case - массив контейнера. Длинная склееная в единое целое последовательность
        mail - массив секретного сообщения. Длинная склеенная в единое целое последовательность
        mask - Маска длинной в len(case) содержащая len(mail) единиц
        Выход 
        Массив длинной len(case) с вкраплёнными данными mail

        """
        out = np.zeros(len(case),int)
        mail_num = 0

        for i in range(len(case)):
            if mask[i] == 1:
                out[i] = mail[mail_num]
                mail_num += 1
            else:
                out[i] = case[i]

        return out
    
    def mail_to_outside(case,mask):
        out = []
        for i in range(len(case)):
            if mask[i] == 1:
                out.append(case[i])
        return np.array(out)
        