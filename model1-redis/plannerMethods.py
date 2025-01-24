#incrementAndSubstitutions = 'zero', 'random', 'total', 'proportionally' # to be accorded with the name of the folder in the experiments
incrementAndSubstitutions = 'proportionally'

#askingMaxInvGoodsProduction = 'min', 'regular', 'max' # to be accorded with the name of the folder in the experiments -> PropMin, PropMax
# 'min' or 'max' to be used ONLY under the case of incrementAndSubstitutions = 'proportionally' 
askingInvGoodsProduction = 'regular' # 'regular' (basic option) OR 'min' OR 'max'

investmentVariation= 0.8 # positive or negative in (-1,+1) 
#used as 1+investmentVariation for the cases 'min' (must be negative) or 'max' (must be positive)

#################################################
#order generation (alternatively)
noOrderGeneration=False
randomOrderGeneration=False
externalOrderGeneration=True

#################################################
#modify duration
durationCoeff=1