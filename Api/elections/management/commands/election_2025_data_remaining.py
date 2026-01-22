"""
Données restantes pour les régions : Nord-Ouest, Ouest, Sud, Sud-Ouest
Extraites du PDF officiel pages 16-23
"""
from decimal import Decimal

# Résultats par département - RÉGION DU NORD-OUEST (pages 16-17 du PDF)
DEPARTMENT_RESULTS_NORD_OUEST = {
    "Boyo": {
        "ATEKI SETA CAXTON": {"votes": 29, "percentage": Decimal("0.30")},
        "BELLO BOUBA MAIGARI": {"votes": 1189, "percentage": Decimal("12.24")},
        "BIYA PAUL": {"votes": 6614, "percentage": Decimal("68.08")},
        "BOUGHA HAGBE JACQUES": {"votes": 18, "percentage": Decimal("0.18")},
        "ISSA TCHIROMA": {"votes": 771, "percentage": Decimal("7.94")},
        "IYODI HIRAM SAMUEL": {"votes": 32, "percentage": Decimal("0.33")},
        "KWEMO PIERRE": {"votes": 17, "percentage": Decimal("0.17")},
        "LIBII LI NGUE NGUE CABRAL": {"votes": 31, "percentage": Decimal("0.32")},
        "MATOMBA SERGE ESPOIR": {"votes": 18, "percentage": Decimal("0.18")},
        "MUNA AKERE TABENG": {"votes": 26, "percentage": Decimal("0.27")},
        "OSIH JOSHUA NAMBANGI": {"votes": 945, "percentage": Decimal("9.73")},
        "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 25, "percentage": Decimal("0.26")},
    },
    "Bui": {
        "ATEKI SETA CAXTON": {"votes": 7, "percentage": Decimal("0.04")},
        "BELLO BOUBA MAIGARI": {"votes": 50, "percentage": Decimal("0.31")},
        "BIYA PAUL": {"votes": 13923, "percentage": Decimal("85.46")},
        "BOUGHA HAGBE JACQUES": {"votes": 2, "percentage": Decimal("0.01")},
        "ISSA TCHIROMA": {"votes": 320, "percentage": Decimal("1.96")},
        "IYODI HIRAM SAMUEL": {"votes": 7, "percentage": Decimal("0.04")},
        "KWEMO PIERRE": {"votes": 1, "percentage": Decimal("0.01")},
        "LIBII LI NGUE NGUE CABRAL": {"votes": 15, "percentage": Decimal("0.09")},
        "MATOMBA SERGE ESPOIR": {"votes": 6, "percentage": Decimal("0.04")},
        "MUNA AKERE TABENG": {"votes": 2, "percentage": Decimal("0.01")},
        "OSIH JOSHUA NAMBANGI": {"votes": 1953, "percentage": Decimal("11.99")},
        "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 7, "percentage": Decimal("0.04")},
    },
    "Donga-Mantung": {
        "ATEKI SETA CAXTON": {"votes": 254, "percentage": Decimal("0.63")},
        "BELLO BOUBA MAIGARI": {"votes": 1758, "percentage": Decimal("4.38")},
        "BIYA PAUL": {"votes": 29219, "percentage": Decimal("72.83")},
        "BOUGHA HAGBE JACQUES": {"votes": 58, "percentage": Decimal("0.14")},
        "ISSA TCHIROMA": {"votes": 4806, "percentage": Decimal("11.98")},
        "IYODI HIRAM SAMUEL": {"votes": 95, "percentage": Decimal("0.24")},
        "KWEMO PIERRE": {"votes": 73, "percentage": Decimal("0.18")},
        "LIBII LI NGUE NGUE CABRAL": {"votes": 253, "percentage": Decimal("0.63")},
        "MATOMBA SERGE ESPOIR": {"votes": 137, "percentage": Decimal("0.34")},
        "MUNA AKERE TABENG": {"votes": 426, "percentage": Decimal("1.06")},
        "OSIH JOSHUA NAMBANGI": {"votes": 2760, "percentage": Decimal("6.88")},
        "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 283, "percentage": Decimal("0.71")},
    },
    "Menchum": {
        "ATEKI SETA CAXTON": {"votes": 151, "percentage": Decimal("1.46")},
        "BELLO BOUBA MAIGARI": {"votes": 221, "percentage": Decimal("2.13")},
        "BIYA PAUL": {"votes": 5517, "percentage": Decimal("53.24")},
        "BOUGHA HAGBE JACQUES": {"votes": 53, "percentage": Decimal("0.51")},
        "ISSA TCHIROMA": {"votes": 1972, "percentage": Decimal("19.03")},
        "IYODI HIRAM SAMUEL": {"votes": 46, "percentage": Decimal("0.44")},
        "KWEMO PIERRE": {"votes": 46, "percentage": Decimal("0.44")},
        "LIBII LI NGUE NGUE CABRAL": {"votes": 44, "percentage": Decimal("0.43")},
        "MATOMBA SERGE ESPOIR": {"votes": 154, "percentage": Decimal("1.49")},
        "MUNA AKERE TABENG": {"votes": 29, "percentage": Decimal("0.28")},
        "OSIH JOSHUA NAMBANGI": {"votes": 2072, "percentage": Decimal("20.00")},
        "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 57, "percentage": Decimal("0.55")},
    },
    "Mezam": {
        "ATEKI SETA CAXTON": {"votes": 71, "percentage": Decimal("0.04")},
        "BELLO BOUBA MAIGARI": {"votes": 789, "percentage": Decimal("0.47")},
        "BIYA PAUL": {"votes": 155885, "percentage": Decimal("92.12")},
        "BOUGHA HAGBE JACQUES": {"votes": 73, "percentage": Decimal("0.04")},
        "ISSA TCHIROMA": {"votes": 6447, "percentage": Decimal("3.81")},
        "IYODI HIRAM SAMUEL": {"votes": 166, "percentage": Decimal("0.10")},
        "KWEMO PIERRE": {"votes": 37, "percentage": Decimal("0.02")},
        "LIBII LI NGUE NGUE CABRAL": {"votes": 197, "percentage": Decimal("0.12")},
        "MATOMBA SERGE ESPOIR": {"votes": 79, "percentage": Decimal("0.05")},
        "MUNA AKERE TABENG": {"votes": 160, "percentage": Decimal("0.09")},
        "OSIH JOSHUA NAMBANGI": {"votes": 5213, "percentage": Decimal("3.08")},
        "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 104, "percentage": Decimal("0.06")},
    },
    "Momo": {
        "ATEKI SETA CAXTON": {"votes": 15, "percentage": Decimal("0.06")},
        "BELLO BOUBA MAIGARI": {"votes": 1044, "percentage": Decimal("3.99")},
        "BIYA PAUL": {"votes": 21303, "percentage": Decimal("81.42")},
        "BOUGHA HAGBE JACQUES": {"votes": 4, "percentage": Decimal("0.02")},
        "ISSA TCHIROMA": {"votes": 738, "percentage": Decimal("2.82")},
        "IYODI HIRAM SAMUEL": {"votes": 7, "percentage": Decimal("0.03")},
        "KWEMO PIERRE": {"votes": 3, "percentage": Decimal("0.01")},
        "LIBII LI NGUE NGUE CABRAL": {"votes": 19, "percentage": Decimal("0.07")},
        "MATOMBA SERGE ESPOIR": {"votes": 13, "percentage": Decimal("0.05")},
        "MUNA AKERE TABENG": {"votes": 8, "percentage": Decimal("0.03")},
        "OSIH JOSHUA NAMBANGI": {"votes": 3004, "percentage": Decimal("11.48")},
        "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 5, "percentage": Decimal("0.02")},
    },
    "Ngo-Ketunjia": {
        "ATEKI SETA CAXTON": {"votes": 7, "percentage": Decimal("0.03")},
        "BELLO BOUBA MAIGARI": {"votes": 274, "percentage": Decimal("1.15")},
        "BIYA PAUL": {"votes": 22727, "percentage": Decimal("95.54")},
        "BOUGHA HAGBE JACQUES": {"votes": 14, "percentage": Decimal("0.06")},
        "ISSA TCHIROMA": {"votes": 338, "percentage": Decimal("1.42")},
        "IYODI HIRAM SAMUEL": {"votes": 14, "percentage": Decimal("0.06")},
        "KWEMO PIERRE": {"votes": 10, "percentage": Decimal("0.04")},
        "LIBII LI NGUE NGUE CABRAL": {"votes": 34, "percentage": Decimal("0.14")},
        "MATOMBA SERGE ESPOIR": {"votes": 2, "percentage": Decimal("0.01")},
        "MUNA AKERE TABENG": {"votes": 5, "percentage": Decimal("0.02")},
        "OSIH JOSHUA NAMBANGI": {"votes": 345, "percentage": Decimal("1.45")},
        "TOMAINO HERMINE PATRICIA épouse NDAM NJOYA": {"votes": 19, "percentage": Decimal("0.08")},
    },
}

# Statistiques par département - RÉGION DU NORD-OUEST (page 16 du PDF)
DEPARTMENT_STATS_NORD_OUEST = {
    "Boyo": {
        "inscrits": 56828,
        "votants": 9775,
        "taux_participation": Decimal("17.20"),
        "taux_abstention": Decimal("82.80"),
        "bulletins_nuls": 60,
        "suffrages_exprimes": 9715
    },
    "Bui": {
        "inscrits": 104230,
        "votants": 16364,
        "taux_participation": Decimal("15.70"),
        "taux_abstention": Decimal("84.30"),
        "bulletins_nuls": 71,
        "suffrages_exprimes": 16293
    },
    "Donga-Mantung": {
        "inscrits": 96778,
        "votants": 40630,
        "taux_participation": Decimal("41.98"),
        "taux_abstention": Decimal("58.02"),
        "bulletins_nuls": 508,
        "suffrages_exprimes": 40122
    },
    "Menchum": {
        "inscrits": 52568,
        "votants": 10520,
        "taux_participation": Decimal("20.01"),
        "taux_abstention": Decimal("79.99"),
        "bulletins_nuls": 158,
        "suffrages_exprimes": 10362
    },
    "Mezam": {
        "inscrits": 208476,
        "votants": 169952,
        "taux_participation": Decimal("81.52"),
        "taux_abstention": Decimal("18.48"),
        "bulletins_nuls": 731,
        "suffrages_exprimes": 169221
    },
    "Momo": {
        "inscrits": 57183,
        "votants": 26317,
        "taux_participation": Decimal("46.02"),
        "taux_abstention": Decimal("53.98"),
        "bulletins_nuls": 154,
        "suffrages_exprimes": 26163
    },
    "Ngo-Ketunjia": {
        "inscrits": 52033,
        "votants": 24317,
        "taux_participation": Decimal("46.73"),
        "taux_abstention": Decimal("53.27"),
        "bulletins_nuls": 528,
        "suffrages_exprimes": 23789
    },
}
