import numpy as np
import simplex_method as sm


class Node:
  def __init__(self, level, value, bounds, C, x, signs, b, x_opt):
    self.level = level  # уровень узла в дереве
    self.value = value  # значение узла
    self.bounds = bounds  # значение функции F
    self.C = C
    self.x = x
    self.signs = signs
    self.b = b
    self.x_opt = x_opt


def check_int(x): # Проверка на целочисленность
  if abs(x - round(x, 0)) < 1e-6:
    return True
  else:
    return False


def calculate_first_bound(extr):
  if extr == 'max':
    bound = -1e10
  elif extr == 'min':
    bound = 1e10
  return bound


def branch_and_bound(extr, F, C, x, b, x_integer, basis, signs, C_copy, x_copy, b_copy):
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
    print('\nМЕТОД ВЕТВЕЙ И ГРАНИЦ')
    MAX_LEVEL = 50  # максимальный уровень дерева
    nodeList = []  # список узлов дерева решений
    bound = calculate_first_bound(extr)
    x_res = []

    element = 0
    for i in x_integer:
      if not check_int(x_opt[i]):
        element = i
        break

    root_node = Node(level=0, value=np.copy(x_opt[element]), bounds=np.copy(C[-1]), C=np.copy(C_copy), x=np.copy(x_copy), signs=np.copy(signs), b=np.copy(b_copy), x_opt=np.copy(x_opt))
    print(f'ROOT {root_node.level}: level={root_node.level}, value={root_node.value}, bound={root_node.bounds}, C={root_node.C}, x={root_node.x}, signs={root_node.signs}, b={root_node.b}, x_opt={root_node.x_opt}')
    nodeList.append(root_node)

    while nodeList:
      current_node = nodeList.pop(0)  # извлекаем первый узел из списка

      if extr == 'max':
        if current_node.bounds > bound and all(check_int(current_node.x_opt[i]) for i in x_integer):
          bound = current_node.bounds
          x_res = current_node.x_opt
        elif not all(check_int(current_node.x_opt[i]) for i in x_integer) and current_node.level < MAX_LEVEL:
          left_node = create_left_node(current_node, extr, x_integer)
          right_node = create_right_node(current_node, extr, x_integer)
          if left_node != -1:
            if left_node.bounds > bound:  # проверка верхней границы
              nodeList.append(left_node)  # добавляем в список узлов
          if right_node != -1:
            if right_node.bounds > bound:  # проверка верхней границы
              nodeList.append(right_node)  # добавляем в список узлов

      elif extr == 'min':
        if current_node.bounds < bound and all(check_int(current_node.x_opt[i]) for i in x_integer):
          bound = current_node.bounds
          x_res = current_node.x_opt
        elif not all(check_int(current_node.x_opt[i]) for i in x_integer) and current_node.level < MAX_LEVEL:
          left_node = create_left_node(current_node, extr, x_integer)
          right_node = create_right_node(current_node, extr, x_integer)
          if left_node != -1:
            if left_node.bounds < bound:  # проверка верхней границы
              nodeList.append(left_node)  # добавляем в список узлов
          if right_node != -1:
            if right_node.bounds < bound:  # проверка верхней границы
              nodeList.append(right_node)  # добавляем в список узлов

      print(f'NODELIST = {nodeList},  LEN = {len(nodeList)}')
      print(f'BOUND = {bound},  X_RES = {x_res}')

    if not x_res:
      print('\nРешение не найдено!')
      return 0
    else:
      print(f'\n\nРезультат: bound = {bound}, x_res = {x_res}, x_int = {x_integer}')
      if all(check_int(x_res[i]) for i in x_integer):
        print(f'План оптимален и допустим:\n x = {x_res}\n F = {bound}')
        return 0


def create_left_node(current_node, extr, x_integer):
  left_level = current_node.level + 1
  left_value = np.floor(current_node.value)

  C, x, signs, b = np.copy(current_node.C), np.copy(current_node.x), np.copy(current_node.signs), np.copy(current_node.b)

  box_x = np.array([])
  for i, el in enumerate(current_node.x_opt):
    if i < len(current_node.C):
      if el == current_node.value:
        box_x = np.append(box_x, 1)
      else:
        box_x = np.append(box_x, 0)
  x = np.vstack((x, box_x))
  del box_x

  signs = np.append(signs, '<=')
  b = np.append(b, left_value)
  left_node = Node(level=left_level, value=0, bounds=0, C=np.copy(C), x=np.copy(x), signs=np.copy(signs), b=np.copy(b), x_opt=0)
  x, _, b, F, C, basis = sm.simplex_method(extr, C, x, signs, b)
  if basis == -1:
    return -1

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

  if all(check_int(x_opt[i]) for i in x_integer):
    left_value = None
  elif not all(check_int(x_opt[i]) for i in x_integer):
    element = 0
    for i in x_integer:
      if not check_int(x_opt[i]):
        element = i
        break
    left_value = x_opt[element]

  left_node.value, left_node.bounds, left_node.x_opt = left_value, C[-1], x_opt
  print(f'LEFT LEVEL {left_level}: level={left_node.level}, value={left_node.value}, bound={left_node.bounds}, C={left_node.C}, x={left_node.x}, signs={left_node.signs}, b={left_node.b}, x_opt={left_node.x_opt}')
  return left_node


def create_right_node(current_node, extr, x_integer):
  right_level = current_node.level + 1
  right_value = np.ceil(current_node.value)

  C, x, signs, b = np.copy(current_node.C), np.copy(current_node.x), np.copy(current_node.signs), np.copy(current_node.b)

  box_x = np.array([])
  for i, el in enumerate(current_node.x_opt):
    if i < len(current_node.C):
      if el == current_node.value:
        box_x = np.append(box_x, 1)
      else:
        box_x = np.append(box_x, 0)
  x = np.vstack((x, box_x))
  del box_x

  signs = np.append(signs, '>=')
  b = np.append(b, right_value)
  right_node = Node(level=right_level, value=0, bounds=0, C=np.copy(C), x=np.copy(x), signs=np.copy(signs), b=np.copy(b), x_opt=0)
  x, _, b, F, C, basis = sm.simplex_method(extr, C, x, signs, b)
  if basis == -1:
    return -1

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

  if all(check_int(x_opt[i]) for i in x_integer):
    right_value = None
  elif not all(check_int(x_opt[i]) for i in x_integer):
    element = 0
    for i in x_integer:
      if not check_int(x_opt[i]):
        element = i
        break
    right_value = x_opt[element]

  right_node.value, right_node.bounds, right_node.x_opt = right_value, C[-1], x_opt
  print(f'RIGHT LEVEL {right_level}: level={right_node.level}, value={right_node.value}, bound={right_node.bounds}, C={right_node.C}, x={right_node.x}, signs={right_node.signs}, b={right_node.b}, x_opt={right_node.x_opt}')
  return right_node
