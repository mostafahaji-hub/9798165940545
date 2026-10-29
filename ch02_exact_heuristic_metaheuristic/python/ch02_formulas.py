"""LaTeX source of every formula image used in Chapter 2 (rendered with matplotlib mathtext at 300 dpi).
Keep this file: it is the editable source for the English edition."""
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'DejaVu Sans'
FORMULAS = {
 'f_rpd':    r"RPD = \frac{Z_{method} - Z_{best}}{Z_{best}} \times 100\%",
 'f_nbsize': r"|N_{swap}(s)| = \binom{n}{2} = \frac{n(n-1)}{2}, \qquad |N_{insert}(s)| = (n-1)^2, \qquad |N_{inv}(s)| = \binom{n}{2}",
 'f_tp_obj': r"\min\; Z = \sum_{i=1}^{m}\sum_{j=1}^{n} c_{ij}\,x_{ij}",
 'f_tp_con': r"\sum_{j=1}^{n} x_{ij} \leq s_i \;\; (i=1,\ldots,m), \qquad \sum_{i=1}^{m} x_{ij} = d_j \;\; (j=1,\ldots,n), \qquad x_{ij} \geq 0",
 'f_evals':  r"\mathrm{evaluations} \approx \mathrm{population\ size} \times \mathrm{iterations} = 100 \times 100 = 10{,}000",
 'f_runs':   r"\bar{Z} = \frac{1}{R}\sum_{r=1}^{R} Z_r, \qquad Z_{best} = \min_r Z_r, \qquad Z_{worst} = \max_r Z_r",
 'f_et':     r"C_{[1]} = p_{[1]}, \quad C_{[k]} = C_{[k-1]} + p_{[k]}, \qquad Z = \sum_{i} \left[\alpha_i \max(0, d_i - C_i) + \beta_i \max(0, C_i - d_i)\right]",
 'f_eff':    r"\tilde{c}_{ij} = c_{ij} + \frac{f_{ij}}{\min(s_i, d_j)}",
 'f_sphere':   r"f_{Sphere}(x) = \sum_{i=1}^{D} x_i^2, \qquad x_i \in [-100, 100], \qquad f^* = 0 \;\; \mathrm{at}\; x = (0,\ldots,0)",
 'f_rosen':    r"f_{Rosenbrock}(x) = \sum_{i=1}^{D-1} \left[100\,(x_{i+1} - x_i^2)^2 + (1 - x_i)^2\right], \qquad f^* = 0 \;\; \mathrm{at}\; x = (1,\ldots,1)",
 'f_rastrigin':r"f_{Rastrigin}(x) = 10D + \sum_{i=1}^{D} \left[x_i^2 - 10\cos(2\pi x_i)\right], \qquad x_i \in [-5.12, 5.12], \qquad f^* = 0",
 'f_ackley':   r"f_{Ackley}(x) = -20\exp\left(-0.2\sqrt{\frac{1}{D}\sum_{i=1}^{D} x_i^2}\right) - \exp\left(\frac{1}{D}\sum_{i=1}^{D} \cos(2\pi x_i)\right) + 20 + e, \qquad f^* = 0",
 'f_griewank': r"f_{Griewank}(x) = 1 + \frac{1}{4000}\sum_{i=1}^{D} x_i^2 - \prod_{i=1}^{D} \cos\left(\frac{x_i}{\sqrt{i}}\right), \qquad f^* = 0",
 'f_gap':      r"\mathrm{Gap} = \frac{Z - LB}{LB} \times 100\%",
 'f_rpdmean':  r"\overline{RPD} = \frac{1}{R}\sum_{r=1}^{R} \frac{Z_r - Z_{best}}{Z_{best}} \times 100\%",
 'f_balinski': r"\min\; \sum_{i}\sum_{j} \left(c_{ij} + \frac{f_{ij}}{\min(s_i, d_j)}\right) x_{ij} \quad \mathrm{subject\ to\ the\ supply\ and\ demand\ constraints}",
}
def render(outdir='../figures', fs=20):
    for name, tex in FORMULAS.items():
        fig = plt.figure(figsize=(0.1, 0.1)); fig.text(0, 0, f"${tex}$", fontsize=fs)
        fig.savefig(f'{outdir}/{name}.png', dpi=300, bbox_inches='tight', pad_inches=0.08); plt.close()
if __name__ == '__main__': render()
