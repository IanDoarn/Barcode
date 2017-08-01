"""
GS1 Barcode parser

Written by: Ian Doarn
"""
from re import match, search, sub
from datetime import datetime
from collections import OrderedDict
import sys
# TODO: Comment this file!


class GS1:

    def __init__(self, _barcode_n):
        self.gs1 = self.__sterilize_input(_barcode_n)
        self.gtin_number = None
        self.ean_number = None
        self.lot_number = None
        self.expiration_date = None
        self.parse()

    @classmethod
    def __verify_gs1(cls, barcode):
        if match(r'^(01)\d{14}(10\d*|17\d{6})(10\d*|17\d{6})$', barcode):
            return True
        return False

    @staticmethod
    def __sterilize_input(_bcde_n):
        return sub(r'[^\w\d]+', '', _bcde_n)

    @staticmethod
    def __strf_gs1(_bcde_n):
        ean_nbr_m = search('^(01)\d{14}', _bcde_n)
        exp_dte_m = search('(17\d{6})', _bcde_n)
        if match(r'^(01)\d{14}(10\d*)(17\d{6})$', _bcde_n):
            lt_nbr_m = search('(?<=^01\d{14})\d*(?=17\d{6})', _bcde_n)
            return ean_nbr_m.group(0), exp_dte_m.group(0), lt_nbr_m.group(0)
        elif match(r'^(01)\d{14}(17\d{6})(10\d*)$', _bcde_n):
            lt_nbr_m = search('(?<=17\d{6})(10\d*)$', _bcde_n)
            return ean_nbr_m.group(0), exp_dte_m.group(0), lt_nbr_m.group(0)
        else:
            raise ValueError('Could not read GS1 [{}]. Failed to match regex sequence.'.format(_bcde_n))

    def __parse(self, _bcde_n):
        if self.__verify_gs1(_bcde_n):
            _ean_nbr, _exp_dte, _lt_nbr = self.__strf_gs1(_bcde_n)
            self.expiration_date = datetime.strptime('20' + _exp_dte[2:], '%Y%m%d').strftime('%Y-%m-%d')
            self.ean_number = _ean_nbr[0:2]
            self.gtin_number = _ean_nbr[2:16]
            self.lot_number = _lt_nbr[2:]
        else:
            raise ValueError('Invalid GS1 [{}]'.format(self.gs1))

    def parse(self):
        self.__parse(self.gs1)

        data = {'barcode': self.gs1,
                'gtin_number': self.gtin_number,
                'ean_number': self.ean_number,
                'lot_number': self.lot_number,
                'expiration_date': self.expiration_date}

        return OrderedDict(data)


def main(barcode):
    gs1 = GS1(barcode)
    for k, v in gs1.parse().items():
        print('{}: {}'.format(str(k), str(v)))

if __name__ == '__main__':
    usage = "gs1.py GS1 PARSER\n" \
            "\n" \
            "Basic usage:\n" \
            "Parse:   gs1.py [GS1 NUMBER]\n" \
            "Help:    gs1.py -h\n"

    try:
        if len(sys.argv) > 2 and sys.argv[1] in ['-h', '-H']:
            print(usage)
        else:
            main(sys.argv[1])
    except IndexError as error:
        print(usage)
