"""
Health Inventory Barcode Parser

Written By: Ian Doarn

Parses HIBC barcode's and ge their information
Only parses concatenated HIBC's. These are combination
of primary and secondary HIBC join at the center with a '/'. The
'*' at the beginning and end of the  number as seen on the barcode
represent the human readable part of the number

Information in HIBC numbers includes:
    1. Product number
    2. Lot Number
    3. Expiration Date
    4. Manufactured Date
    5. LIC
    6. Units

How a HIBC works:
    1. All HIBC's must begin with the check character '+'
    2. Each character is assigned a value from 0 to 42
       starting at 0 to 1 then A to Z and the additional characters
       ' ', '-', '.', '$', '%', '/', '+'
    3. The primary and secondary must match and are checked by summing
       all the characters values not including the very last one, then
       divide the sum by 43 and the remainder should match the value of
       the last character:

Primary:
    Primary HIBC stores the LIC, Product Number (edi) and Units .
    Example: +M894NX4532MP1
    + / LIC: M894 / Product Number: NX4532MP / Units: 1


     - The LIC M894 can be referenced in a table of values and can show where
       a product was manufactured.
     - The units shows how many of that product are contained in the box

Secondary:
    Secondary HIBC stores the Expiration Date, Lot Number,
    Manufactured Date, and Check Digit.
    Example: 1800113011703A13O
    Expiration Date: 18001 / Lot Number: 13011703 / Manufactured Date: A13

    - The Expiration date is in Julian format and must be converted to standard
      YYYY-MM-DD format. Example: 18001 -> 2018-01-01
    - The Manufactured date is in the format MDYY with its values being
      being represented by the HIBC numbers. Example: A13 -> 2013-01-01
    - The Check Digit value must match the HIBC numbers sum % 43.
    Example:
        '+M894NX4532MP1/1800113011703A13O'
        sum = 282
        sum % 43 = 24
        value of O is 24
        24 == 24
"""

import sys
from collections import OrderedDict
from datetime import datetime
from re import match

# Barcode Table
HIBC_TABLE = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4,
              "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
              "A": 10, "B": 11, "C": 12, "D": 13,
              "E": 14, "F": 15, "G": 16, "H": 17,
              "I": 18, "J": 19, "K": 20, "L": 21,
              "M": 22, "N": 23, "O": 24, "P": 25,
              "Q": 26, "R": 27, "S": 28, "T": 29,
              "U": 30, "V": 31, "W": 32, "X": 33,
              "Y": 34, "Z": 35, "-": 36, ".": 37,
              " ": 38, "$": 39, "/": 40, "+": 41,
              "%": 42}


class HIBC:
    """
    Barcode Parser
    """
    def __init__(self, _hibc_n):
        """
        :param _hibc_n: Barcode Number from barcode
        """
        self.hibc = _hibc_n
        self.primary, self.secondary = None, None
        self.lic = None
        self.units = None
        self.expire_date = None
        self.edi_number = None
        self.lot_number = None
        self.manufactured_date = None

    def parse(self):
        """
        Public method to parse Barcode
        :return:
        """
        return self.__parse_hibc(self.hibc)

    @classmethod
    def __jd_to_dt(cls, jd):
        """
        Convert Julian date to datetime format YYYY-MM-DD

        :param jd: Julian date
        :return: datetime object
        """
        return datetime.strptime(jd, '%y%j').date()

    @classmethod
    def __verify(cls, _hibc):
        """
        Verify HIBC is valid using regex to match

        Pattern: (^[+])\w(\d{3})([\w\d]*)/(\d{6})(\d*)([\w\d_+$\-.\s%]*)$

        :param _hibc: Barcode number
        :return: bool
        """
        if match(r'(^[+])\w(\d{3})([\w\d]*)/(\d{6})(\d*)([\w\d_+$\-.\s%]*)$', _hibc):
            return True
        return False

    @classmethod
    def __verify_concat_hibc(cls, hibc, check_digit):
        """
        Verify that the primary and secondary Barcode match.
        Sum all the values of the Barcode excluding the very last digit,
        divide the number by 43 and take the remainder. If the remainder
        matches the value of the check digit's value the return True,
        otherwise they do not match and return False

        :param hibc: Barcode Number
        :param check_digit: Check digit character
        :return: bool
        """
        chr_list = list(hibc[:-1])
        # Get values from Barcode Table, create a new list, then sum the list and
        # and divide by 43 with the % operator
        if sum([HIBC_TABLE[c] for c in chr_list]) % 43 == HIBC_TABLE[check_digit]:
            return True
        return False

    @classmethod
    def __parse_manufactured_date(cls, key):
        """
        Convert manufactured date to YYYY-MM-DD format

        :param key: Barcode manufactured date value
        :return: datetime object
        """

        # This is pretty ass backwards and needs to be fixed
        date = ''.join([str(HIBC_TABLE[x]) for x in list(key)])
        year = '20' + date[2:]
        month = str(int(date[1]) + 1)
        day = date[0]
        _date = '{}-{}-{}'.format(year, month, day)
        n_date = ''.join(('0' if len(x) < 2 else '')+x for x in _date.split('-'))
        # but somehow it works
        return datetime.strptime(n_date, '%Y%m%d').date()

    def __parse_hibc(self, hibc):
        """
        Parse Barcode value and create a dictionary of its values

        :param hibc: Barcode number
        :return: Ordered Dictionary of values
        """

        # verify Barcode as valid
        if not self.__verify(hibc):
            raise ValueError("Not a valid Barcode [{}]. Missing flag at beginning"
                             " of Barcode: +".format(hibc))

        # Verify Barcode's primary and secondary match
        if not self.__verify_concat_hibc(hibc, hibc[-1:]):
            raise ValueError("Not a valid Barcode [{}]. Primary and "
                             "Secondary Barcode's do not match.".format(hibc))

        # split Barcode on concatenation
        s_hibc = hibc.split(r'/')

        # Analyze Barcode
        self.primary, self.secondary = s_hibc[0], s_hibc[1]
        self.lic = self.primary[1:5]
        self.units = self.primary[-1:]
        self.expire_date = self.__jd_to_dt(self.secondary[:5]) if self.secondary[0] != '%' else 'None'
        self.edi_number = self.primary[5:-1]
        self.lot_number = self.secondary[5:-4]
        self.manufactured_date = self.__parse_manufactured_date(self.secondary[-4:-1])

        # Return its values in an Ordered Dictionary
        return OrderedDict({"barcode": hibc, "lic": self.lic, "units": self.units,
                            "edi_number": self.edi_number, "lot_number": self.lot_number,
                            "expiration_date": self.expire_date,
                            "manufactured_date": self.manufactured_date})


def main(hibc_number):
    hibc_reader = HIBC(hibc_number)
    for k, v in hibc_reader.parse().items():
        print('{}: {}'.format(str(k), str(v)))

if __name__ == '__main__':
    usage = "hibc.py Barcode PARSER\n" \
            "\n" \
            "Basic usage:\n" \
            "Parse:   hibc.py [Barcode NUMBER]\n" \
            "Help:    hibc.py -h\n"
    try:
        if len(sys.argv) > 2 and sys.argv[1] in ['-h', '-H']:
            print(usage)
        else:
            main(sys.argv[1])
    except IndexError as error:
        print(usage)
