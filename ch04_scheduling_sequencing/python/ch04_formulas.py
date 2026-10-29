"""LaTeX sources of Chapter 4 formula images."""
FORMULAS = {
 'f_completion': r"C_{[1]} = p_{[1]}, \qquad C_{[k]} = C_{[k-1]} + p_{[k]} \quad (k = 2,\ldots,n)",
 'f_ET':         r"E_i = \max(0,\; d_i - C_i), \qquad T_i = \max(0,\; C_i - d_i), \qquad L_i = C_i - d_i",
 'f_ET_obj':     r"\min\; Z = \sum_{i=1}^{n} \left( \alpha_i\, E_i + \beta_i\, T_i \right) \qquad \mathrm{subject\ to:\ } (s_1,\ldots,s_n) \mathrm{\ is\ a\ permutation\ of\ } \{1,\ldots,n\}",
 'f_objectives': r"C_{\max} = \sum_i p_i, \qquad \sum_i C_i, \qquad L_{\max} = \max_i L_i, \qquad \sum_i T_i, \qquad \sum_i w_i T_i, \qquad \sum_i (\alpha_i E_i + \beta_i T_i)",
 'f_tsp_obj':    r"\min\; Z = \sum_{i=0}^{n}\sum_{j \neq i} d_{ij}\, x_{ij}",
 'f_tsp_con':    r"\sum_{j \neq i} x_{ij} = 1 \;\;(\forall i), \qquad \sum_{i \neq j} x_{ij} = 1 \;\;(\forall j), \qquad u_i - u_j + n\,x_{ij} \leq n - 1 \;\;(i \neq j;\; i,j = 1,\ldots,n), \qquad x_{ij} \in \{0,1\}",
 'f_tours':      r"\mathrm{number\ of\ distinct\ tours} = \frac{n!}{2} \quad (\mathrm{symmetric\ distances},\; n \mathrm{\ shops})",
 'f_vrp_obj':    r"\min\; Z = \sum_{i=0}^{n}\sum_{j \neq i} d_{ij}\, x_{ij}, \qquad \sum_{j \neq i} x_{ij} = 1,\;\; \sum_{i \neq j} x_{ij} = 1 \;\;(i,j = 1,\ldots,n), \qquad \sum_{j=1}^{n} x_{0j} \leq K",
 'f_vrp_cap':    r"\ell_j \geq \ell_i + q_j - Q\,(1 - x_{ij}) \;\;(i \neq j;\; i,j = 1,\ldots,n), \qquad q_j \leq \ell_j \leq Q, \qquad x_{ij} \in \{0,1\}",
}
