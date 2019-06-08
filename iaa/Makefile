NU_A   = $(HOME)/Sites/brat/data/coref/Numbers/annotate
NU_B   = $(HOME)/Sites/brat/data/gyusang/coref/Numbers/annotate
PS_A   = $(HOME)/Sites/brat/data/coref/Psalms/annotate
PS_B   = $(HOME)/Sites/brat/data/gyusang/coref/Psalms/annotate

PYTHON3 = python3

NU_IAA = $(shell ls $(NU_B)/*.ann |awk -F/ '{print $$NF}' | sed 's/ann$$/iaa/')
PS_IAA = $(shell ls $(PS_B)/*.ann |awk -F/ '{print $$NF}' | sed 's/ann$$/iaa/')

Numbers_%.iaa: iaa.py $(NU_A)/Numbers_%.ann $(NU_B)/Numbers_%.ann
	$(PYTHON3) iaa.py $(NU_A)/Numbers_$*.ann $(NU_B)/Numbers_$*.ann > $@

Psalms_%.iaa: iaa.py $(PS_A)/Psalms_%.ann $(PS_B)/Psalms_%.ann
	$(PYTHON3) iaa.py $(PS_A)/Psalms_$*.ann $(PS_B)/Psalms_$*.ann > $@

all: total_numbers total_psalms
	sort -k 7n,7 total_numbers total_psalms
	$(PYTHON3) acc.py total_numbers total_psalms

total_numbers: acc.py $(NU_IAA)
	$(PYTHON3) acc.py $(NU_IAA) > $@

total_psalms: acc.py $(PS_IAA)
	$(PYTHON3) acc.py $(PS_IAA) > $@
