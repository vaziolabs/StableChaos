package _01

import (
	"engine"
	"testing"
)

func TestNewForest(t *testing.T) {
	f := NewForest("test_forest")
	if f.Name != "test_forest" {
		t.Errorf("Expected name to be 'test', got %s", f.Name)
	}
	engine.Log(engine.DebugLevel, " > NewForestTest")
	engine.Log(engine.DebugLevel, "Forest: %v", f)
	engine.Log(engine.DebugLevel, " ")
}
