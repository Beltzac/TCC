from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import pprint 

result_handle=NCBIWWW.qblast('blastn','nr','ACCATCCGCCGAAAGATGGTCGACGGCGTGCAGGTGCACTTCTGGGCCGACGAAGAGCGCGAACTGTCCTTCCTCAACAACTTCGCCTTCGAAGGCGGCACGACCATCTTCCAGGCCACCGGCCAATGGAACGACGCCTTCAACGCCACCTGACCGGCCTGCGCGCCAAGAAGGCCAAGGTCGAGATCGTGCCCGAACCCAAGTTCAGCTAAAAATTAA')
records = NCBIXML.parse(result_handle)
blastrecord = records.next()
for alignment in blastrecord.alignments:
	for hsp in alignment.hsps:
		if hsp.expect < 0.01:
			print "****Alinhamento****"
			print "Sequencia:", alignment.title
			print "Tamanho:", alignment.length
			print "Valor E:", hsp.expect
			print hsp.query[:50] + "..."
			print hsp.match[:50] + "..."
			print hsp.sbjct[:50] + "..."
			print "----------------------------------------------"
			pprint.pprint(vars(alignment))

      