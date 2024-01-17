import numpy as np

def find_F(x, C_copy):
  res = 0
  for i in range(len(C_copy)):
    res += x[i] * C_copy[i]
  return res


def dual_negativity_check(x, b, signs):
  for i in range(len(signs)):
    if signs[i] == '>=':
      b[i] *= -1
      signs[i] = '<='
      for j in range(len(x[i])):
        x[i][j] *= -1
  return x, b, signs


# Приведение к каноническому виду
def dual_canonization(C, x, signs, b):
  x_i = len(x[0]) # Длина строки х (до добавления искуственных переменных)
  Si = []
  basis = []

  for i, el in enumerate(signs):
    if el=='<=':
      Si.append(i)

  if len(Si) != 0:
    S = []
    for i in Si:
      box = [0] * len(b)
      for j in range(len(b)):
        if j == i:
          box[j] = 1.0
      S.append(box)
    x = np.hstack((x, np.transpose(S)))

  for i in range(len(Si)):
    C = np.insert(C, -2, 0)

  print(f'\nТаблица с искуственными переменными:\n{C}\n{x}')

  for i in range(len(x)):
    for j in range(x_i, len(x[i])):
      if x[i][j] == 1:
        basis.append(j)
  return C, x


# Нахождение решающих столбца, строки и элемента
def dual_find_decisive(delta, b, x, basis):
  # print(f'delta={delta},{len(delta)}\nx={x},{len(x)}\nb={b},{len(b)}\nbasis={basis},{len(basis)}')
  row_decisive = 0  # Нахождение решающей строки
  maximum = -1e3
  for i in range(len(b)):
    if b[i] <= 0 and abs(b[i]) >= maximum:
      row_decisive = i
      maximum = abs(b[i])
  col_decisive = 0 # Нахождение решающего столбца
  box_col = []
  minimum = 1e3
  for i in range(len(x[0])):
    print(f'delta[i] = {delta[i]}, x[row_decisive][i] = {x[row_decisive][i]}')
    if delta[i] <= 0 and x[row_decisive][i] < 0:
      if delta[i]/x[row_decisive][i] <= minimum:
        minimum = delta[i]/x[row_decisive][i]
        box_col.append(delta[i]/x[row_decisive][i])
        col_decisive = i
    else:
      box_col.append(-1)
  count = 0 # Расмотр варианта, когда решения не существует
  for el in box_col:
    if el == -1:
      count += 1
  if count == len(box_col):
    return col_decisive, -1, -1, -1

  el_decisive = x[row_decisive][col_decisive] # Нахождение решающего элемента
  basis[row_decisive] = col_decisive # Обновление базиса
  return row_decisive, col_decisive, el_decisive, basis


# Метод Гаусса-Жордана
def dual_Gauss_Jordan(delta, x, b, el, row, col):
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

  box_delta = delta[col]
  for j in range(len(x[0])):
    delta[j] -= box_delta * x[row][j]
  # delta[-1] -= box_delta * b[row]

  for i in range(len(x)):
    if i != row:
      b[i] -= box_col[i] * b[row]

  return x, b, delta


# Проверка на оптимальность
def dual_optimality(delta):
  return np.all(delta >= 0)


def dual_simplex_method(C, x, signs, b, basis, C_copy):
  print("\nДВОЙСТВЕННЫЙ СИМПЛЕКС-МЕТОД")
  x, b, signs = dual_negativity_check(x, b, signs)

  for i in range(len(b)):
    print(f'{x[i]} {signs[i]} {b[i]}')

  delta = C
  print(f'\nСимплекс-таблица с дельтами:\n{x}\n{delta}')

  current_x = np.zeros(len(x[0]))
  k = 0
  for i in basis:
    current_x[i] += b[k]
    k += 1
  del k
  print(f'X: {current_x}\nF: {delta[-1]}') # Вывод текущего плана и целевой функции
  delta = delta[:-1]

  count = 1 # Счетчик итераций
  while not dual_optimality(b):
    print(f'\n\t\033[1mДВОЙСТВЕННЫЙ Итерация\033[0m {count}')

    row, col, el, basis = dual_find_decisive(delta, b, x, basis) # Нахождение решающих значений
    if basis == -1:
      print('\033[1mФункция не ограничена. Оптимальное решение отсутсвует\033[0m')
      return -1, -1, -1, -1, -1, -1
    print(f'Решающий столбец:{col} \nРешающая строка:{row} \nРешающий элемент:{x[row][col]} \nНовый базис(ном.столбцов):{basis}')

    x, b, delta = dual_Gauss_Jordan(delta, x, b, el, row, col)
    print(f'\nСимплекс-таблица с обновленными дельтами:\n{x}\n{delta}')

    current_x = np.zeros(len(x[0])) # Вывод текущего плана Х, и целевой функции F
    k = 0
    for i in basis:
      current_x[i] += b[k]
      k += 1
    del k
    print(f'X: {current_x}\nF: {find_F(current_x, C_copy)}')
    count += 1
  delta = np.append(delta, find_F(current_x, C_copy))
  return x, signs, b, delta, delta, basis


def check_int(x): # Проверка на целочисленность
  if abs(x - round(x, 0)) < 1e-6:
    return True
  else:
    return False


def fractional_decomposition(num): # Разложение нецелочисленных переменных на целую и дробную части
  if check_int(num):
    fraction = 0
    # print(f'INT {num}: whole = {int(num)}, fraction = {fraction}')
  else:
    whole = np.floor(num)
    fraction = num - whole
    # print(f'NOTINT {num}: whole = {whole}, fraction = {fraction}')
  return fraction


def canonization(x, b, z, add_x, add_b, basis, signs):
  print(f'\n{z}\n{x}\nБазис: {basis}')
  x_len = len(add_x) # Длина строки х (до добавления искуственных переменных)
  flag = False
  k = -1
  for i, el in enumerate(z):
    if el > 1e3:
      flag = True
      k = i

  if flag:
    add_x[k] = 1
    for i in range(len(b)):
      x[i][k] = 0
    x = np.vstack((x, add_x))
    b = np.append(b, add_b)
    z[k] = 0
    basis.append(x_len - 1)
    signs = np.append(signs, '=')
  else:
    add_x = np.append(add_x, 1)
    x = np.hstack((x, np.zeros((len(x), 1))))
    print(f'x = {x} _______ add_x = {add_x}')
    x = np.vstack((x, add_x))
    b = np.append(b, add_b)
    z = np.append(z, 0)
    basis.append(x_len)
    signs = np.append(signs, '=')

  print(f'\nТаблица с искуственными переменными:\n{z}\n{x}\nОбновленный базис: {basis}')
  return z, x, b, basis, signs


# Определяем функцию для поиска оптимального решения методом Гомори
def gomory_method(extr, F, C, x, b, x_integer, basis, signs, C_copy):
  # Вывод полученного оптимального плана
  print('\n' + '-' * 100)
  for i in range(len(x)):
    print(x[i])
  x_opt = [0] * len(C)
  k = 0
  for i in basis:
    x_opt[i] += b[k]
    k += 1
  del k
  print(f'Оптимальный план можно записать так:\n x = {x_opt}\n F = {F}')

  if all(check_int(x_opt[i]) for i in x_integer): # Проверяем целочисленность переменных
    print(f'План оптимален и допустим:\n x = {x_opt}\n F = {F}')
    return 0
  else:
    print('\nМЕТОД ГОМОРИ')
    count = 1
    while count != 100:
      print(f'\n\t\033[1mГОМОРИ Итерация\033[0m {count}')

      box = [] # Находим нецелочисленную переменную с наибольшим дробным значением
      for i in x_integer:
        if not check_int(x_opt[i]):
          box.append(i)
      # if not box:
      #   if not check_int(C[-1]):
      #     box.append(-1)
      print(box)

      maximum = 0
      for j in box:
        if j != -1:
          if abs(x_opt[j]) >= 1:
            if abs(x_opt[j]) - abs(np.trunc(x_opt[j])) > abs(x_opt[maximum]) - abs(np.trunc(x_opt[maximum])):
              print(f'{j}: {x_opt[j]} = {abs(x_opt[j]) - abs(np.trunc(x_opt[j]))}')
              maximum = j
          elif 0 < abs(x_opt[j]) < 1:
            if abs(x_opt[j]) > abs(x_opt[maximum]) - abs(np.trunc(x_opt[maximum])):
              maximum = j
              print(f'{j}: {x_opt[j]} = {x_opt[j]}')
        # elif j == -1:
        #   if abs(C[-1]) >= 1:
        #     maximum = -1

      # Добавляем ограничение для переменной
      add_x = np.array([])
      add_b = 0
      # if maximum == -1:
      #   add_b = fractional_decomposition(C[-1]) * -1
      #   for i in range(len(x[j])):
      #     add_x = np.append(add_x, fractional_decomposition(C[i]) * -1)
      # else:
      for j, el in enumerate(basis):
        if el == maximum:
          add_b = fractional_decomposition(b[j]) * -1
          for i in range(len(x[j])):
            add_x = np.append(add_x, fractional_decomposition(x[j][i]) * -1)
      print(f'Производящая строка для построения отсечения: {add_x} <= {add_b}')

      z, x, b, basis, signs = canonization(x, b, C[:-1], add_x, add_b, basis, signs)
      z = np.append(z, C[-1])

      print(z)
      if extr == 'max' and count == 1:
        for i in range(len(z)):
          z[i] *= -1
      print(z)

      current_x = np.zeros(len(x[0]))
      k = 0
      for i in basis:
        current_x[i] += b[k]
        k += 1
      del k
      print(f'X: {current_x}\nF: {z[-1]}')  # Вывод текущего плана и целевой функции

      # Решаем задачу линейного программирования для нового ограничения
      x, signs, b, F, C, basis = dual_simplex_method(z, x, signs, b, basis, C_copy)
      if basis == -1:
        return -1

      x_opt = [0] * len(C)
      k = 0
      for i in basis:
        x_opt[i] += b[k]
        k += 1
      del k

      # Проверяем целочисленность решения
      if all(check_int(x_opt[i]) for i in x_integer):
        print(f'План оптимален и допустим:\n x = {x_opt}\n F = {C[-1]}')
        return 0

      count += 1
