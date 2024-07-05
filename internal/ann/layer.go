package ann

type Layer struct {
	Neurons []*Neuron
}

func NewLayer(neurons []*Neuron) *Layer {
	return &Layer{Neurons: neurons}
}
