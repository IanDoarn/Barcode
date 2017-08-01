"""
Prototype class object for
other barcode types used in the environment

Written by: Ian Doarn
"""
# TODO: Comment this file!


class Barcode(object):

    def __init__(self, barcode):
        self.__barcode = barcode
        self.barcode, self.type = self.__parse(barcode)

    @staticmethod
    def __parse(_bcde_n):
        if _bcde_n[0:2].upper() != 'ZI':
            t = _bcde_n.split('-')[0]
            if t.upper() == 'Z':
                return t[1], 'Kit'
            if t.upper() == 'X':
                return t[1], 'Transfer'
            if t.upper() == 'ORD':
                return t[1], 'Order'
            if t.upper() == 'V':
                return t[1], 'Vehicle'
            if t.upper() == 'BIN':
                return t[1], 'Bin'
            if t.upper() == 'CASE':
                return t[1], 'Case'
        else:
            return _bcde_n[2:], 'Z-Tag'

    def __repr__(self):
        return self.__barcode

    def __str__(self):
        return self.type + " " + self.barcode

if __name__ == '__main__':
    i = input('Scan barcode: ')
    b = Barcode(i)
    print(repr(b), str(b))
