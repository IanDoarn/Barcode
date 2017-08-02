"""
Prototype class object for
other barcode types used in the environment

Written by: Ian Doarn
"""
from hibc import HIBC
from gs1 import GS1
import re
# TODO: Comment this file!


class Barcode(object):

    def __init__(self, barcode):
        self.barcode_data = self.__verify_barcode(barcode)
        self.barcode = barcode

    def __verify_barcode(self, __barcode):
        if re.match(r'^(ZI|zi)(\d*)$', __barcode):
            raise ValueError('Invalid barcode [{}] Can not parse ZTags'.format(__barcode))
        elif re.match(r'^(\w{1,4})(-)\d*$', __barcode):
            return [x for x in re.search(r'^(\w{1,4})(-)(\d*)$', t).groups() if x != '-']
        elif re.match(r'^\w{1,4}-\d*-\d{1,3}$', __barcode):
            return [x for x in re.search(r'^(\w{1,4})(-)(\d*)(-)(\d{1,3})$', t).groups() if x != '-']
        elif re.match(r'(^[+])\w(\d{3})([\w\d]*)/(\d{6})(\d*)([\w\d_+$\-.\s%]*)$', __barcode):
            return HIBC(__barcode).parse()
        elif re.match(r'^(01)[0-9]{14}(10[0-9]*|17[0-9]{6})(10[0-9]*|17[0-9]{6})$',
                      re.sub(r'[^A-Za-z0-9]+', '', __barcode)):
            return GS1(__barcode).parse()
        raise ValueError('Invalid barcode [{}]'.format(__barcode))


tests = [
    'CASE-1352315',
    'Z-356415-51',
    'X-78587192',
    'MOV-10004655',
    'ORD-7876585',
    '+H124425114008161/2203162599746A14.',
    '01008803044758231722050410986720'
]
for t in tests:
    b = Barcode(t)
    print(b.barcode_data)

