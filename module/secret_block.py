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
    
    def mail_to_outside(self,case,mask):
        """Извлекает сообщение по маске
        Вход:
        case - сообщение из линии связи
        mask - маска на основе секретного ключа 
        Выход:
        out - закодированное секретное послание 
        """
        out = []
        for i in range(len(case)):
            if mask[i] == 1:
                out.append(case[i])
        return np.array(out)
    
    def gen_mark_sequence_bin(self,size):
        """Простой генератор марковской цепи
        Матрица переходов = |0.5, 0.5|
                            |0.5, 0.5|
        """
        out = np.zeros(size,int)
        rand_seq = self.rand_dop.rand_with_memory(size)
        #первый элемент 
        if rand_seq[0] < 0.5:
            out[0] = 0
        else:
            out[0] = 1
            
        for i in range(1,size):
            if rand_seq[i] > 0.5:
                if out[i-1] == 0:
                    out[i] = 1
                else:
                    out[i] = 0         
            else:
                out[i] = out[i-1]


        return np.array(out)
        
        
    def merge_sequences(self,case,mail,ps):
        """Основная функия встраивания сообщения 
        Вход:
        case - длинная последовательность закодированного контейнера 
        mail - длинная последовательнсоть закодированного сообщения
        ps - вероятность искуственной ошибки
        Выход:
        to_link - Длинная последовательность для линии передачи 
        """
        mask_work = self.gen_mask(len(case),ps)
        dop_noise = self.gen_mark_sequence_bin(sum(mask_work) - len(mail))
        long_mail = np.concatenate((mail,dop_noise),0)
        return self.mail_to_inside(case,long_mail,mask_work)
    
    
    def separation_sequences(self,case,ps):
        """Основная функция извлечения информации из последовательности
        Вход:
        case - последовательность полученная из линии связи 
        ps - вероятность искуственной ошибки 
        Выход:
        out - закодированное секретное сообщение 
        """
        mask_work = self.gen_mask(len(case),ps)
        return self.mail_to_outside(case,mask_work)
        
        
        