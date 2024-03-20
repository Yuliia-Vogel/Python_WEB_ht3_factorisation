from time import time
import multiprocessing
from multiprocessing import Process
import pprint


def factorize(numbers):
    list_of_factors = [] # оскільки на вхід отримуємо не 1 число, а список чисел, то й повинні скласти список списків дільників/множників, 
                        # тож ініціалізуємо його, цей список списків
    for each in numbers:
        factors = [] # ініціалізуємо список множників для кожного числа
        for i in range(1, each + 1): # перевірка чисел від 1 до його самого включно
            if each % i == 0:  
                factors.append(i) # Якщо на це число ділиться наше без остачі, то аппендимо його до нашого списку "факторз"
        list_of_factors.append(f'assert {each} == {factors}') # всі списки - в один спільний список, який буде результатом
    return list_of_factors # Повертаємо список списків дільників для кожного числа


def cpu_count():
    cpu_on_my_computer = multiprocessing.cpu_count()
    print(f'Here are {cpu_on_my_computer} CPUs on my notebook. \n')
    return int(cpu_on_my_computer)
    


if __name__ == '__main__':
    numbers  = [128, 255, 99999, 10651060, 321123]

    timer = time() # замір часу виконання функції
    result = factorize(numbers) # синхронний запуск функції (в 1 потік)
    pprint.pprint(result) 
    print(f'\nDone by 1 thread: {round(time() - timer, 4)} seconds\n')

    # тепер будемо запускати наприклад паралельні процеси, залежно від того, скільки в нас є ядер на компі:
    cpus = cpu_count()
    step = len(numbers) // cpus
    remnant = len(numbers) % cpus
    print(f'Step is {step}, remnant is {remnant}')

    processes = []
    start_index = 0 # стартовий та кінцевий індекс вводимо, щоб врахувати остачу від ділення ВСІХ елементів списку чисел на вході, при розподіленні між процесами (процесорами)
    for i in range(0, cpus):
        end_index = start_index + step
        if i < remnant:
            end_index += 1  # додаємо одиницю для кожного залишку, щоб ми точно не згубили жодного елемента з остачі від ділення
        processes.append(Process(target=factorize, args=(numbers[start_index:end_index],)))
        start_index = end_index

    print(f"Ready to start {len(processes)} processes at the same time!")    
    timer = time() # замір часу виконання функції тепер в паралельних процесах на всіх ядрах компа
    [process.start() for process in processes]
    [process.join() for process in processes]
    [process.close() for process in processes]
    print(f'Done by {len(processes)} processes: {round(time() - timer, 4)} seconds')