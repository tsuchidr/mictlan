package ann

import "math/rand/v2"

type Network struct {
	Computer    Computer
	Layers      []*Layer
	Connections []*Connection
}

func NewNetwork(layers []*Layer, computer Computer) *Network {
	network := &Network{Layers: layers, Computer: computer}
	network.ConnectAllLayers()
	return network
}

func (n *Network) ConnectAllLayers() {
	n.Connections = make([]*Connection, 0)
	for i := 0; i < len(n.Layers)-1; i++ {
		n.ConnectLayers(n.Layers[i], n.Layers[i+1])
	}
}

func (n *Network) ConnectLayers(fromLayer, toLayer *Layer) {
	for _, fromNeuron := range fromLayer.Neurons {
		for _, toNeuron := range toLayer.Neurons {
			weight := Number(rand.Float64()*2 - 1) // -1から1の間のランダムな値
			connection := NewConnection(fromNeuron, toNeuron, weight)
			n.Connections = append(n.Connections, connection)
		}
	}
}
