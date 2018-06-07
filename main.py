# -*- coding: UTF-8 -*-
import plane as pl
import time


def main():
    game = pl.Game()
    game.printGame("line")
    # game.playGame()


def main2():
    pl.genAll()


def main3():
    print pl.getPdf(["3d", "4g", "3g", "6j", "7j", "7f", "9g"],
                    ["3h", "0h", "2g", "3c", "2b", "1c", "7g", "5g"],
                    [23, 28, 63])


def solve(number, debug=1):
    # db = pl.Database()
    h = []
    v0 = []
    v1 = []
    moves = ""
    heads = ""
    while len(h) < 4:
        # # 确定下一步之前，对已有头部做一个预判
        # if len(h) > 0:
        #     pl.getPossibleDir(v1, h)
        #     pass

        # 确定下一步
        # st = time.time()
        nextmove = pl.getNext(v0, v1, h, len(moves) / 2, debug)
        moves = moves + nextmove
        # print "getPdf() time cost %.2f" % (time.time() - st)
        # print nextmove
        # print h, v0, v1
        # 根据返回值确定放那个里面
        # st = time.time()
        ret = pl.getAnser(data=nextmove + "," + str(number))
        # print "getAnser() time cost %.2f" % (time.time() - st)
        if ret == "0":
            v0.append(nextmove)
        if ret == "1":
            v1.append(nextmove)
        if ret == "2":
            x = int(nextmove[0])
            y = ord(nextmove[1]) - ord('a')
            h.append(x * 10 + y)
    ##print "head is",
    tmp = []  # head sort
    for i in h:
        tmp.append(str(i / 10) + chr(i % 10 + ord('a')))
    tmp.sort()
    for i in tmp:
        heads = heads + i
    print ("%s,%d,%s") % (heads, len(moves) / 2, moves)
    return len(moves) / 2


def main4():
    print "<" + pl.getAnser("localhost", 9000, "8c") + ">"


def main5():
    db = pl.Database()
    print len(db.DB)
    # print db.DB[3]
    print db.getRandomGame()
    print db.searchForNextMove(["3d"], [], [])


if __name__ == "__main__":
    st = time.time()
    sum = 0
    # for i in range(100):
    #    sum = solve(i) + sum
    print solve(6, debug=1)
    et = time.time()
    print sum
    print "time cost %.2f" % (et - st)
