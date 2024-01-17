import numpy as np
import simplex_method as sm
import gomori as gomori
import branchbound

if __name__ == '__main__':
  # вариант 1
  # C = np.array([2, -5, 2, -1, -1], dtype=float)
  # x = np.array([[1, -14, 2, -1, -1], [10, -6, 9, -5, -2], [1, 3, 19, -10, -5]], dtype=float)
  # signs = np.array(['=', '=', '='])
  # b = np.array([9, 2, 4], dtype=float)
  # x_integer = np.array([0, 1, 2]) # a
  # x_integer = np.array([0, 2]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 2
  C = np.array([8, -2, 4, -7, 4], dtype=float)
  x = np.array([[4, -7, 6, 5, -2], [9, 2, -9, 3, 9], [-1, 5, 2, -4, 5]], dtype=float)
  signs = np.array(['<=', '>=', '<='])
  b = np.array([9, 6, 6], dtype=float)
  x_integer = np.array([0, 2, 4]) # вариант а
  x_integer = np.array([1, 2, 3]) # вариант б
  # x_integer = np.array([0, 1, 2, 3, 4]) # когда все целочисленные переменные

  # вариант 3
  # C = np.array([1, -8, 5, -4, 0], dtype=float)
  # x = np.array([[5, -7, 5, 6, 9], [0, 6, 0, 8, -9], [0, 4, 3, -9, 2]], dtype=float)
  # signs = np.array(['<=', '>=', '<='])
  # b = np.array([1, 6, 1], dtype=float)
  # x_integer = np.array([1, 3, 4]) # a
  # x_integer = np.array([0, 1, 4]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 4
  # C = np.array([3, -1, 4, -6, 4], dtype=float)
  # x = np.array([[2, -5, 7, 0, 0], [1, 0, -8, 7, 2], [-9, 0, 7, 6, -3]], dtype=float)
  # signs = np.array(['=', '=', '='])
  # b = np.array([8, 1, 9], dtype=float)
  # x_integer = np.array([0, 2, 3]) # a
  # x_integer = np.array([2, 3]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 5
  # C = np.array([2, -1, 6, -9, 3], dtype=float)
  # x = np.array([[0, 5, -7, 5, 0], [5, 2, 4, -6, 4], [4, -8, 4, 3, 0]], dtype=float)
  # signs = np.array(['=', '=', '='])
  # b = np.array([4, 2, 3], dtype=float)
  # x_integer = np.array([2, 3]) # a
  # x_integer = np.array([1, 4]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 6
  # C = np.array([-1, 7, -3, 5, 9], dtype=float)
  # x = np.array([[8, -3, 0, 1, 0], [0, 0, 1, 6, -6], [5, -1, 8, -1, 2]], dtype=float)
  # signs = np.array(['=', '=', '='])
  # b = np.array([2, 9, 8], dtype=float)
  # x_integer = np.array([0, 4]) # a
  # x_integer = np.array([1, 3]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 7
  # C = np.array([6, 0, -6, 4, 9], dtype=float)
  # x = np.array([[1, 4, 0, 2, -4], [1, 2, -1, 0, 1], [1, -8, 6, 0, 6]], dtype=float)
  # signs = np.array(['<=', '>=', '<='])
  # b = np.array([3, 1, 4], dtype=float)
  # x_integer = np.array([0, 2, 3]) # a
  # x_integer = np.array([1, 2, 4]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 8
  # C = np.array([9, -8, 8, -9, -3], dtype=float)
  # x = np.array([[-5, 5, 7, 3, 8], [5, 3, -8, 3, 4], [1, 4, 2, -3, -4]], dtype=float)
  # signs = np.array(['<=', '=', '<='])
  # b = np.array([1, 6, 8], dtype=float)
  # x_integer = np.array([1, 3, 4]) # a
  # x_integer = np.array([0, 2, 4]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 9
  # C = np.array([-7, 0, 5, 2, -9], dtype=float)
  # x = np.array([[1, 9, 0, -7, 1], [3, -8, 4, 2, 4], [-8, 5, 1, 2, -6]], dtype=float)
  # signs = np.array(['<=', '=', '<='])
  # b = np.array([8, 7, 7], dtype=float)
  # x_integer = np.array([0, 3, 4]) # a
  # x_integer = np.array([1, 2, 4]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 10
  # C = np.array([4, 4, 0, -5, 5], dtype=float)
  # x = np.array([[1, 1, 8, 6, 6], [-3, 7, 2, 1, -8], [4, 8, -4, 2, 2]], dtype=float)
  # signs = np.array(['<=', '<=', '<='])
  # b = np.array([4, 1, 1], dtype=float)
  # x_integer = np.array([1, 2]) # a
  # x_integer = np.array([0, 3]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 11
  # C = np.array([7, -5, 0, 0, 4], dtype=float)
  # x = np.array([[-7, -7, 4, 2, 9], [5, 6, 2, -7, 5], [4, 1, 8, 3, -7]], dtype=float)
  # signs = np.array(['=', '=', '='])
  # b = np.array([8, 8, 7], dtype=float)
  # x_integer = np.array([2, 3, 4]) # a
  # x_integer = np.array([2, 4]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 12
  # C = np.array([2, 3, -6, -4, -2], dtype=float)
  # x = np.array([[0, 2, -9, 9, 4], [0, 3, 4, 5, -3], [3, -3, 4, -3, 6]], dtype=float)
  # signs = np.array(['=', '=', '='])
  # b = np.array([1, 9, 7], dtype=float)
  # x_integer = np.array([0, 1]) # a
  # x_integer = np.array([3, 4]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 13
  # C = np.array([3, -9, 2, 8, -9], dtype=float)
  # x = np.array([[2, 4, -5, 5, 9], [-4, 6, 6, 1, -3], [9, -8, 4, 4, 3]], dtype=float)
  # signs = np.array(['<=', '>=', '<='])
  # b = np.array([9, 7, 6], dtype=float)
  # x_integer = np.array([0, 2, 3]) # a
  # x_integer = np.array([1, 2, 4]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 14
  # C = np.array([0, 5, 5, -6, 2], dtype=float)
  # x = np.array([[2, -5, 9, 1, 7], [2, 8, 1, -4, 0], [0, -5, 0, 9, -3]], dtype=float)
  # signs = np.array(['<=', '>=', '<='])
  # b = np.array([8, 9, 2], dtype=float)
  # x_integer = np.array([2, 3, 4]) # a
  # x_integer = np.array([0, 1, 2]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 15
  # C = np.array([0, -2, -2, 1, 4], dtype=float)
  # x = np.array([[3, -2, 9, 9, -7], [8, 3, -3, 0, 3], [1, 6, 3, 6, -5]], dtype=float)
  # signs = np.array(['<=', '>=', '<='])
  # b = np.array([1, 3, 9], dtype=float)
  # x_integer = np.array([0, 3, 4]) # a
  # x_integer = np.array([1, 2, 3]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 16
  # C = np.array([2, -8, -1, -3, 2], dtype=float)
  # x = np.array([[-9, 4, 8, -3, 2], [7, 7, -4, 1, 5], [-8, 2, 0, 4, 0]], dtype=float)
  # signs = np.array(['<=', '=', '<='])
  # b = np.array([8, 7, 1], dtype=float)
  # x_integer = np.array([2, 3, 4]) # a
  # x_integer = np.array([0, 1, 3]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # вариант 17
  # C = np.array([1, -7, -5, 4, 0], dtype=float)
  # x = np.array([[3, -7, 3, 0, 5], [2, 1, -5, 8, 2], [-5, 0, 2, -3, 4]], dtype=float)
  # signs = np.array(['<=', '=', '<='])
  # b = np.array([4, 3, 3], dtype=float)
  # x_integer = np.array([1, 2, 3]) # a
  # x_integer = np.array([0, 3, 4]) # b
  # x_integer = np.array([0, 1, 2, 3, 4]) # all

  # Таха метод отсечений
  # C = np.array([7, 10], dtype=float)
  # x = np.array([[-1, 3], [7, 1]], dtype=float)
  # signs = np.array(['<=', '<='])
  # b = np.array([6, 35], dtype=float)
  # x_integer = np.array([0, 1])

  # Таха метод ветвей
  # C = np.array([5, 4], dtype=float)
  # x = np.array([[1, 1], [10, 6]], dtype=float)
  # signs = np.array(['<=', '<='])
  # b = np.array([5, 45], dtype=float)
  # x_integer = np.array([0, 1])

  # https://www.matburo.ru/mart_sub.php?p=art_lp_215
  # C = np.array([4, 5, 6], dtype=float)
  # x = np.array([[1, 2, 3], [4, 3, 2], [3, 1, 1]], dtype=float)
  # signs = np.array(['<=', '<=', '<='])
  # b = np.array([35, 45, 40], dtype=float)
  # x_integer = np.array([0, 1, 2])

  # https://moluch.ru/archive/116/31884/
  # C = np.array([27, 21], dtype=float)
  # x = np.array([[2, 1], [5, 4]], dtype=float)
  # signs = np.array(['<=', '<='])
  # b = np.array([9, 29], dtype=float)
  # x_integer = np.array([0, 1])

  C_copy = np.copy(C)
  x_copy = np.copy(x)
  signs_copy = np.copy(signs)
  b_copy = np.copy(b)

  # ВЫЗОВ СИМПЛЕКС-МЕТОДА
  extr = int(input('\nЧто нужно найти: \n\t1.min \n\t2.max \nВведите номер варианта: '))
  if extr == 1:
    extr = 'min'
    x, signs, b, F, C, basis = sm.simplex_method(extr, C, x, signs, b)
  elif extr == 2:
    extr = 'max'
    x, signs, b, F, C, basis = sm.simplex_method(extr, C, x, signs, b)
  else:
    print('Неверный тип задачи!')
    exit()

  if basis == -1:
    print('\nМетод Гомори или метод ветвей и границ не могут быть применимы, так как у задач нет решения')
    exit()

  # ВЫЗОВ МЕТОДА ГОМОРИ
  # gomori.gomory_method(extr, F, C, x, b, x_integer, basis, signs, C_copy)

  # ВЫЗОВ МЕТОДА ВЕТВЕЙ И ГРАНИЦ
  branchbound.branch_and_bound(extr, F, C, x, b, x_integer, basis, signs_copy, C_copy, x_copy, b_copy)
