# -*- coding: UTF-8 -*-
import random
import time
import socket

trytimes = 100000
shape = [
    [[0, 0], [1, 0], [2, 0], [3, 0], [1, -1], [1, -2], [1, 1], [1, 2], [3, -1], [3, 1]],
    [[0, 0], [0, -1], [0, -2], [0, -3], [-1, -1], [-2, -1], [1, -1], [2, -1], [-1, -3], [1, -3]],
    [[0, 0], [-1, 0], [-2, 0], [-3, 0], [-1, -1], [-1, -2], [-1, 1], [-1, 2], [-3, -1], [-3, 1]],
    [[0, 0], [0, 1], [0, 2], [0, 3], [-1, 1], [-2, 1], [1, 1], [2, 1], [-1, 3], [1, 3]]
]


class Game:
    def __init__(self):
        self.map = [0] * 10
        self.head = [0] * 4
        self.dir = [0] * 4
        self.gameok = False

        # 尝试增加飞机
        random.seed(time.time())
        for i in range(0, trytimes):
            # 清空map
            for j in range(0, 10):
                self.map[j] = [0] * 10
            # 初始化头部和方向
            self.head = [0] * 4
            self.dir = [0] * 4

            # 并画上去

            for k in range(0, 4):
                self.head[k] = [0] * 2
                self.head[k][0] = random.randint(0, 9)
                self.head[k][1] = random.randint(0, 9)
                self.dir[k] = random.randint(0, 3)
                err = 0
                for dx, dy in shape[self.dir[k]]:
                    nx = self.head[k][0] + dx
                    ny = self.head[k][1] + dy
                    if nx < 0 or ny < 0 or nx > 9 or ny > 9:
                        err = 1
                        break
                    self.map[nx][ny] = 1
                if err == 1:
                    break

            # 完成了一次尝试，下面验证：
            mapsum = 0
            for k in range(0, 10):
                mapsum = mapsum + sum(self.map[k])
            if mapsum == 40:
                print "after %d times try, game initial success!" % i
                self.gameok = True
                return
        print "%d times try over, there is no illegal map.." % trytimes
        return

    def printGame(self, type="white"):
        if not self.gameok:
            print "game is not ok, you cannot print it!"
            return
        print "heads is",
        for i in range(0, 4):
            print "(" + str(self.head[i][0]) + chr(ord('a') + self.head[i][1]) + ")",
        print "\n=========================================="
        if type == "white":
            print "  a b c d e f g h i j"
            for i in range(0, 10):
                print "%d" % (i),
                for j in range(0, 10):
                    print Game.int2Char(self.map[i][j]),
                print ""
        elif type == "color":
            pass
        else:
            print "unknow type"

    @staticmethod
    def int2Char(data):
        if data == 1:
            return '■'
        else:
            return '□'

    def playGame(self):
        if not self.gameok:
            print "game is not ok, you cannot play it!"
            return
        print "game begin!!!(Q to quit)"
        headshot = 0
        st = time.time()
        tmap = [0] * 10
        for i in range(0, 10):
            tmap[i] = [0] * 10

        while True:
            inp = raw_input("what:")

            if inp == "q" or inp == "Q":
                break

            if len(inp) != 2:
                print "input error!(plz input like MN, M=(0~9),N=(a~j)"
                continue
            inp1 = inp[0]
            inp2 = inp[1]
            if inp1 not in "0123456789" or inp2 not in "abcdefghij":
                print "input error!(plz input like MN, M=(0~9),N=(a~j)"
                continue
            x = int(inp1)
            y = ord(inp2) - ord('a')

            print "miss..." if self.map[x][y] == 0 else "bingo!"
            tmap[x][y] = 1
            if [x, y] in self.head:
                print "one plane down!"
                tmap[x][y] = 2
                headshot = headshot + 1
            self.printTemp(tmap)
            if headshot == 4:
                print "你赢了！总耗时: %.2f sec" % (time.time() - st)
                self.printGame()
                break

        print "bye"

    def printTemp(self, data):
        if self.gameok == False:
            print "game is not ok, you cannot print temp"
            return
        print "  a b c d e f g h i j"
        for i in range(0, 10):
            print "%d" % (i),
            for j in range(0, 10):
                if (data[i][j], self.map[i][j]) == (1, 1):
                    print "■", #means body shot
                elif (data[i][j], self.map[i][j]) == (2, 1):
                    print "☻", #means head shot
                elif (data[i][j], self.map[i][j]) == (1, 0):
                    print "□", #means miss
                else:
                    print " ", #means not open
            print ""
