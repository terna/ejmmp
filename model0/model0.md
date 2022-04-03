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

$q_{i,t}$ - production in quantity, `production`

$\Pi_{i,t}$ - profit, `profit`

$w$ - wage `wage`

$r_{i,t}$ - revenues, `revenues`

$s_{i,t}$ - sales, `sales`

$T$ - number of cycles `ncycles`

$t$ -cycle `cycle`

### 

### agent structure

Here we have the structure of a generic agent: it can represent and employer, a worker, an unemployed person.

When an agent is created, the initialization process defines:

- its numerical id, `num`

- its employer status, `employer`, setting it to $false$
- the id of its employer, `myEmployer`, setting it to $0$
- 