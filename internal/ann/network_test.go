package ann

import (
	"math"
	"testing"
)

type MockComputer struct {
}

func NewMockComputer() Computer {
	return MockComputer{}
}

func TestNetwork(t *testing.T) {
	// 活性化関数（この例ではシグモイド関数）を定義
	sigmoid := func(x Number) Number {
		return Number(1 / (1 + math.Exp(-float64(x))))
	}

	// レイヤーを作成
	inputLayer := NewLayer(NewNeurons(28*28, 0, sigmoid))
	hiddenLayer1 := NewLayer(NewNeurons(16, 0.1, sigmoid))
	hiddenLayer2 := NewLayer(NewNeurons(16, 0.1, sigmoid))
	outputLayer := NewLayer(NewNeurons(10, 0.3, sigmoid))

	// ネットワークを作成
	computer := NewMockComputer()
	network := NewNetwork([]*Layer{inputLayer, hiddenLayer1, hiddenLayer2, outputLayer}, computer)

	// テスト: レイヤー数が正しいか
	if len(network.Layers) != 4 {
		t.Errorf("Expected 3 layers, got %d", len(network.Layers))
	}

	// テスト: ニューロン数が各レイヤーで正しいか
	if len(network.Layers[0].Neurons) != 784 {
		t.Errorf("Expected 784 neurons in input layer, got %d", len(network.Layers[0].Neurons))
	}
	if len(network.Layers[1].Neurons) != 16 {
		t.Errorf("Expected 16 neurons in hidden layer, got %d", len(network.Layers[1].Neurons))
	}
	if len(network.Layers[2].Neurons) != 16 {
		t.Errorf("Expected 16 neurons in hidden layer, got %d", len(network.Layers[1].Neurons))
	}
	if len(network.Layers[3].Neurons) != 10 {
		t.Errorf("Expected 10 neuron in output layer, got %d", len(network.Layers[2].Neurons))
	}

	// テスト: コネクション数が正しいか
	if len(network.Connections) != 784*16+16*16+16*10 {
		t.Errorf("Expected 6 connections, got %d", len(network.Connections))
	}
}
