package _01

import (
	"engine"
	"testing"
)

func TestUnwrapDeclaration(t *testing.T) {
	wrapped1 := "[declaration(1,2,3)]"
	unwrapped1, declarations1, err1 := UnwrapDeclaration(wrapped1)
	engine.Log(engine.InfoLevel, "Unwrapped: %s, Declarations: %v, Error: %v", unwrapped1, declarations1, err1)

	if unwrapped1 != "declaration" {
		t.Errorf("Expected 'declaration', got %s", unwrapped1)
	}

	if len(declarations1) != 3 {
		t.Errorf("Expected 3 declarations, got %d", len(declarations1))
	}
}

func TestUnwrapFork(t *testing.T) {
	wrapped2 := "{fork1, fork2}"
	forks2, err2 := UnwrapFork(wrapped2)
	engine.Log(engine.InfoLevel, "Forks: %v, Error: %v", forks2, err2)

	if len(forks2) != 2 {
		t.Errorf("Expected 2 forks, got %d", len(forks2))
	}
}

func TestUnwrapChain(t *testing.T) {
	wrapped3 := "chain1::{fork1,fork2}::[distribution1(d1,d2)]::{fork3,fork4::[distribution2(chain3,chain4)]}::leaf_node"
	chains3, err3 := UnwrapChain(wrapped3)
	engine.Log(engine.InfoLevel, "Chains: %v, Error: %v", chains3, err3)

	if len(chains3) != 5 {
		t.Errorf("Expected 5 chains, got %d", len(chains3))
	}
}
