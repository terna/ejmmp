### Stock-flow *model0*, the real part

- We are considering here uniquely the real part of the economy.

- No loans, credits,`` debits, capital stock, interest rate

- Enterpreneurs have unlimited funds that they put freely in their activities.

- Saving is abstension from consuming.

  

### simbols

[symbol table](https://www.caam.rice.edu/~heinken/latex/symbols.pdf) in $\LaTeX$ 

$\mathcal{N}$ - number of agents, `agentNum`

$\mathcal{E}$ - employer number, a uniformly distributed integer number in range $[\mathcal{E}_{min},\mathcal{E}_{max}]$, `employerNum`

$p$ - price `price`

$u$ - unemployment rate `unemploymentRate`

$dimensional~etherogeneity$ is a $true/false$ chooser, forcing increasing firms to attract more workers. `dimensionalEtherogeneity`

$\pi_{i,t}$ - labor productivity, a uniformly distributed decimal number in range $[\pi_{min},\pi_{max}]$,`productivity`

$\Delta\pi_{i,t}$ - uniperiodal additive productivity correction in range $[\Delta\pi_{min},\Delta\pi_{max}]$, `productivityDelta`

$n_{i,t}$ - number of workers in a firm, set just in time

$q_{i,t}$ - production in quantity, `production`

$\Pi_{i,t}$ - profit, `profit`

$w$ - wage `wage`

$r_{i,t}$ - revenues, `revenues`

$s_{i,t}$ - sales, `sales`

$i_{i,t}$ - inventories (final, initial), `initialInventories`, `finalInventories`

$d_{i,t}$ - deperibility share, `deperibilityShare`

$T$ - number of cycles `ncycles`

$t$ - cycle `cycle`

### 

### agent structure

Here we have the structure of a generic agent: it can represent and employer, a worker, an unemployed person.

When an agent is created, the **initialization process** defines:

- its numerical id, `num`

- its employer status, `employer`, set to $false$
- the id of its employer, `myEmployer`, set to $0$
- $r_{i,0}$ - `revenues`, initial value  $0$
- $s_{i,0}$ - `sales`, , initial value  $0$
- $i_{i,0}$ - inventories, `initialInventories`, set to $0$ 



each agent has a **produce** function, used only if is an employer, with:

$\pi_{i,t}=\pi_{i,t-1}+\Delta\pi_{i,t}$

$q_{i,t}=n_{i,t} \pi_{i,t}$



