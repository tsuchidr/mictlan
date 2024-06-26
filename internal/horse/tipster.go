package horse

type Odds float32

// PredictOrder は各チケットで当てる順位のリスト
type PredictOrder []int

type TicketName string

type Ticket struct {
	name  TicketName
	order PredictOrder
	odds  Odds
}

type TipsterInput struct {
	tickets []Ticket
	infos   []Info
}

type Tipster struct {
	ai     AI
	solver Solver
}

func (t *Tipster) decide(i TipsterInput) []Bet {
	orm := t.ai.PredictOrderRates(i.infos)
	return t.solver.SolveTicket(orm, i.tickets)
}
