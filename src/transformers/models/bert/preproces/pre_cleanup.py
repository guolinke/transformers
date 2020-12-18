import re
import sys
import unicodedata

def _is_whitespace(char):
    """Checks whether `chars` is a whitespace character."""
    # \t, \n, and \r are technically contorl characters but we treat them
    # as whitespace since they are generally considered as such.
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def _is_control(char):
    """Checks whether `chars` is a control character."""
    # These are technically control characters but we count them as whitespace
    # characters.
    if char == "\t" or char == "\n" or char == "\r":
        return False
    cat = unicodedata.category(char)
    if cat in ("Cc", "Cf"):
        return True
    return False

def _clean_text(text):
    """Performs invalid character removal and whitespace cleanup on text."""
    output = []
    for char in text:
        cp = ord(char)
        if cp == 0 or cp == 0xfffd or _is_control(char):
            continue
        if _is_whitespace(char):
            output.append(" ")
        else:
            output.append(char)
    return "".join(output)

def pre_cleanup(line):
    line = _clean_text(line)
    # fix repeating quotes in QQP
    line = re.sub(r"\'\'", '"', line)
    line = re.sub(r'""', '"', line)
    line = line.replace('\t', ' ')  # replace tab with spaces
    line = ' '.join(line.strip().split())  # remove redundant spaces
    line = line.replace('…', '...')
    line = re.sub(r'\.{4,}', '...', line)  # remove extra dots
    line = line.replace('<<', '«').replace('>>', '»')  # group << together
    line = re.sub(' (,:\.\)\]»)', r'\1', line)  # remove space before >>
    line = re.sub('(\[\(«) ', r'\1', line)  # remove space after <<
    line = line.replace(',,', ',').replace(',.', '.')  # remove redundant punctuations
    line = re.sub(r' \*([^ ])', r' \1', line)  # remove redundant asterisks
    line = re.sub(r'^\[\d+\:\d+\]', '', line)
    # fix the single quote problems
    line = re.sub(r"’([sSmMdD])\b", r"'\1", line)
    line = re.sub(r"’ll\b", "'ll", line)
    line = re.sub(r"’re\b", "'re", line)
    line = re.sub(r"’ve\b", "'ve", line)
    line = re.sub(r"n’t\b", "n't", line)
    line = re.sub(r"’LL\b", "'LL", line)
    line = re.sub(r"’RE\b", "'RE", line)
    line = re.sub(r"’VE\b", "'VE", line)
    line = re.sub(r"N’T\b", "N'T", line)
    #reverse
    line = line[::-1]
    line = re.sub(r"’([^‘]+)‘", r'"\1"', line)
    line = re.sub(r"’([^‘]+)‘", r'"\1"', line)
    line = re.sub(r"’([^‘]+)‘", r'"\1"', line)
    line = line[::-1]
    return ' '.join(line.strip().split())  # remove redundant spaces


def main():
    for line in sys.stdin:
        line = line.strip()
        if line:
            line = pre_cleanup(line)
            sys.stdout.write(line + '\n')
        else:
            sys.stdout.write('\n')


if __name__ == '__main__':
    main()