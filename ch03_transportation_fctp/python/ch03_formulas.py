"""LaTeX sources of Chapter 3 formula images (rendered with matplotlib mathtext, 300 dpi)."""
FORMULAS = {
 'f_tp_obj':  r"\min\; Z = \sum_{i=1}^{m}\sum_{j=1}^{n} c_{ij}\,x_{ij}",
 'f_tp_con':  r"\sum_{j=1}^{n} x_{ij} \leq s_i \quad (i=1,\ldots,m), \qquad \sum_{i=1}^{m} x_{ij} = d_j \quad (j=1,\ldots,n), \qquad x_{ij} \geq 0",
 'f_balance': r"\sum_{i=1}^{m} s_i = \sum_{j=1}^{n} d_j \;\;(\mathrm{balanced}), \qquad \sum_i s_i > \sum_j d_j \;\;(\mathrm{surplus}), \qquad \sum_i s_i < \sum_j d_j \;\;(\mathrm{shortage})",
 'f_param':   r"Z(t) = 4t + 7(50-t) + 3(40-t) + 5(30+t) = 620 - t, \qquad 0 \leq t \leq 40",
 'f_ts_obj':  r"\min\; Z = \sum_{i}\sum_{k} a_{ik}\,x_{ik} + \sum_{k}\sum_{j} b_{kj}\,y_{kj}",
 'f_ts_con':  r"\sum_{k} x_{ik} \leq s_i \;\;(\forall i), \qquad \sum_{i} x_{ik} \leq q_k \;\;(\forall k), \qquad \sum_{i} x_{ik} = \sum_{j} y_{kj} \;\;(\forall k), \qquad \sum_{k} y_{kj} = d_j \;\;(\forall j)",
 'f_fc_obj':  r"\min\; Z = \sum_{i}\sum_{j} \left( c_{ij}\,x_{ij} + f_{ij}\,y_{ij} \right)",
 'f_fc_con':  r"\sum_{j} x_{ij} \leq s_i, \qquad \sum_{i} x_{ij} = d_j, \qquad x_{ij} \leq M_{ij}\,y_{ij}, \qquad M_{ij} = \min(s_i, d_j), \qquad x_{ij} \geq 0,\;\; y_{ij} \in \{0,1\}",
 'f_patterns':r"\mathrm{number\ of\ open/closed\ patterns} = 2^{\,m \times n}",
 'f_lanecost':r"\mathrm{lane\ cost}(x_{ij}) = 0 \;\;\mathrm{if}\;\; x_{ij} = 0, \qquad \mathrm{lane\ cost}(x_{ij}) = f_{ij} + c_{ij}\,x_{ij} \;\;\mathrm{if}\;\; x_{ij} > 0",
}
