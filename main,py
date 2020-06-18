# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 15:23:04 2019

@author: Isaac
"""

import random
from itertools import combinations
import copy
import time
import numpy as np

class MineGround:
    bomb = -1
    def MakeGround(self, size, bombnum):
        '''
        size 크기의 배열을 만든 후,
        랜덤으로 지정한 개수의 폭탄을 심는다.
        이후 배열을 반환한다.
        '''
        ground = [[0 for _ in range(size[1])] for _ in range(size[0])]
        all_indexs = []
        for i in range(size[0]):
            for j in range(size[1]):
                all_indexs.append([i,j])
        
        indexs = random.choices(all_indexs, k = bombnum)
        for i, j in indexs:
            ground[i][j] = self.bomb
        
        for i, j in all_indexs:
            if ground[i][j]!=self.bomb:
                ground[i][j] = self.getAroundBombNum(ground, (i,j))
        return ground, indexs
    
    def getWays8(self, pos, xmax, ymax):
        '''
        주어진 좌표의 주변 8방향 좌표 배열을 반환한다.
        '''
        ways8 = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if self.is_in(pos[0] + i, pos[1] + j,xmax,ymax):
                    ways8.append([pos[0] + i, pos[1] + j])
        ways8.remove(list(pos))
        return ways8
    
    def getAroundBombNum(self, ground, pos):
        '''
        주어진 좌표의 주변에 있는 폭탄의 개수를 반환한다.
        '''
        result = 0
        xmax = len(ground)
        ymax = len(ground[0])
        
        ways8 = self.getWays8(pos, xmax, ymax)
        
        for i,j in ways8:
            if ground[i][j]==self.bomb:
                result += 1
        return result
    
    def printGround(self, innground):
        '''
        게임 판을 출력한다.
        '''
        print()
        maxlen = -1
        ground = copy.deepcopy(innground)
        for i in range(len(ground)):
            for j in range(len(ground[0])):
                ground[i][j] = str(ground[i][j])
                maxlen = max(maxlen, len(ground[i][j]))
        
        for i in ground:
            for j in i:
                    print(j ,end=' ' + ' '*(maxlen-len(j)))
            print()
        print()
    
    def is_in(self, x,y,xmax,ymax):
        '''
        입력된 좌표 x,y 가 주어진 범위를 만족하는지 검사한다.
        '''
        return 0<=x and x<xmax and 0<=y and y<ymax
    
    def getEmptyTable(self, size):
        '''
        0으로 초기화 된 2차원 배열을 반환한다.
        '''
        return [[0 for _ in range(size[1])] for _ in range(size[0])]


class MineSweeper(MineGround):
    def __init__(self, bombrate, size):
        self.bombrate = bombrate
        self.size = size
        self.bombnum = int(size[0]*size[1]*bombrate)
    
        self.ground, self.bombs = self.MakeGround(size, self.bombnum)
        self.mask = self.getEmptyTable(size)
        self.game = self.getEmptyTable(size)
        self.done = False
        self.playerwin = False
        self.updateGame()
        
    def check(self, pos):
        '''
        주어진 좌표를 확인한다.
        폭탄이면 게임종료. 아니면 숨어있던 숫자가 보인다.
        '''
        pos = list(pos)
        x,y = pos
        self.mask[x][y] = 1
        if self.ground[x][y]==self.bomb:
            self.done = True
            return
        
        elif self.ground[x][y]!=0:
            self.mask[x][y] = 1
        
        else:
            indexs = []
            self.getAllBlockPos(self.ground, pos, 0, indexs)
            for poss in indexs:
                ways = self.getWays8(poss, len(self.ground), len(self.ground[0]))
                for i,j in ways:
                    self.mask[i][j] = 1
        
        if self.checkWin():
            self.done = True
            self.playerwin = True
        
        self.updateGame()
    
    def updateGame(self):
        '''
        게임 판을 업데이트 한다.
        '''
        for i in range(len(self.ground)):
            for j in range(len(self.ground[0])):
                if self.mask[i][j]==1:
                    self.game[i][j] = str(self.ground[i][j])
                    
                elif self.mask[i][j]==0:
                    self.game[i][j] = "-"
                else:
                    self.game[i][j] = "b"

    
    def flag(self, pos):
        '''
        주어진 좌표에 폭탄 표시를 한다.
        '''
        x,y = pos
        if self.mask[x][y]==0:
            self.mask[x][y] = -1
        self.updateGame()
    
            
    def getAllBlockPos(self, ground, pos, value, array):
        '''
        주어진 좌표와 연결되어 있으며 주어진 좌표와 같은 값을 가지는
        좌표 덩어리들을 구한다.
        '''
        pos = list(pos)
        x,y = pos
        
        if ground[x][y]!=value:
            return 
        elif pos in array:
            return 
        else:
            array.append(pos)
        
        ways = self.getWays8(pos, len(ground), len(ground[0]))
        for i,j in ways:
            self.getAllBlockPos(ground, (i,j), value, array)
    
    def printgame(self):
        '''
        게임을 출력한다.
        '''
        self.updateGame()
        if self.done:
            if not self.playerwin:
                print("Game Over!")
            else:
                print("You Win!")
            self.printGround(self.game)
        else:
            self.printGround(self.game)
    
    def checkWin(self):
        '''
        승부를 체크한다.
        '''
        for i in range(len(self.ground)):
            for j in range(len(self.ground[0])):
                if [i,j] in self.bombs:
                    if self.mask[i][j]==1:
                        return False
                else:
                    if self.mask[i][j]!=1:
                        return False
        return True

class MineSweeperAI(MineGround):
    block = "-"
    flag = "b"
    bomb = "-1"
    
    def main(self, table):
        if self.isNoZero(table):
            return [], [self.getRandomBlock(table)]
        
        b, nb, p = self.findBombs(table)
        xlen = len(table)
        ylen = len(table[0])
        
        if b==[] and nb==[]:
            print("check all cases")
            #주변에 폭탄이 남아있는 숫자블록 리스트(poslist)를 구한다.
            poslist = []
            for i in range(xlen):
                for j in range(ylen):
                    if self.isNaturalNum(table[i][j]):
                        flags, blocks, bombnum = self.getFlagBlockNum(table, [i,j])
                        if bombnum - len(flags) > 0:
                            poslist.append([i,j])

            #좌표들을 인접한 것 끼리 묶는다.
            clusters = self.makeClusters(poslist)
            
            #모든 경우의 수를 계산한다.
            
            result = np.asarray(self.getEmptyTable((len(table), len(table[0]))), dtype=np.float32)
            resultmask = np.asarray(self.getEmptyTable((len(table), len(table[0]))), dtype=np.int32)

            for cluster in clusters:
                counttable, casenum, mask = self.resultAllCase(table, cluster)
                counttable = np.asarray(counttable, dtype=np.float32)
                if casenum==0: 
                    continue
                counttable = counttable/casenum
                result += counttable
                
                resultmask += np.asarray(mask, dtype=np.int32)

            #반올림 및 다른 상관없는 칸들은 블락처리
            result = result.tolist()
            resultmask = resultmask.tolist()
            for i in range(xlen):
                for j in range(ylen):
                    if resultmask[i][j] != 1:
                        result[i][j] = self.block
                    else:
                        result[i][j] = round(result[i][j], 1)
            
            
            #무조건 폭탄인경우, 아닌경우 체크하기
            bomb, nbomb = [],[]
            for i in range(xlen):
                for j in range(ylen):
                    if result[i][j]!=self.block:
                        if result[i][j] == 1.0:
                            bomb.append((i,j))
                        elif result[i][j] == 0.0:
                            nbomb.append((i,j))
            
            if len(bomb) > 0 or len(nbomb) > 0:
                return bomb, nbomb
            #찍어야 하는 경우
            else:
                minval = 100
                maxval = -1
                
                minpos, maxpos = (), ()
                
                for i in range(xlen):
                    for j in range(ylen):
                        if result[i][j]==self.block:
                            continue
                        
                        if result[i][j] < minval:
                            minval = result[i][j]
                            minpos = (i,j)
                        
                        if result[i][j] > maxval:
                            maxval = result[i][j]
                            maxpos = (i,j)
                
                return [], [minpos]
#                if (1-minval) > maxval:
#                    return [], [minpos]
#                else:
#                    return [maxpos], []
                    
        else:
            return b, nb
    
    def makeClusters(self, poslist):
        '''
        좌표들의 리스트를 입력받아 서로 인접한 좌표끼리 묶는다.
        '''
        result = []
        #모든 주변좌표가 추가된 클러스터
        cluster = []
        #주변 좌표를 추가해야 하는 클러스터
        semicluster = [tuple(poslist.pop())]
        #새롭게 추가된 좌표 클러스터
        newcluster = []
        
        while poslist:
            
            for mpos in semicluster:
                i = 0
                while i<len(poslist):
                    pos = poslist[i]
                    if self.isNear(mpos, pos):
                        newcluster.append(tuple(pos))
                        del poslist[i]
                    else:
                        i += 1
            
            cluster += semicluster
            semicluster = []
            
            if len(newcluster)>0:
                semicluster += newcluster
                
                newcluster = []
                
            else:
                result.append(copy.deepcopy(cluster))
                cluster = []
                semicluster = [tuple(poslist.pop())]
                newcluster = []
        
        cluster += semicluster
        semicluster = []
        
        if len(cluster)>0:
            result.append(cluster)
        
        return result
    
    def isNear(self, pos1, pos2):
        '''
        두 좌표를 입력받아 거리가 두 칸 이내인지 검사한다.
        '''
        x1, y1 = pos1
        x2, y2 = pos2
        return abs(x1-x2) <= 2 and abs(y1-y2) <= 2
    
    def resultAllCase(self, inputtable, poslist):
        
        table = copy.deepcopy(inputtable)
        xlen = len(table)
        ylen = len(table[0])
        mask = self.getEmptyTable((len(inputtable), len(inputtable[0])))
        
        for i in range(xlen):
            for j in range(ylen):
                if table[i][j] == self.flag:
                    ways = self.getWays8((i,j), xlen, ylen)
                    for wx, wy in ways:
                        if self.isNaturalNum(table[wx][wy]) or\
                            table[wx][wy] == 0 or table[wx][wy] == '0':
                            table[wx][wy] = int(table[wx][wy])-1
                            table[wx][wy] = str(table[wx][wy])
        
        
        counttable = [[0 for _ in range(ylen)] for _ in range(xlen)]
        result = []
        self.checkAllCase(poslist, 0, table, result, mask)
        for casetable in result:
            for i in range(xlen):
                for j in range(ylen):
                    if casetable[i][j]==self.flag and table[i][j]==self.block:
                        counttable[i][j] += 1
        return counttable, len(result), mask
    
    def checkAllCase(self, poslist, index, table, result, mask):
        '''
        모든 경우의 수를 계산하는 함수
        '''
        xlen = len(table)
        ylen = len(table[0])
        
        if len(poslist) <= index:
            result.append(table)
            return
        
        flags, blocks, bombnum = self.getFlagBlockNum(table, poslist[index])
        
        for bx, by in blocks:
            mask[bx][by] = 1
        
        leftnum = bombnum
        #폭탄이 없는 경우
        if leftnum==0:
            self.checkAllCase(poslist, index+1, table, result, mask)
        #폭탄이 남아있는 경우
        elif leftnum > 0:
            for poses in combinations(blocks, leftnum):
                
                isWrong = False
                new_table = copy.deepcopy(table)
                for i,j in poses:
                    new_table[i][j] = self.flag
                    ways = self.getWays8((i,j), xlen, ylen)
                    for wx, wy in ways:
                        if self.isNaturalNum(new_table[wx][wy]) or\
                            new_table[wx][wy] == 0 or new_table[wx][wy] == '0':
                            new_table[wx][wy] = int(new_table[wx][wy])-1
                            
                            if new_table[wx][wy] < 0:
                                isWrong = True
                                break
                            
                            new_table[wx][wy] = str(new_table[wx][wy])
                            
                    if isWrong:
                        break
                            
                if isWrong:
                    continue
                else:
                    self.checkAllCase(poslist, index+1, new_table, result, mask)
        else:
            print("error")
    
    
    
    def findBombs(self, table):
        xlen = len(table)
        ylen = len(table[0])
        points = []
        for i in range(xlen):
            for j in range(ylen):
                if self.isNaturalNum(table[i][j]):
                    points.append([i,j])
        
        bombs = []
        notbombs = []
        probs = [[0 for _ in range(len(table[0]))] for _ in range(len(table))]

        for i, j in points:
            flags, blocks, bombnum = self.getFlagBlockNum(table, [i,j])
            
            if bombnum == len(blocks) + len(flags):
                bombs += blocks
            elif bombnum == len(flags):
                notbombs += blocks
            elif bombnum < len(flags):
                assert False, "error"
            
            elif bombnum > len(flags):
                prob = (bombnum - len(flags))/len(blocks)
                for bx, by in blocks:
                    probs[bx][by] += prob
                
        
        bombs = list(set([tuple(i) for i in bombs]))
        notbombs = list(set([tuple(i) for i in notbombs]))
        return bombs, notbombs, probs
    
    def isNoZero(self, table):
        for i in range(len(table)):
            for j in range(len(table[0])):
                try:
                    if int(table[i][j])==0:
                        return False
                except:
                    pass
        return True
    
    def getRandomBlock(self, table):
        poses = []
        for i in range(len(table)):
            for j in range(len(table[0])):
                if table[i][j]==self.block:
                    poses.append([i,j])
        
        return random.choice(poses)

        
    def getFlagBlockNum(self, table, pos):
        x,y = pos
        bombnum = int(table[x][y])
        ways = self.getWays8(pos, len(table), len(table[0]))
        
        flags = []
        blocks = []
        for i,j in ways:
            if table[i][j]==self.flag:
                flags.append([i,j])
            elif table[i][j]==self.block:
                blocks.append([i,j])
        
        return flags, blocks, bombnum
    
    def isNaturalNum(self, num):
        result = False
        try:
            num = int(num)
            if num >= 1:
                result = True
        except:
            pass
        return result
        
if __name__=='__main__':
    
    ai = MineSweeperAI()
    
    winrate = []
    for _ in range(50):
        mg = MineSweeper(0.1, (30,30))
        while not mg.done:
            b, nb = ai.main(mg.game)
            for pos in b:
                mg.flag(pos)
            for pos in nb:
                mg.check(pos)
        winrate.append(mg.playerwin)

    print("accuracy : {}".format(sum(winrate)/len(winrate)))
    
    
