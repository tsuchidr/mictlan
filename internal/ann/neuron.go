package ann

type Activation func(Number) Number

type Neuron struct {
	Value      Number
	Bias       Number
	Activation Activation
}

func NewNeuron(value Number, bias Number, activation Activation) *Neuron {
	return &Neuron{value, bias, activation}
}

func NewNeurons(count int, bias Number, activation Activation) []*Neuron {
	neurons := make([]*Neuron, count)
	for i := 0; i < count; i++ {
		neurons[i] = NewNeuron(0, bias, activation)
	}
	return neurons
}
