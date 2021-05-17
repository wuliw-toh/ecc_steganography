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