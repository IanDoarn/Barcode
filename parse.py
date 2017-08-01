from hibc import HIBC
from gs1 import GS1
import re
import sys
import pprint


def main(barcode):
    _bcde_n = re.sub(r'[^A-Za-z0-9]+', '', barcode)
    if re.match(r'^(01)[0-9]{14}(10[0-9]*|17[0-9]{6})(10[0-9]*|17[0-9]{6})$', _bcde_n):
        _gs1 = GS1(_bcde_n)
        return _gs1.parse()
    if re.match(r'(^[+])\w(\d{3})([\w\d]*)/(\d{6})(\d*)([\w\d_+$\-.\s%]*)$', barcode):
        _hibc = HIBC(barcode)
        return _hibc.parse()
    else:
        raise ValueError('Unable to parse barcode [{}]'.format(_bcde_n))


if __name__ == '__main__':
    usage = "parse.py Barcode Parser\n" \
            "\n" \
            "Basic usage:\n" \
            "Parse:   parse.py [BARCODE NUMBER]\n" \
            "Help:    parse.py -h\n"
    try:
        if len(sys.argv) > 2 and sys.argv[1] in ['-h', '-H']:
            print(usage)
        else:
            pprint.pprint(main(sys.argv[1]))
    except IndexError as error:
        print(usage)
