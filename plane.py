# -*- coding: UTF-8 -*-
import random
import time
from socket import *
import urllib, urllib2
import random

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
        elif type == "line":
            print self.map
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
                    print "■",  # means body shot
                elif (data[i][j], self.map[i][j]) == (2, 1):
                    print "☻",  # means head shot
                elif (data[i][j], self.map[i][j]) == (1, 0):
                    print "□",  # means miss
                else:
                    print " ",  # means not open
            print ""


# 遍历所有局面:C(100,4)*4^4=3921225*256=10,0383,3600
def genAll():
    for p1 in range(97):
        for p2 in range(p1 + 1, 98):
            for p3 in range(p2 + 1, 99):
                for p4 in range(p3 + 1, 100):
                    # print p1, p2, p3, p4
                    for d1 in range(4):
                        for d2 in range(4):
                            for d3 in range(4):
                                for d4 in range(4):
                                    isOk([p1, p2, p3, p4], [d1, d2, d3, d4])


# 判断一个局面是否合法(合法的只有150456个)
def isOk(p, d):
    map = [0] * 10
    for i in range(10):
        map[i] = [0] * 10

    for i in range(4):
        # 头部坐标
        x = p[i] / 10
        y = p[i] % 10
        dir = d[i]
        for dx, dy in shape[dir]:
            rx = x + dx
            ry = y + dy
            if rx < 0 or rx > 9 or ry < 0 or ry > 9 or map[rx][ry] == 1:
                return p, d, "error"
            else:
                map[rx][ry] = 1
    return p, map


# 根据已有局面从服务端获取机头最大概率点
thre = 0


def getNext(v0, v1, h, step, debug=0):
    # if len(h) == 0 and (len(v0) + len(v1)) == 0:
    #     return "3d"
    # if len(h) == 0 and (len(v0), len(v1)) == (1, 0):
    #     return "2d"
    # if len(h) == 0 and (len(v0), len(v1)) == (0, 1):
    #     return "0c"
    url = "http://localhost/data.php"
    if step < 6:
        url = "http://localhost/data_new.php"
    else:
        url = "http://localhost/data.php"

    try:
        v0_str = ""
        v1_str = ""
        h_str = ""
        for i in v0:
            x = int(i[0])
            y = ord(i[1]) - ord('a')
            v0_str = v0_str + ",d" + str(x * 10 + y)
        for i in v1:
            x = int(i[0])
            y = ord(i[1]) - ord('a')
            v1_str = v1_str + ",d" + str(x * 10 + y)
        for i in h:
            h_str = h_str + "," + str(i)
        if v0_str != "":
            v0_str = v0_str[1:]
        if v1_str != "":
            v1_str = v1_str[1:]
        if h_str != "":
            h_str = h_str[1:]
        bigurl = "%s?v0=%s&v1=%s&h=%s" % (url, v0_str, v1_str, h_str)
        if debug == 1:
            print bigurl + "&debug"
        req = urllib2.Request(url=bigurl)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        return res
    except:
        print "err"
        return None


def getAnser(host='localhost', port=9000, data="test"):
    BUFSIZE = 1024
    udpCliSock = socket(AF_INET, SOCK_DGRAM)
    ADDR = (host, port)

    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)

    tcpCliSock.send(data)
    ret = tcpCliSock.recv(BUFSIZE)
    tcpCliSock.close()
    return ret


# 获取飞机的可能方向，暂时支持一个
def getPossibleDir(v1, h):
    podi = []  # 可能的方向
    pass

#search_server的替代方案，读入内存
class Database:
    def __init__(self):
        fd = open('data0', 'r')
        temp = fd.readlines()
        self.DB = []
        fd.close()
        for i in temp:
            map = i[-200:].replace(" ", "")
            h = i[:-200].split()
            random.seed(time.time())

            self.DB.append([h, map])

    def getRandomGame(self):
        i = random.randint(0, len(self.DB))
        return self.DB[i]

    def searchForNextMove(self, v0, v1, h):
        ok = 0
        tmp = [0] * 100
        for i in self.DB:
            falt = False
            for j in v0:
                if i[1][int(j[0]) * 10 + (ord(j[1]) - ord('a'))] == "1":
                    falt = True
                    break;
                if falt:
                    break;
            if falt:
                continue

            for j in v1:
                if i[1][int(j[0]) * 10 + (ord(j[1]) - ord('a'))] == "0":
                    falt = True
                    break;
                if falt:
                    break;
            if falt:
                continue

            for j in h:
                if h in i[0]:
                    falt = True
                    break
            if falt:
                continue

            ok = ok + 1
            for j in i[0]:
                tmp[int(j)] = tmp[int(j)] + 1
        ret_ind = tmp.index(max(tmp))
        p1 = str(int((ret_ind / 10)))
        p2 = chr(ret_ind % 10 + ord('a'))
        return p1 + p2
