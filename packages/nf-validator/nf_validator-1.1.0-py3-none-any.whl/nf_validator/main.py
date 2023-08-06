import unicodedata2


def nf_validating(parameter):
    to_list = parameter.split()
    to_string = " ".join(to_list)
    only_ascii = unicodedata2.normalize('NFKD', to_string).encode('ASCII', 'ignore').decode('utf-8').strip().replace(
        " ", "")
    if only_ascii.isalpha():
        return to_string.strip()
    else:
        return False

