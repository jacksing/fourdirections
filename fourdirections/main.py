# coding: utf-8

'''A mock game of the flexagon game Dong-Nan-Xi-Bei.'''

import re
import sys
from collections import OrderedDict
import prettytable
from random import sample

from rules import (
    PLAYERS, TIMES_IN_TURN, WINNER_COUNT,
    DIRECTION_A, DIRECTION_B,
    DIRECTION_C, DIRECTION_D
)


def pinfo(info):
    sys.stdout.write('\033[1;32;40m')
    sys.stdout.write(info)
    sys.stdout.write('\033[0m')
    sys.stdout.write('\n')

def pstatus(status):
    sys.stdout.write('\033[1;35;40m')
    sys.stdout.write(status)
    sys.stdout.write('\033[0m')
    sys.stdout.write('\n')

def perror(error):
    sys.stderr.write('\033[1;31;40m')
    sys.stderr.write(error)
    sys.stderr.write('\033[0m')
    sys.stderr.write('\n')


class FourDirections(object):
    all_roles = set(DIRECTION_A + DIRECTION_B + DIRECTION_C + DIRECTION_D)

    def __init__(self):
        self.gamen_status = OrderedDict()

    def next_turn(self, player):
        '''Represents the turn for the player to play.'''
        results = self.gamen_status[player]
        i = 1
        while 1:
            if i > TIMES_IN_TURN:
                break
            sys.stdout.write('%s(第%d次)：' % (player, i))
            selection = sys.stdin.readline().lower()
            if selection.strip() == '?':
                self.print_game()
                continue
            elif not re.match(r'^[ABCD][1-9]$', selection, re.IGNORECASE):
                perror('请输入a/b/c/d开头、1位非零数字结尾的内容，如：a9')
                continue
            if selection[0] == 'a':
                direction = DIRECTION_A
            elif selection[0] == 'b':
                direction = DIRECTION_B
            elif selection[0] == 'c':
                direction = DIRECTION_C
            else:
                direction = DIRECTION_D
            role = sample(direction * int(selection[1]), 1)[0]
            sys.stdout.write('%s抽到了' % player)
            pinfo(role)
            results[role] += 1
            if WINNER_COUNT == results[role]:
                break
            else:
                i += 1

    def is_winner(self, player):
        '''Check whether the player wins or not.'''
        return max(self.gamen_status[player].values()) == WINNER_COUNT

    def get_winner_role(self, player):
        '''Get the role for the winner player.'''
        return [k for k, v in self.gamen_status[player].items() if v == WINNER_COUNT][0]

    def is_gameover(self):
        '''Check whether it is gameover as all player win.'''
        return all(self.is_winner(player) for player in self.gamen_status.keys())

    def print_game(self):
        '''Print out the status of the game'''
        table = prettytable.PrettyTable([''] + list(self.all_roles))
        for player in self.gamen_status:
            row = [player]
            for role in self.all_roles:
                row.append(self.gamen_status[player][role])
            table.add_row(row)
        pstatus(table.__str__())

    def play(self):
        '''Main entrance of the game.'''
        self.gamen_status.clear()
        for player in PLAYERS:
            self.gamen_status[player] = {r: 0 for r in self.all_roles}

        just_began = True
        pinfo('\n====开始====\n')
        while 1:
            if self.is_gameover():
                pinfo('所有人获胜，游戏结束！')
                self.print_game()
                break
            for player in self.gamen_status.keys():
                if self.is_winner(player):
                    continue

                if just_began:
                    just_began = False
                else:
                    pinfo('\n====换人====\n')

                self.next_turn(player)

                if self.is_winner(player):
                    pinfo('%s获胜，成为了%s' % (player, self.get_winner_role(player)))


if __name__ == '__main__':
    FourDirections().play()
