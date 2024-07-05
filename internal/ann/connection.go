package ann

type Number float64

type Connection struct {
	From   *Neuron
	To     *Neuron
	Weight Number
}

func NewConnection(from *Neuron, to *Neuron, weight Number) *Connection {
	return &Connection{from, to, weight}
}
