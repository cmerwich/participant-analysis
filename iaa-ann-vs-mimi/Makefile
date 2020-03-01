PS_A   = $(HOME)/Sites/brat/data/coref/Psalms/annotate
PS_B   = $(HOME)/github/cmerwich/participant-analysis/iaa-ann-vs-mimi

PYTHON3 = python3

PS_IAA = $(shell ls $(PS_B)/*.ann |awk -F/ '{print $$NF}' | sed 's/ann$$/iaa/')

Psalms_%.iaa: iaa.py $(PS_A)/Psalms_%.ann $(PS_B)/Psalms_%.ann
	$(PYTHON3) iaa.py $(PS_A)/Psalms_$*.ann $(PS_B)/Psalms_$*.ann > $@

all: total_psalms
	sort -k 7n,7 total_psalms
	$(PYTHON3) acc.py total_psalms

total_psalms: acc.py $(PS_IAA)
	$(PYTHON3) acc.py $(PS_IAA) > $@
