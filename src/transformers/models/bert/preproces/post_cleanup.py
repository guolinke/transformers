import sys
import re

import unicodedata
import unidecode

def acsii_only(s):
    return unidecode.unidecode(s)

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

for line in sys.stdin:
    line = line.strip()
    if line:
        # special cases in STS data
        line = re.sub(u'\' ?[^\x00-\x7F]*', "'", line)
        line = re.sub(r'\\', ' ', line)  # remove all backslashes
        line = re.sub(r'\/', ' / ', line)
        line = re.sub(r'\-+', ' - ', line)

        line = re.sub(r' \.( ?\.){1,}', ' ...', line)
        line = re.sub(r'^\.( ?\.){1,}', '...', line)

        line = re.sub(r'\?', ' ? ', line)
        line = re.sub(r'\!', ' ! ', line)
        line = ' '.join(line.split())
        line = re.sub(r'\?( \?){2,}', '? ? ?', line)
        line = re.sub(r'\!( \!){2,}', '! ! !', line)
        line = re.sub(r'\,( ?\,){1,}', ',', line)
        line = re.sub(r'\,( ?\.){1,}', '.', line)
        line = re.sub(r'\[[\-\,\.\:\?\! \'\"\;]*\]', ' ', line)
        line = re.sub(r'\{[\-\,\.\:\?\! \'\"\;]*\}', ' ', line)
        line = re.sub(r'\([\-\,\.\:\?\! \'\"\;]*\)', ' ', line)
        line = re.sub(r'\<[\-\,\.\:\?\! \'\"\;]*\>', ' ', line)
        # fix unpair quotes
        quotes_cnt = sum(c == '"' for c in line)
        if quotes_cnt == 1:
            #sys.stderr.write(line + '\n')
            line = line.replace('"', "")
            #sys.stderr.write(line + '\n\n')
        # follow BERT
        line = line.replace("'", " ' ")
        line = ' '.join(line.split())
        line = re.sub(r" ' ([smdSMDtT])\b", r" '\1", line)
        line = re.sub(r" ' ll\b", " 'll", line)
        line = re.sub(r" ' re\b", " 're", line)
        line = re.sub(r" ' ve\b", " 've", line)
        line = re.sub(r" ' LL\b", " 'LL ", line)
        line = re.sub(r" ' RE\b", " 'RE ", line)
        line = re.sub(r" ' VE\b", " 'VE ", line)
        # line = re.sub(r"\'", " ' ", line)
        # line = re.sub(r'<[^<>\[\]]*>', ' ', line) # clean html tags
        # line = strip_accents(line)
        # line = acsii_only(line)
        line = ' '.join(line.split())
        sys.stdout.write(line + '\n')
    else:
        sys.stdout.write('\n')