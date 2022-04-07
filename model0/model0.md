### Stock-flow *model0*, the real part

- We are considering here uniquely the real part of the economy.

  

- No loans, credits, debts, capital stock, interest rate.



- Enterpreneurs have unlimited funds that they put freely in their activities.

  

- Saving is abstension from consuming.



- Investments are uniquely replacement ones, without technical progress.

  

### symbol table

[symbol table](https://www.caam.rice.edu/~heinken/latex/symbols.pdf) in $\LaTeX$ 

$\mathcal{N}$ - number of agents, `agentNum`

$\mathcal{E}$ - employer number, a uniformly distributed integer number in range $[\mathcal{E}_{min},\mathcal{E}_{max}]$, `employerNum`

$p$ - price `price`

$u$ - unemployment rate `unemploymentRate`

$dimensional~heterogeneity$ is a $true/false$ chooser, forcing increasing firms to attract more workers. `dimensionalHeterogeneity`

$\pi_{i,t}$ - labor productivity, a uniformly distributed decimal number in range $[\pi_{min},\pi_{max}]$,`productivity`

&Delta;$\pi_{i,t}$ - uniperiodal additive productivity correction in range $[$&Delta;$\pi_{min},$ &Delta;$\pi_{max}]$, `productivityDelta`

$n_{i,t}$ - number of workers in a firm, set just in time

$q_{i,t}$ - production in quantity, `production`

$\Pi_{i,t}$ - profit, `profit`

$w$ - wage `wage`

$r_{i,t}$ - revenues, `revenues`

$s_{i,t}$ - sales, `sales`

$v_{i,t}$ - in**v**entories (final, initial), `initialInventories`, `finalInventories`

$d_{i}$ - deperibility share of the production, `deperibilityShare`, setting $d_{max}$

$c_{i,t}$ - consumption rate, a uniformly distributed decimal number in range $[c_{min},c_{max}]$,`consumptionRate`

$C_{i,t}$ - consumption of $i$ in $t$

$I_{i,t}$  - investment plan  of $i$ in $t$, a uniformly distributed realization in range $[I_{min},I_{max}]$,`investmentProgram`

the investment and consumption actions are repeated in each cycle, looking around randomly for the sellers; currently `nOfConsumptionActions` $=30$ and `nOfInvestmentActions`$=10$; each consumption buy action is at maximum the 20% of the planned consumptions in that cycle; instead, each investment buy action can reach the whole amount of the investment program of the cycle; each buy action is limited by the residual capabilty of the seller

magically, the same good can be a consumption item or an investment one

$T$ - number of cycles `ncycles`

$t$ - cycle `cycle`

### 

### agent structure

The structure of a generic agent: it can represent and employer, a worker, an unemployed person.

When an agent is created, the **initialization process** defines:

- its numerical id, `num`

- its employer status, `employer`, set to $false$
- the id of its employer, `myEmployer`, set to $0$
- $r_{i,0}$ - `revenues`, initial value  $0$
- $s_{i,0}$ - `sales`, , initial value  $0$
- $v^i_{i,0}$ - inventories, `initialInventories`, set to $0$ 
- $v^f_{i,0}$ - inventories, `finalInventories`, set to $0$ 
- $d_{i}$ - deperibility share, a uniformly distributed decimal number in range $[0,d_{max}]$,`deperibilityShare`
- $c_{i,0}$ - consumption rate, set to $0$
- $I_{i,0}$  - investment plan, set to $0$
- $\Pi_{i,0}$ - profit, set to 0



we have also a *wallet*, currently unused



each agent has the **functions**:



- **produce** function, used only if is an employer, with:

  $\pi_{i,t}=\pi_{i,t-1}+\Delta\pi_{i,t}$

  $q_{i,t}=n_{i,t} \pi_{i,t}$

  

- **payWages**

  if employer, pays $w$ to each employee in each time $t$

  

- **buyConsumptionGoods** 

  $C_{i,t}=c_{i,t} (w+\Pi_{i,t-1})$ 	using $\Pi_{i,t-1}$ we introduce a lag with a (possible) cyclical effect

  

- **buyInvestmentGoods**

  $I_[i,t]$

  

- **makeBalanceSheet**

  $v^f_{i,t}=v^i_{i,t}+q_{i,t}-s_{i,t}-(q_{i,t}-s_{i,t}) d_{i}$

  $r_{i,t}=p s_{i,t}$

  $\Pi_{i,t}=r_{i,t}-w n_{i,t}-p(v^f_{i,t}-v^i_{i,t})$



@@

### agent setup

