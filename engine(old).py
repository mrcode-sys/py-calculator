operators = ['+','-','x','/']

def calc(num1, ext, num2, percent = False):

  if percent and percent.isnumeric():
    num_list = [num1, num2]
    percent-1
    value1 = num_list[percent]
    value2 = num_list[percent-1]

    num_list[percent] = value2 / 100 * value1

    num1 = num_list[0]
    num2 = num_list[1]

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
    case _:
      return 2, False
    

def resolve_percentage(num1, num2, op):
  match op:
    case "+":
      return num1 + (num2 / 100 * num1)
    case "-":
      return num1 - (num2 / 100 * num1)
    case "x":
      return (num2 / 100) * num1
    case "/":
      return (num2 / num1) * 100
    case _:
      return num2 / 100

def resolve_percentage_index(form, op_location):
  num1 = 100
  num2 = None

  op_idx = op_location - 2
  op = form[op_idx] if op_idx >= 0 else None

  if op_location -1 >= 0 and isinstance(form[op_location - 1], (int, float)):
    num2 = form[op_location - 1]

  if op_location -3 >= 0 and isinstance(form[op_location - 3], (int, float)):
    num1 = form[op_location - 3]

    start_del = op_location - 3
  else:
    start_del = op_location - 1

  if num2 == None:
    return 3, False

  num_percent = resolve_percentage(num1, num2, op)

  del form[start_del:op_location+1]
  form.insert(start_del, num_percent)
  return form

def calc_form(form):
  while "x" in form or "/" in form or "%" in form:
    prioritary_op_idx = [form.index(op) for op in ["x", "/", "%"] if op in form]
    
    if prioritary_op_idx:
      first_op = min(prioritary_op_idx)

      if form[first_op] == "%" or form[first_op+2] == "%":
        if len(form) > first_op + 2 and form[first_op+2] == "%":
          first_op += 2
        form = resolve_percentage_index(form, first_op)
        continue

      num1 = form[first_op-1]
      op = form[first_op]
      num2 = form[first_op+1]
      value, success = calc(num1, op, num2)
      if success == False:
        return value, False

      del form[first_op-1:first_op+2]
      form.insert(first_op-1, value)

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
  print(form)
  if len(form) == 1:
    return form[0], True
  else:
    return 101, False

def resolve_parentheses_form(form):
  while "(" in form and ")" in form:

    internal_end_parenthesis = form.index(")")
    internal_init_parenthesis = len(form) - 1 - form[::-1].index("(", len(form) - internal_end_parenthesis)

    internal_form = form[internal_init_parenthesis+1:internal_end_parenthesis]
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
  print(f"Step 1:\nSuccess: {success}\nValue: {to_list_value}")
  if success == False:
    return f"Err{to_list_value}", True

  resolved_parentheses_value, success = resolve_parentheses_form(to_list_value)
  print(f"Step 2:\nSuccess: {success}\nValue: {resolved_parentheses_value}")
  if success == False:
    return f"Err{resolved_parentheses_value}", True

  final_result, success = calc_form(resolved_parentheses_value)
  print(f"Step 3:\nSuccess: {success}\nValue: {final_result}")
  print(f"Final: {final_result}")
  if success == False:
    return f"Err{final_result}", True
  
  return str(final_result), False