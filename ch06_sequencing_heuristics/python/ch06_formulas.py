"""LaTeX sources of Chapter 6 formula images."""
FORMULAS = {
 'f_rules':   r"\mathrm{WSPT:\ sort\ by\ } \frac{p_i}{\beta_i} \uparrow, \qquad \mathrm{slack:\ sort\ by\ } d_i - p_i \uparrow, \qquad \mathrm{our\ rule:\ sort\ by\ } \frac{d_i}{\beta_i} \uparrow",
 'f_atc':     r"I_i(t) = \frac{\beta_i}{p_i}\, \exp\!\left( -\frac{\max(0,\; d_i - p_i - t)}{K\,\bar{p}} \right) \qquad (\mathrm{ATC\ index\ at\ time\ } t)",
 'f_savings': r"s_{ij} = d_{0i} + d_{0j} - d_{ij} \qquad (\mathrm{saving\ of\ joining\ } i \mathrm{\ and\ } j)",
 'f_insert':  r"\Delta_{\mathrm{insert}}(k \mathrm{\ between\ } a,b) = d_{ak} + d_{kb} - d_{ab}",
 'f_twoopt':  r"\Delta_{\mathrm{2opt}} = d_{ac} + d_{bd} - d_{ab} - d_{cd} \qquad (\mathrm{remove\ edges\ } ab, cd;\ \mathrm{add\ } ac, bd;\ \mathrm{reverse\ the\ segment\ } b \ldots c)",
 'f_sweep':   r"\theta_i = \mathrm{atan2}(y_i - y_0,\; x_i - x_0) \qquad (\mathrm{sweep\ angle\ of\ shop\ } i \mathrm{\ seen\ from\ the\ depot})",
}
