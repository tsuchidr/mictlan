package horse

type Name string
type Pedigree string
type Jockey string
type BodyWeight float32
type AssignedWeight float32

type Info struct {
	name           Name
	pedigree       Pedigree
	jockey         Jockey
	bodyWeight     BodyWeight
	assignedWeight AssignedWeight
}

func NewInfo(
	name Name,
	pedigree Pedigree,
	jockey Jockey,
	bodyWeight BodyWeight,
	assignedWeight AssignedWeight,
) Info {
	return Info{name, pedigree, jockey, bodyWeight, assignedWeight}
}

type OrderRates []float32
type OrderRatesMap map[Name]OrderRates

type AI interface {
	PredictOrderRates(input []Info) OrderRatesMap
}
