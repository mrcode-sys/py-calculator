operators = ['+','-','x','/']

def calc(num1, ext, num2):
  print(num1)
  print(num2)
  match ext:
    case "x":
      return num1 * num2, True
    case "/":
      if num2 == 0:
        return 1, False 
      return num1 / num2, True
    case "+":
      return num1 + num2, True
    case "-":
      return num1 - num2, True
    case "%":
      pass
    case _:
      return 2, False
    
def calc_form(form):
  while "x" in form or "/" in form:
    div_mult_idx = [form.index(op) for op in ["x", "/"] if op in form]
    
    if div_mult_idx:
      fisrt_op = min(div_mult_idx)
      num1 = form[fisrt_op-1]
      op = form[fisrt_op]
      num2 = form[fisrt_op+1]
      value, success = calc(num1, op, num2)
      if success == False:
        return value, False

      del form[fisrt_op-1:fisrt_op+2]
      form.insert(fisrt_op-1, value)

  while any(op in form for op in operators):

    index = 0
    while index < len(form):
        character = form[index]
        
        if character in operators:
            num1 = form[index - 1]
            op = form[index]
            num2 = form[index + 1]
            value, success = calc(num1, op, num2)
            if not success:
              return value, False
            del form[index-1:index+2]
            form.insert(index - 1, value)
            index = 0 
        else:
            index += 1

  if len(form) == 1:
    return form[0], True
  else:
    return 101, False

def resolve_parentheses_form(form):
  while "(" in form and ")" in form:

    internal_end_parenthesis = form.index(")")
    internal_init_parenthesis = len(form) - 1 - form[::-1].index("(", len(form) - internal_end_parenthesis)

    internal_form = form[internal_init_parenthesis+1:internal_end_parenthesis]
    print(internal_form)
    value, success = calc_form(internal_form)
    if success == False:
      return value, False
    
    del form[internal_init_parenthesis : internal_end_parenthesis + 1]
    form.insert(internal_init_parenthesis, value)

  return form, True

def convert_to_list(string):
  numStr = ""
  form = []

  for character in string + " ":
    print(character)
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
          return 102, False

      numStr = ""
      if character != " ":
        form.append(character)        
  return form, True

def core(string):
  to_list_value, success = convert_to_list(string)
  if success == False:
    return f"Err{to_list_value}", True

  resolved_parentheses_value, success = resolve_parentheses_form(to_list_value)
  if success == False:
    return f"Err{resolved_parentheses_value}", True

  final_result, success = calc_form(resolved_parentheses_value)
  if success == False:
    return f"Err{final_result}", True
  
  return str(final_result), False