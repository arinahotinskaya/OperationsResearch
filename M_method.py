from sympy import *
import numpy as np

M = symbols('M', real=True, positive=True)
np.set_printoptions(precision=3)

def negativity_check(x, b, signs):
  for i in range(len(signs)):
    if signs[i] == '=' and b[i] < 0:
      b[i] *= -1
      for j in range(len(x[i])):
        x[i][j] *= -1
    elif signs[i] == '>=' and b[i] < 0:
      b[i] *= -1
      signs[i] = '<='
      for j in range(len(x[i])):
        x[i][j] *= -1
    elif signs[i] == '<=' and b[i] < 0:
      b[i] *= -1
      signs[i] = '>='
      for j in range(len(x[i])):
        x[i][j] *= -1
  return x, b, signs


# Приведение к каноническому виду
def canonization(extr, C, x, signs, b):
  x_i = len(x[0]) # Длина строки х (до добавления искуственных переменных)
  Ri, Si, RS = [], [], []
  basis = []

  for i, el in enumerate(signs):
    if el=='>=':
      Si.append(i), RS.append(i)
    if el=='=' or el=='>=':
      Ri.append(i)
    if el=='<=':
      Si.append(i)

  if len(Si) != 0:
    S = []
    for i in Si:
      box = [0] * len(b)
      for j in range(len(b)):
        if j == i:
          box[j] = 1.0
      for k in RS:
        for j in range(len(b)):
          if j == k:
            box[j] *= -1.0
      S.append(box)
    x = np.hstack((x, np.transpose(S)))

  if len(Ri) != 0:
    R = []
    for i in Ri:
      box = [0] * len(b)
      for j in range(len(b)):
        if j == i:
          box[j] = 1.0
      R.append(box)
    x = np.hstack((x, np.transpose(R)))

  for i in range(len(Si)):
    C = np.append(C, 0)

  for i in range(len(Ri)):
    if extr=='max':
      C = np.append(C, -M)
    elif extr=='min':
      C = np.append(C, M)
  C = np.append(C, 0)

  # print(f'\nТаблица с искуственными переменными:\n{C}\n{x}')

  for i in range(len(x)):
    for j in range(x_i, len(x[i])):
      if x[i][j] == 1:
        basis.append(j)
  for i in range(len(signs)):
    signs[i] = '='
  return C, x, basis, Ri, signs


# Нахождение решающих столбца, строки и элемента
def find_decisive(extr, delta, b, x, basis):
  for i in range(len(delta)):
    if hasattr(delta[i], 'evalf') == true:
      delta[i] = delta[i].evalf(subs={M: 1e10})

  col_decisive = 0 # Нахождение решающего столбца
  if extr == 'max':
    min_value = min(delta[0:-2])
    col_decisive = delta[0:-2].index(min_value)
  elif extr == 'min':
    max_value = max(delta[0:-2])
    col_decisive = delta[0:-2].index(max_value)

  box_col = []
  for i in range(len(b)):
    if x[i][col_decisive] > 0:
      box_col.append(x[i][col_decisive])
    else:
      box_col.append(-1)

  count = 0 # Расмотр варианта, когда решения не существует
  for el in box_col:
    if el < 0:
      count += 1
  if count == len(box_col):
    return col_decisive, -1, -1, -1

  Q = []  # Cимплекс-отношения Q
  row_decisive = 0  # Нахождение решающей строки
  minimum = 1e5
  for i in range(len(b)):
    if x[i][col_decisive] > 0:
      Q.append(b[i] / x[i][col_decisive])
    else:
      Q.append(-1)
  for i in range(len(Q)):
    if 0 <= Q[i] < minimum:
      minimum = Q[i]
      row_decisive = i

  el_decisive = x[row_decisive][col_decisive] # Нахождение решающего элемента
  basis[row_decisive] = col_decisive # Обновление базиса
  return row_decisive, col_decisive, el_decisive, basis


# Метод Гаусса-Жордана
def Gauss_Jordan(x, b, el, row, col):
  for i in range(len(x[row])): # Делим решающую строку на решающий элемент
    x[row][i] /= el
  b[row] /= el

  box_col = []
  for i in range(len(x)):
    box_col.append(x[i][col])

  for i in range(len(x)): # Из оставшихся строк вычитаем решающую строку, умноженную на соотвествующий элемент в столбце решающем
    for j in range(len(x[0])):
      if i != row:
        x[i][j] -= box_col[i] * x[row][j]

  for i in range(len(x)):
    if i != row:
      b[i] -= box_col[i] * b[row]
  return x, b


# Проверка на оптимальность
def optimality(extr, delta):
  for i in range(len(delta)):
    if hasattr(delta[i], 'evalf') == true:
      delta[i] = delta[i].evalf(subs={M: 1e10})

  for i, el in enumerate(delta[0:-2]):
    if extr == 'max' and el < 0:
      return True
    elif extr == 'min' and delta[i] > 0:
      return True
  return False


# Вычисление дельта
def calculate_delta(C, x, b, basis):
  delta = []
  for i in range(len(x[0])):
    expression = 0
    for j in range(len(x)):
      expression += C[basis[j]] * x[j][i]
    delta.append(expression - C[i])
  expression = 0
  for j in range(len(basis)):
    expression += C[basis[j]] * b[j]
  delta.append(expression - C[-1])
  return delta


def simplex_method(extr, C, x, signs, b):
  x, b, signs = negativity_check(x, b, signs)

  # print('\n')
  # for i in range(len(b)):
  #   print(f'{x[i]} {signs[i]} {b[i]}')

  C, x, basis, R, signs = canonization(extr, C, x, signs, b) # Канонизация
  delta = calculate_delta(C, x, b, basis) # Вычисление новых дельт
  # print(f'\nСимплекс-таблица с дельтами:\n{C}\n{x}\n{delta}')
  basis_copy = basis.copy()

  current_x = np.zeros(len(x[0]))
  k = 0
  for i in basis:
    current_x[i] += b[k]
    k += 1
  del k
  # print(f'X: {current_x}\nF: {delta[-1]}') # Вывод текущего плана и целевой функции

  flag = optimality(extr, delta) # Проверка на оптимальность
  # if not flag:
  #   print("План оптимален")
  # else:
  #   print("План не оптимален")

  count = 1 # Счетчик итераций
  while True:
    # print(f'\n\t\033[1mИтерация\033[0m {count}')

    row, col, el, basis = find_decisive(extr, delta, b, x, basis) # Нахождение решающих значений
    if basis == -1:
      # print('\033[1mФункция не ограничена. Оптимальное решение отсутсвует\033[0m')
      return -1, -1, -1, -1, -1, -1
    # print(f'Решающий столбец:{col} \nРешающая строка:{row} \nРешающий элемент:{x[row][col]} \nНовый базис(ном.столбцов):{basis}')

    x, b = Gauss_Jordan(x, b, el, row, col)
    delta = calculate_delta(C, x, b, basis)
    # print(f'\nСимплекс-таблица с обновленными дельтами:\n{C}\n{x}\n{delta}')

    current_x = np.zeros(len(x[0])) # Вывод текущего плана Х, и целевой функции F
    k = 0
    for i in basis:
      current_x[i] += b[k]
      k += 1
    del k
    # print(f'X: {current_x}\nF: {delta[-1]}')

    flag_iter = optimality(extr, delta)
    if not flag_iter:
      # print('План оптимален\n')
      mark = 0
      for i in range(len(basis)):
        for j in R:
          if i == j:
            if basis[i] == basis_copy[i]:
              # print('\033[1mТак как в оптимальном решении присутствуют искусственные переменные, то задача не имеет допустимого решения\033[0m')
              mark = 1
              return -1, -1, -1, -1, -1, -1
      # if mark == 0:
        # print(f'\033[1mОтвет \n\tx: {current_x}\n\tF_{extr}: {delta[-1]}\033[0m')
      return x, signs, b, delta[-1], delta, basis

    # else:
    #   print('План не оптимален')
    count += 1
