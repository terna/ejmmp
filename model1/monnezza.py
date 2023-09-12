    def receivingNewOrder(self, productionOrder:float):
        self.dealingMovAvElements(self.orderObservationFrequency, productionOrder)
        
        #decision on accepting or refusing the new order
        productionOrderQuantityByPeriod=productionOrder/self.duration
        requiredLabor=np.ceil(productionOrderQuantityByPeriod/self.laborProductivity)
        requiredCapital=requiredLabor*self.recipe
        
        #create a new aPP or skip the order
        if requiredLabor <= self.labor and requiredCapital <= self.capital: 
            aProductiveProcess = ProductiveProcess(productionOrderQuantityByPeriod, \
                                                   requiredLabor, requiredCapital, self.duration)
            self.appRepository.append(aProductiveProcess)
        
        

    def produce(self)->tuple: 
        
        self.totalCostOfProductionOrder=0
        self.output=0
        self.costOfUnusedFactors=0
        self.totalLostProduction=0
        self.totalCostOfLostProduction=0
        
        for aProductiveProcess in self.appRepository:  
            
            if aProductiveProcess.hasResources or \
            (self.availableLabor >= aProductiveProcess.requiredLabor and\
                self.availableCapital >= aProductiveProcess.requiredCapital):
                
                if not aProductiveProcess.hasResources: #first cycle dealing the aPP (gets resources if not available)
                    self.availableLabor -= aProductiveProcess.requiredLabor
                    self.availableCapital -= aProductiveProcess.requiredCapital
                    aProductiveProcess.hasResources = True 
                    
                #production
                (aPPoutputOfThePeriod, requiredLabor, requiredCapital, lostProduction, costOfLostProduction)=\
                aProductiveProcess.step()
                #aProductiveProcess.step(productionOrder)
                     
                self.output += aPPoutputOfThePeriod
                
                cost = requiredLabor*params['wage'] + requiredCapital*params['costOfCapital']
                self.totalCostOfProductionOrder += cost
                
                self.totalLostProduction += lostProduction
                self.totalCostOfLostProduction += costOfLostProduction
              
        
                if aProductiveProcess.failure:
                    self.inProgressInventories -= cost*(aProductiveProcess.productionClock-1)
                
                else:
                    if aProductiveProcess.productionClock < aProductiveProcess.duration:
                        self.inProgressInventories += cost
                    else:
                        self.inventories+=cost*self.duration
                        self.inProgressInventories -= cost*(self.duration-1)

        self.costOfUnusedFactors =  self.availableLabor*params['wage'] + \
                                    self.availableCapital*params['costOfCapital']
        
        self.totalCostOfLabor= self.labor*params['wage']
        self.totalCostOfCapital=self.capital*params['costOfCapital']
        
        
        if t() % self.orderObservationFrequency==0:
            #print("ORDER MOV AV",self.uid, sum(self.movAvElements)/ len(self.movAvElements), flush=True)
            requiredLabor=ceil(sum(self.movAvElements)/ len(self.movAvElements))
            requiredCapital=requiredLabor*self.recipe
            
            if self.labor > (1+params['tollerance']) * requiredLabor:
                self.labor = int((1+params['tollerance']) * requiredLabor)
            if self.labor < (1/(1+params['tollerance'])) * requiredLabor:
                self.labor = int((1/(1+params['tollerance'])) * requiredLabor)
            #print(self.uid, "L", self.labor, flush=True)
       
        if self.capital >(1+params['tollerance']) * requiredCapital: #no substitution of the machinery
                self.capital *= (1 - 1/(self.assetsUsefulLife * params['timeFraction']))              
        else: #subtstitution #if substitution occurs, then add its cost
            self.totalCostOfCapital += self.capital * 1/(self.assetsUsefulLife * params['timeFraction']) 
        #print(self.uid, "K", self.capital, flush=True)
        
        # NB solo messo sostituzioni, serve l'aumento, come per il lavoro
            
                
            
        # remove concluded aPPs from the list
        for i in range(len(self.appRepository)-1,-1,-1):
            if self.appRepository[i].productionClock == self.appRepository[i].duration: 
                self.availableLabor+=self.appRepository[i].requiredLabor
                self.availableCapital+=self.appRepository[i].requiredCapital
                #self.appRepository.remove(aProductiveProcess)
                del self.appRepository[i]

        
        #print(self.uid,"\n", productionOrder,  self.labor, self.capital, self.recipe,\
              #self.laborProductivity,self.duration,"\n",\
              #output, self.totalCostOfProductionOrder, self.costOfUnusedFactors, self.inventories,\
              #self.inProgressInventories, self.totalLostProduction,self.totalCostOfLostProduction, flush=True)
        
        return(self.output, self.totalCostOfProductionOrder, self.costOfUnusedFactors,self.inventories,\
               self.inProgressInventories, self.totalLostProduction, self.totalCostOfLostProduction)
