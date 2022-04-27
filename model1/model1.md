### Stock-flow *model1*, with real and financial elements

- Besides the real part of the economy, we introduce the initial element of the monetary side of the economy.

  

- We are introducing gradually loans, credits, debts, capital stock, interest rate.



- Enterpreneurs have unlimited funds that they put freely in their activities, balancing negative cash if any.

  

- Saving is abstension from consuming, employed in cash.



- Investments are uniquely replacement ones, without technical progress.

  

### symbol table

[symbol table](https://oeis.org/wiki/List_of_LaTeX_mathematical_symbols) in $\LaTeX$ 

$a_i$ -  with $a_i \in \mathbf{A}$; agent number $N=|\mathbf{A}|$, `agentList` and`agentNum`

$a^e_i$ -  with $a^e_i \in \mathbf{A^e}$ and $\mathbf{A^e} \subset \mathbf{A}$; employer number $N^e=|\mathbf{A^e}|$ in range $[N^e_{min},N^e_{max}]$, `employerList`

$\mathbf{F}$ - firms' set, with $f_j \in \mathbf{F}$ being $N^f = |\mathbf{F}|$,  with $N^f = |\mathbf{F}| = |\mathbf{A^e}|$ , `firmList`

$\mathbf{A}^w$ - working agents' set, being $\mathbf{A}^w \subseteq \mathbf{A}$, with $N^w_i=|\mathbf{A}^w_i|$ number of working agents employed by employer $i$, also including self-employed employers, with $a_i \in \mathbf{A}^e$

$\mathbf{B}$ - banks' set, with $b_j \in \mathbf{B}$ being $N^b = |\mathbf{B}|$, `bankList`

$p$ - price `price`

$u$ - unemployment rate `unemploymentRate`

$dimensional~heterogeneity$ is a $true/false$ chooser, forcing increasing firms to attract more workers. `dimensionalHeterogeneity`

$\pi_{i,t}$ - labor productivity, a uniformly distributed decimal number in range $[\pi_{min},\pi_{max}]$,`productivity`

&Delta;$\pi_{i,t}$ - uniperiodal additive productivity correction in range $[$&Delta;$\pi_{min},$ &Delta;$\pi_{max}]$, `productivityDelta`

$n_{i,t}$ - number of workers in a firm, set just in time

$q_{i,t}$ - production in quantity, `production`

$\Pi_{i,t}$ - profit, `profit`

$W$ - wage `wage`

$R_{i,t}$ - revenues, `revenues`

$s_{i,t}$ - sales in quantity, `sales`

$v_{i,t}$ - in**v**entories (final, initial), `initialInventories`, `finalInventories`

$d_{i}$ - deperibility share of the production, `deperibilityShare`, setting $d_{max}$

$c_{i,t}$ - consumption rate, a uniformly distributed decimal number in range $[c_{min},c_{max}]$,`consumptionRate`

$C_{i,t}$ - consumption of $i$ in $t$

$I_{i,t}$  - investment plan  of $i$ in $t$, a uniformly distributed realization in range $[I_{min},I_{max}]$,`investmentProgram`

$H_{i,t}$  - high powered money (cash) held by individuals (also acting as employers), `cashMoney`

$M1_{i,t}$ - checking account money deposits held by  $a_i$ at time $t$, `checkingAccount`

$M1^f_{i,t}$ - firm's bank account (with positive or negative balance), `bankAccount`

the investment and consumption actions are repeated in each cycle, looking around randomly for the sellers; currently `nOfConsumptionActions` $=30$ and `nOfInvestmentActions`$=10$; each consumption buy action is at maximum the 20% of the planned consumptions in that cycle; instead, each investment buy action can reach the whole amount of the investment program of the cycle; each buy action is limited by the residual capabilty of the seller

**magically**, the same good can be a consumption item or an investment one

$T$ - number of cycles `ncycles`

$t$ - cycle `cycle`

### agent structure

The structure of a **generic agent**: it can represent an employer, a worker, an unemployed person.

When an agent is created, the **initialization process** defines:

- its numerical id, `num`

- its employer status, `employer`, set to $false$
- the id of its employer, `myEmployer`, set to $0$
- $R_{i,0}$ - `revenues`, initial value  $0$
- $s_{i,0}$ - `sales`, initial value  $0$
- $v^i_{i,0}$ - inventories, `initialInventories`, set to $0$ 
- $v^f_{i,0}$ - inventories, `finalInventories`, set to $0$ 
- $d_{i}$ - deperibility share, a uniformly distributed decimal number in range $[0,d_{max}]$,`deperibilityShare`
- $c_{i,0}$ - consumption rate, set to $0$
- $I_{i,0}$  - investment plan, set to $0$
- $\Pi_{i,0}$ - profit, set to $0$
- $H_{i,0}$ - cash money, set to $0$ 
- $M1_{i,0}$ - checking account money deposits, set to $0$
- $M1^f_{i,0}$ - firm's bank account, set to $0$

- $\pi_{i,t-1}$ is set after the initialization step, if an agent becomes an employer



each **generic agent** has the **functions**:



- **produce** function, used only if is an employer, with:

  $\pi_{i,t}=\pi_{i,t-1}+$&Delta;$\pi_{i,t}$

  $q_{i,t}=n_{i,t} \pi_{i,t}$

  

- **payWages**

  if employer, pays $W$ to each employee in each time $t$

  &Delta;$M1_{i,t}=W$ for  $a_i \in \mathbf{A}^w$ 

  &Delta;$M1^f_{i,t}=-W \mathbf{N}^w_i$ for $a_i \in \mathbf{A}^e$ 

  

- **buyConsumptionGoods** 

  $C_{i,t}=c_{i,t} (W+\Pi_{i,t-1})$ 	using $\Pi_{i,t-1}$ we introduce a lag with a (possible) cyclical effect

  being $bu$ the buyer and $se$ the seller, for each fraction $C_{i,t}/k$

  &Delta;$M1^f_{se,t}=C_{bu,t}/k$

  &Delta;$M1_{bu,t}=-C_{bu,t}/k$

  

- **buyInvestmentGoods**

  $I_{j,t}$ for $f_j \in \mathbf{F}$  ($I_{j,t}$ is exogenously set)

  being $bu$ the buyer and $se$ the seller, for each fraction $I_{j,t}/k$

  &Delta;$M1^f_{se,t}=I_{bu,t}/k$

  &Delta;$M1^f_{bu,t}=-I_{bu,t}/k$

  

- **makeBalanceSheet**

  $v^f_{i,t}=v^i_{i,t}+q_{i,t}-s_{i,t}-(q_{i,t}-s_{i,t}) d_{i}$

  $R_{i,t}=p s_{i,t}$

  $\Pi_{i,t}=R_{i,t}-W n_{i,t}-p(v^f_{i,t}-v^i_{i,t})$



If an agent becomes an employer, it generates an agent **firm** (to be continued) 



Agent **bank** is a special subject operating on the financial side of the model  (to be continued)



### agent setup

- agent basic creation

  

- creation of employer list

  

- selecting employers

  

- with a given (heterogeneous) productivity

  

- assigning to the employer itself as employee

  

- creation of a temporary workforce list of to-be-employed agent, escluding employers (already self employed)

  

- applying the unmployement rate to exclude agents

  

- assigning workforce (to-be-employed agents) to employers, with a reinforcement mechanism, gradually giving more attraction/hiring capacity to those who grow the most



### meta actions



- *produceAll* orders to the employers to produce and to collects the results

  

- *payWagesAll* orders to the employers to pay wages, also to themselves

  

- *buyConsumptionGoodsAll* orders to the agents to buy investment goodsorder to the employers to buy investment goods

  

- *buyInvestmentGoodsAll* orders to the employers to buy investment goodsorder to the employers to buy investment goods



- *makeBalanceSheetAll* with everyone making accounts



- *accountCashMoney* summraizing eveyone cash money at the end of a cycle



## <p style="color:red">model machine</p>

- a random seed determining the random number sequences



- a list of actions (meta ones)



- an engine excecuting the meta actions



- display tools (their code is hidden into the file `tools.py`)

