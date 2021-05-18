import numpy as np

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
    