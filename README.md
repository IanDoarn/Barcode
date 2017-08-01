# Barcode

Parses HIBC and GS1 barcode's

Written by: Ian Doarn

## Usage
Simply call either hibc.py, gs1.p1 or parse.py from the commandline
and pass the barcode in as an argument

#### HIBC Example:
```commandline
python hibc.py +H124425114008161/2203162599746A14.
```

Returns:
```
units: 1
lot_number: 06121404
barcode: +M894NX55M1/1915206121404F14B
expiration_date: 2019-06-01
edi_number: NX55M
lic: M894
manufactured_date: 2014-06-01

```

#### GS1 Example:
```commandline
python gs1.py 010088030454456710353259317200325
```

Returns:
```
barcode: 010088030454456710353259317200325
gtin_number: 00880304544567
expiration_date: 2020-03-25
ean_number: 01
lot_number: 3532593
```
