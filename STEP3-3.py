def read_number(line, index):
  number = 0
  #　負の数の時があるから、それは別に処理する
  if line[index][0]=='-':
      token = {'type': 'NUMBER', 'number': int(line[index])}
      return token, index+1
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    decimal = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * decimal
      decimal /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def read_plus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1

def read_minus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1

def read_multi(line, index):
  token = {'type': 'MULTIPLY'}
  return token, index + 1

def read_divide(line, index):
  token = {'type': 'DIVIDE'}
  return token, index + 1

def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = read_number(line, index)
    elif line[index] == '+':
      (token, index) = read_plus(line, index)
    elif line[index] == '-':
      (token, index) = read_minus(line, index)
    elif line[index] == '*':
      (token, index) = read_multi(line, index)
    elif line[index] == '/':
      (token, index) = read_divide(line,  index)
    else:
        #負の数の時があるから、別の処理をする
      if line[index][0] == '-' and line[index][1:].isdigit():
         (token, index) = read_number(line, index)
      else:
        print('Invalid character found: ' + line[index])
        exit(1)
    tokens.append(token)
  return tokens


def evaluate(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'MULTIPLY':
        tokens[index-2]['number'] =  tokens[index-2]['number'] * tokens[index]['number']
        tokens.pop(index-1)
        tokens.pop(index-1)
        index = index - 2
      if tokens[index - 1]['type'] == 'DIVIDE':
        tokens[index-2]['number'] =  tokens[index-2]['number'] / tokens[index]['number']
        tokens.pop(index-1)
        tokens.pop(index-1)
        index = index - 2
    index  +=1

  index = 1

  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer


def test(line):
  tokens = tokenize(line)
  actual_answer = evaluate(tokens)
  expected_answer = eval(line)
  if abs(actual_answer - expected_answer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expected_answer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

def solver(line):
    n = len(line)
    L = [] # 新しい文字列
    kakko = [] # Lのなかの (の位置を表す
    for i in range(n):
        if line[i]=='(':
            #(かっこを見つけたらLのなかの何番目かをkakkoというリストに入れとく
            kakko.append(len(L))
        elif line[i] == ')':
            #)かっこを見つけたらkakkoリストの最後から)の間を計算して、
            # ()の中身を計算結果と置き換えてLに追加する
            left = kakko.pop(-1) # kakkoの最後を取り出す&kakkoから削除
            inp = L[left:] #()の中身になる部分
            tokens = tokenize(inp)
            ans = evaluate(tokens) #計算結果
            L = L[:left] #(から後ろを削除
            L.append(str(ans)) #計算結果ansを代わりに入れる
        else:
            L.append(line[i]) #(でも)でもないときは普通に追加
    #Lはかっこがない文字列になっているから、最後に計算する
    tokens = tokenize(L)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))

# Add more tests to this function :)
def run_test():
  print("==== Test started! ====")
  solver("(1+11+(3+5*4+(3+4))*3)/(1+4)*(4+4)")
  solver("(1+11+(3+5*4+(3+4))*3)/(1+4)")
  solver("(1+11+(3+5*4+(-1))*3)/(1+4)")
  solver("(1+11+(3+5*4+(3-4))*3)/(1+4)*(4+4)")
  solver("(1+11+(3+5*4+(3-4))*3)/(1+4)*(4+4)/33*93+(55-(84-87+(44-11)*4))/43+(45)")
  print("==== Test finished! ====\n")
run_test()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)
