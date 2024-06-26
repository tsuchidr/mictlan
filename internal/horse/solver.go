package horse

type BetRatio int

type Bet struct {
	ticketName TicketName
	names      []Name
	ratio      BetRatio
}

type Solver interface {
	SolveTicket(orm OrderRatesMap, tickets []Ticket) []Bet
}
