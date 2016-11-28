# -*- coding: utf-8 -*-

import itertools
import sys
from reward import rewards


class MGPLotto(object):
    table = None
    expected = None

    def __init__(self):
        self.table = []
        self.expected = []
        self.main()

    def get_input(self):
        self.table = []
        for i in xrange(3):
            text = raw_input(
                '{}번째 줄을 입력하세요 (모르는 칸은 0으로): '.format(i + 1))
            # apply input constraints
            if not text.isdigit() or len(text) != 3:
                sys.exit('종료합니다.')
            row = [int(t) for t in text]
            self.table += row

    def expect(self):
        self.expected = [0] * 8
        pool = [x for x in xrange(1, 10) if x not in self.table]
        pos = [i for i, v in enumerate(self.table) if v == 0]

        iterator = itertools.permutations(pool)
        count = 1
        try:
            while True:
                shuffled_pool = next(iterator)
                table = self.table[:]
                for i, v in enumerate(pos):
                    table[v] = shuffled_pool[i]
                self.add_value(table)
                count += 1
        except StopIteration:
            pass
        finally:
            del iterator

        result = [v / count for v in self.expected]
        self.show_result(result)

    def add_value(self, table):
        # 4 5 6 7 8
        # 3 x x x
        # 2 x x x
        # 1 x x x
        self.expected[0] += rewards[table[6] + table[7] + table[8]]
        self.expected[1] += rewards[table[3] + table[4] + table[5]]
        self.expected[2] += rewards[table[0] + table[1] + table[2]]
        self.expected[3] += rewards[table[0] + table[4] + table[8]]
        self.expected[4] += rewards[table[0] + table[3] + table[6]]
        self.expected[5] += rewards[table[1] + table[4] + table[7]]
        self.expected[6] += rewards[table[2] + table[5] + table[8]]
        self.expected[7] += rewards[table[2] + table[4] + table[6]]

    @staticmethod
    def show_result(result):
        best_choice = result.index(max(result))
        print '......'
        print '[{}번]이 최고의 선택입니다! (기대값: {})'\
            .format(best_choice + 1, result[best_choice])
        print '  4 5 6 7 8'
        print '  3 x x x'
        print '  2 x x x '
        print '  1 x x x '
        print result
        print '-' * 60

    def main(self):
        while True:
            self.get_input()
            self.expect()


if __name__ == '__main__':
    MGPLotto()
