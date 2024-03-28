#incrementAndSubstitutions = 'zero', 'random', 'total', 'proportionally' # to be accorded with the name of the folder in the experiments
incrementAndSubstitutions = 'proportionally'

#askingMaxInvGoodsProduction = 'min', 'regular', 'max' # to be accorded with the name of the folder in the experiments -> PropMin, PropMax
# relevant only under the case of incrementAndSubstitutions = 'proportionally' 
askingInvGoodsProduction = 'max' # OR 'regular' (basic option) OR 'min' OR 'max'

investmentVariation= 0.1 # positive or negative in (-1,+1) 
#used as 1+investmentVariation for the cases 'min'(must be negative) or 'max' (must be positive)

#################################################
#order generation (alternatively)
noOrderGeneration=False
randomOrderGeneration=True

durationCoeff=2