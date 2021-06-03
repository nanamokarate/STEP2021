from collections import deque

def main():
  pages = {}
  links = {}

  with open('data/pages.txt') as f:
    for data in f.read().splitlines():
      page = data.split('\t')
      # page[0]: id, page[1]: title
      pages[page[0]] = page[1]

  with open('data/links.txt') as f:
    for data in f.read().splitlines():
      link = data.split('\t')
      # link[0]: id (from), links[1]: id (to)
      if link[0] in links:
        links[link[0]].add(link[1])
      else:
        links[link[0]] = {link[1]}

#ここから自分のプログラム

  for k, v in pages.items():
    if v == 'Google':
      start = k
    if v == '渋谷':
      goal = k

  BFS(links, start, goal, pages)#幅優先探索
  
  

##幅優先探索を用いる
##queue=[〇〇：{〇〇のlink先},〇〇のlink先のある要素△△：{△△のlink先}…]という形にする
##ループを防ぐために一度確認したものをprevに入れておく
def BFS(links, start, goal, pages):
  path = {}#経路を入れていく
  queue = deque()
  queue.append(start)
  before_checked = set()#一回でも調べたもの
  before_checked.add(start)
  a = 0
  while len(queue) != 0:
    b=0
    now = queue.popleft()
    if now == goal:
      a=1
      break
    if now in links:
      for link in links[now]:
        if link not in before_checked:
          queue.append(link)
          before_checked.add(link)
          if b == 0:
            path[now] = {link}
            b +=1
          else:#すでにpath内にnowのリンクの要素が１つでも入っている時は追加するだけ
            path[now].add(link)
  if a == 1:#経路が見つかった場合
    return(path_print(start, goal, path, pages))
  if a == 0:
    print('経路なし')
    return False

##pathを受け取って、goalの'渋谷'を要素に持つkがあれば今度はそのkをgoalとしstartのGoogleに辿り着くまで繰り返す
##startからgoalの最短経路をgoalから遡って表示
##goalから辿っていって,最終的にstartが表示できればfinishを表示して終了する
def path_print(start, goal, path, pages):
  print(goal,pages[goal])
  while True:
    for k in path:
      if goal in path[k]:
        if k == start:
          print(start,pages[start])
          return 'finish'
        else:
          print(k,pages[k])
          goal=k


if __name__ == '__main__':
  main()