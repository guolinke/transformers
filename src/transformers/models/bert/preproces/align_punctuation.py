import sys
import re

# as in it's, I'm, we'd
# $text =~ s='([sSmMdD]) = '$1 =g;
# $text =~ s='ll = 'll =g;
# $text =~ s='re = 're =g;
# $text =~ s='ve = 've =g;
# $text =~ s=n't = n't =g;
# $text =~ s='LL = 'LL =g;
# $text =~ s='RE = 'RE =g;
# $text =~ s='VE = 'VE =g;
# $text =~ s=N'T = N'T =g;
# https://stackoverflow.com/questions/32031353/replace-single-quotes-with-double-with-exclusion-of-some-elements
p = re.compile(r'(?:(?<!\w)\'((?:.|\n)+?\'?)(?:(?<!s)\'(?!\w)|(?<=s)\'(?!([^\']|\w\'\w)+\'(?!\w))))')
subst = u"\"\g<1>\""
for line in sys.stdin:
    line = re.sub(r" '([sSmMdD])\b", r"'\1", line)
    line = re.sub(r" 'll\b", "'ll", line)
    line = re.sub(r" 're\b", "'re", line)
    line = re.sub(r" 've\b", "'ve", line)
    line = re.sub(r" n't\b", "n't", line)
    line = re.sub(r" 'LL\b", "'LL", line)
    line = re.sub(r" 'RE\b", "'RE", line)
    line = re.sub(r" 'VE\b", "'VE", line)
    line = re.sub(r" N'T\b", "N'T", line)
    #line = re.sub(p, subst, line)
    sys.stdout.write(line.strip() + '\n')