package _01

import (
	"engine"
	"testing"
)

func TestUnwrapPath(t *testing.T) {
	path := "parent::child::grandchild"
	_, err := UnwrapPath(path)
	if err != nil {
		t.Error("Expected path to be unwrapped")
	}
	engine.Log(engine.DebugLevel, " > UnwrapPathTest")
	engine.Log(engine.DebugLevel, "Path: %v", path)
	engine.Log(engine.DebugLevel, " ")
}
