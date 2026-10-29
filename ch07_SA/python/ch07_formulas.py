"""LaTeX sources of Chapter 7 formula images."""
FORMULAS = {
 'f_metropolis': r"P(\mathrm{accept}) = 1 \;\;\mathrm{if}\;\; \Delta \leq 0, \qquad P(\mathrm{accept}) = \exp\!\left(-\frac{\Delta}{T}\right) \;\;\mathrm{if}\;\; \Delta > 0, \qquad \Delta = f(y) - f(x)",
 'f_T0': r"T_0 = -\frac{\bar{\Delta}^{+}}{\ln p_0} \qquad (\bar{\Delta}^{+} = \mathrm{average\ increase\ of\ worse\ moves\ in\ a\ short\ random\ walk},\ p_0 = \mathrm{target\ initial\ acceptance})",
 'f_cooling': r"T_{k+1} = \alpha\, T_k \quad (0 < \alpha < 1), \qquad \mathrm{number\ of\ temperature\ levels\ } m = \frac{\ln(T_f / T_0)}{\ln \alpha}, \qquad \mathrm{evaluations} \approx m \times L",
 'f_sn': r"\mathrm{SN} = -10 \log_{10}\!\left( \frac{1}{R}\sum_{r=1}^{R} RPD_r^{\,2} \right) \qquad (\mathrm{smaller\ the\ better;\ larger\ SN\ is\ better})",
}
