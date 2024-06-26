package horse

import "testing"

type MockAI struct {
}

func (m MockAI) PredictOrderRates(input []Info) OrderRatesMap {
	//TODO implement me
	panic("implement me")
}

func NewMockAI() AI {
	return &MockAI{}
}

func TestAI(t *testing.T) {
	ai := NewMockAI()
	var input []Info
	for i := 0; i < 10; i++ {
		input = append(input, NewInfo("", "", "", 1.1, 1.1))
	}
	r := ai.PredictOrderRates(input)
	t.Log(r)
}
