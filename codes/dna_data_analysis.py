from codes.DNA_QC import dna_qc
from codes.panelcreation import panel
from codes.cgi_analysis import cgi
from codes.CNV import cnv_analysis
from codes.annotation import anno
from codes.filter_engine import filtereng
from codes.TMB import tmb_calculation
from codes.MSI import msi_analysis

def dna_data_analysis():
    print("Running DNA QC")
    dna_qc()
    print("Running Panel")
    panel()
    print("Running CGI")
    cgi()
    print("Running CNV")
    cnv_analysis()
