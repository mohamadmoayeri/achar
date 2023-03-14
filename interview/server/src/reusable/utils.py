def translate_number(number):
    fa_num = '۰١٢٣٤٥٦٧٨٩'
    en_num = '0123456789'
    table = str.maketrans(en_num, fa_num)
    persian_number = str(number).translate(table)
    return persian_number