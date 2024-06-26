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

func TestMultipleTrees(t *testing.T) {
	forest := NewForest("My First Forest")
	forest.AddTree("Health")
	forest.AddBranch("Health", NewBranch("Diet"))
	forest.AddBranch("Health", NewBranch("Exercise"))
	forest.AddBranch("Health", NewBranch("Sleep"))

	forest.AddTree("Finance")
	forest.AddBranch("Finance", NewBranch("Budget"))
	forest.AddBranch("Finance", NewBranch("Investing"))
	forest.AddBranch("Finance", NewBranch("Retirement"))

	forest.AddTree("Relationships")
	forest.AddBranch("Relationships", NewBranch("Family"))
	forest.AddBranch("Relationships", NewBranch("Friends"))
	forest.AddBranch("Relationships", NewBranch("Romance"))

	forest.AddTree("Business")
	forest.AddBranch("Business", NewBranch("Marketing"))
	forest.AddBranch("Business", NewBranch("Sales"))
	forest.AddBranch("Business", NewBranch("Operations"))

	if len(forest.Trees) != 4 {
		t.Errorf("Expected 4 trees, got %d", len(forest.Trees))
	}

	engine.Log(engine.TraceLevel, " > MultipleTreesTest")
	forest.Log()
}
