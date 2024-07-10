package _01

import (
	"engine"
)

// Parent -> It can have a fork or a distribution
type Seed struct {
	name          string
	forks         []Seed
	distributions []string // List of Names for groupings of forks
}

func (s *Seed) AddDistribution(dist string, forks []string) {
	s.distributions = append(s.distributions, dist)
	for _, fork := range forks {
		s.AddFork(fork)
	}
}

func (s *Seed) AddFork(fork_str string) {
	fork := Seed{fork_str, nil, nil}
	s.forks = append(s.forks, fork)
}

func UnwrapPath(path string) (string, error) {
	engine.Log(engine.DebugLevel, "Unwrapping path: %v", path)

	// We need to check all distributions and Forks

	return path, nil
}
