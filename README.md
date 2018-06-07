猜飞机游戏简介
----
随机生成如下图的四架飞机，通过尝试猜测的方式确定4个飞机头部就算赢。

```
  a b c d e f g h i j
0 □ ■ □ □ □ ■ ■ ■ □ □
1 □ ■ □ ■ □ □ ■ □ □ □
2 ■ ■ ■ ■ ■ ■ ■ ■ ■ □
3 □ ■ □ ■ □ □ ■ □ □ □
4 □ ■ □ □ □ □ □ □ □ □
5 □ ■ ■ ■ □ □ □ ■ □ □
6 □ □ ■ □ □ ■ □ ■ □ □
7 ■ ■ ■ ■ ■ ■ ■ ■ ■ □
8 □ □ ■ □ □ ■ □ ■ □ □
9 □ □ □ □ □ □ □ ■ □ □
```

玩法1-随机生成题目玩
----

```
import plane as pl
game=pl.Game()
#game.printGame('line')
game.playGame()

```

玩法2-批量求解
----
. 搭好php，建表table.sql,录入数据allgames.tar.gz
. 生成题目(1000data)，开启verify server:./srv.py 1000data
```
solve(N)
```