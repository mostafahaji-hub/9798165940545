"""LaTeX sources of Chapter 8 formula images."""
FORMULAS = {
 'f_rk': r"\mathrm{chromosome:}\ \ k = (k_1, k_2, \ldots, k_n), \quad k_i \in [0, 1) \qquad \mathrm{decoding:\ sort\ the\ keys\ ascending;\ the\ order\ of\ indices\ is\ the\ sequence}",
 'f_fit': r"\mathrm{fit}_i = Z_{worst} - Z_i + 1 \;\;(\mathrm{minimisation}), \qquad \mathrm{fit}_i = Z_i \;\;(\mathrm{maximisation\ of\ a\ positive\ profit})",
 'f_roulette': r"p_i = \frac{\mathrm{fit}_i}{\sum_j \mathrm{fit}_j}, \qquad c_i = \sum_{j \leq i} p_j, \qquad \mathrm{draw\ } u \sim U(0,1): \mathrm{\ select\ the\ first\ } i \mathrm{\ with\ } c_i \geq u",
 'f_xover': r"\mathrm{uniform:}\ c^{(1)}_i = m_i\,p^{(1)}_i + (1-m_i)\,p^{(2)}_i, \quad c^{(2)}_i = m_i\,p^{(2)}_i + (1-m_i)\,p^{(1)}_i, \qquad m_i \in \{0,1\} \mathrm{\ random\ mask}",
 'f_gens': r"\mathrm{evaluations\ per\ generation} \approx N - E, \qquad \mathrm{generations} \approx \frac{\mathrm{budget} - N}{N - E}",
}
