operators_prec = {
    '+': 1,
    '-': 1,
    'x': 2,
    '/': 2,
    '%': 3
}

def apply_op(op, b, a=None):
    match op:
        case '+': return a + b, True
        case '-': return a - b, True
        case 'x': return a * b, True
        case '/': 
            if b == 0: return 1, False
            return a / b, True
        case '%':
            if a is not None:
                return a * (b / 100), True
            return b / 100, True
        case _:
            return 2, False

def to_rpn(eq):
  output = []
  stack = []

  # 5+((1+2) x 4) - 3
  # 5 1 2 + 4 x + 3 -


  # 5 + 5 + 10 - 2
  # 5, 5, '+', 10, '+', 2, '-'

  for char in eq:
    if isinstance(char, (int, float)):
      output.append(char)
    elif char in operators_prec:
      while (
        stack and
        operators_prec.get(stack[-1], 0) >= operators_prec[char] and
        stack[-1] != '('
        ):
        
        output.append(stack.pop())

      stack.append(char)
    
    elif char == '(':
      stack.append(char)
    elif char == ')':
      while stack and stack[-1] != '(':
        output.append(stack.pop())
      if not stack:
        return None, False
      stack.pop()

  while stack:
    op = stack.pop()
    if op in ('(', ')'):
      return None, False
    output.append(op)
  return output, True

def resolve_rpn(rpn_list):
  val_stack = []
  
  for char in rpn_list:
    if isinstance(char, (int, float)):
      val_stack.append(char)
    elif char in operators_prec:
        if char == '%':
          if not val_stack:
            return 101, False
          b = val_stack.pop()
          a = val_stack[-1] if val_stack else None
          res, ok = apply_op('%', b, a)
          if not ok: return res, False
          val_stack.append(res)
        else:
          if len(val_stack) < 2:
            return 101, False
          b = val_stack.pop()
          a = val_stack.pop()
          res, ok = apply_op(char, b, a)
          if not ok: return res, False
          val_stack.append(res)

  if len(val_stack) == 1:
    return val_stack[0], True
  return 101, False

def to_list(string):
  numStr = ""
  form = []

  for character in string + " ":
    if character.isnumeric() or character == ".":
      numStr += character
    else:
      if numStr:
        try:
          if "." in numStr:
            form.append(float(numStr))
          else:
            form.append(int(numStr))
        except ValueError:
          return 201, False

      numStr = ""
      if character != " ":
        form.append(character)        
  return form, True

def core(string):
  eq, ok = to_list(string)
  if not ok:
    return f"Err{eq}", True

  rpn_list, ok = to_rpn(eq)
  if not ok:
    return f"Err{rpn_list}", True

  solved_rpn, ok = resolve_rpn(rpn_list)
  if not ok:
    return f"Err{solved_rpn}", True
  else:
    return solved_rpn, False