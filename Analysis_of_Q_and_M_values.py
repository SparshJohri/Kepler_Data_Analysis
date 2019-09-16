# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 17:52:23 2019

@author: lokes
"""

import pandas as pd

M_File = 'USco_yesdisks_flux_M_edited.csv'
Q_File = 'USco_yesdisks_Q_edited.csv'

m_values = pd.read_csv(M_File)
q_values = pd.read_csv(Q_File)




final_table = pd.DataFrame(columns = ["ID", "M", "Q"], index = list(range(288)))


for i in range(288):
    proto_format1 = str(m_values.iloc[i]).split()
    proto_format2 = str(q_values.iloc[i]).split()
    q = float(proto_format2[5])
    m = float(proto_format1[3])
    ID = int(proto_format1[2])
    
    final_table.iloc[i]=[ID, m, q]


#final_table=final_table.append([[ID, q, m]], ignore_index = True) 
#m_values.set_index(m_values.columns[0], inplace=True, drop = True)