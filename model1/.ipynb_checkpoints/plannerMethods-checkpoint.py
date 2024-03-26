#incrementAndSubstitutions = 'zero', 'random', 'total', 'proportionally' # to be accorded with the name of the folder in the experiments
incrementAndSubstitutions = 'proportionally'

#askingMaxInvGoodsProduction = 'min', 'regular', 'max' # to be accorded with the name of the folder in the experiments -> PropMin, PropMax
# relevant only under the case of incrementAndSubstitutions = 'proportionally' 
askingInvGoodsProduction = 'max' # OR 'regular' (basic option) OR 'min' OR 'max'
investmentVariation= 2 # used directly if max and as (1/investmentVariation) if min

##################################################
#order generation (alternatively)
noOrderGeneration=False
randomOrderGeneration=True
