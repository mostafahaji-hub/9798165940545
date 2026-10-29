"""LaTeX sources of Chapter 5 formula images."""
FORMULAS = {
 'f_vam':   r"\mathrm{penalty\ of\ row\ } i = c_{i(2)} - c_{i(1)}, \qquad \mathrm{penalty\ of\ column\ } j = c_{(2)j} - c_{(1)j} \qquad (\mathrm{two\ smallest\ costs\ still\ available})",
 'f_modi1': r"u_i + v_j = c_{ij} \quad \mathrm{for\ every\ basic\ (allocated)\ cell}, \qquad u_1 = 0",
 'f_modi2': r"k_{ij} = c_{ij} - u_i - v_j \quad \mathrm{for\ every\ empty\ cell}; \qquad k_{ij} < 0 \Rightarrow \mathrm{allocating\ to\ } (i,j) \mathrm{\ reduces\ cost}",
 'f_theta': r"\Delta Z = \theta \cdot k_{ij}, \qquad \theta = \min\{x \mathrm{\ of\ the\ cells\ with\ a\ minus\ sign\ on\ the\ loop}\}",
 'f_eff':   r"\tilde{c}_{ij} = c_{ij} + \frac{f_{ij}}{\min(s_i,\, d_j)} \qquad (\mathrm{effective\ unit\ cost})",
 'f_pattern': r"Z(y) = \min_{x \geq 0} \sum_{ij} c_{ij} x_{ij} + \sum_{ij} f_{ij} y_{ij} \quad \mathrm{s.t.\ supply,\ demand,\ } x_{ij} = 0 \mathrm{\ if\ } y_{ij} = 0",
 'f_rpd':   r"RPD = \frac{Z_{heuristic} - Z_{optimal}}{Z_{optimal}} \times 100\%",
}
