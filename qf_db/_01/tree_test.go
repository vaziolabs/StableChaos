package _01

import (
	"engine"
	"testing"
)

func TestSearchTree(t *testing.T) {
	tree := NewTree("test")
	if tree.Name != "test" {
		t.Errorf("Expected name to be 'test', got %s", tree.Name)
	}
}

func TestMultipleTrees(t *testing.T) {
	forest := NewForest("My First Forest")

	health_tree := forest.GetTree("Health")
	health_tree.GrowBranch("Diet")
	health_tree.GrowBranch("Exercise")
	health_tree.GrowBranch("Sleep")
	health_tree.Log()

	finance_tree := forest.GetTree("Finance")
	finance_tree.GrowBranches([]string{"Budget", "Investing", "Retirement"})
	engine.Log(engine.InfoLevel, "Finance Tree: %v", finance_tree)

	relationship_tree := forest.GetTree("Relationships")
	relationship_tree.GrowBranches([]string{"Family", "Friends"})
	engine.Log(engine.InfoLevel, "Relationships Tree: %v", relationship_tree)

	business_tree := forest.GetTree("Business")
	business_tree.GrowBranches([]string{"Marketing", "Operations", "Finance"})
	engine.Log(engine.InfoLevel, "Business Tree: %v", business_tree)

	sales := NewBranch("Sales")
	finance_tree.AddBranch("Sales", sales)
	business_tree.AddBranch("Sales", sales)
	engine.Log(engine.InfoLevel, "Sales Branch: %v", sales)

	if len(forest.Trees) != 4 {
		t.Errorf("Expected 4 trees, got %d", len(forest.Trees))
	}

	engine.Log(engine.TraceLevel, " > MultipleTreesTest")
	engine.Log(engine.TraceLevel, " ~~~ Forest ~~~")
	forest.Log()
}

func TestMultipleParents(t *testing.T) {
	forest := NewForest("MultipleParents")

	health_tree := forest.GetTree("Health")
	fitness_branch := health_tree.GrowBranch("Fitness")

	career_tree := forest.GetTree("Career")
	training_branch := career_tree.GrowBranch("Training")

	workout_routing := NewBranch("Workout Routine").AddParents([]*Branch{fitness_branch, training_branch})

	engine.Log(engine.InfoLevel, "Workout Routine: %v", workout_routing)

	if len(workout_routing.Parents) != 2 {
		t.Errorf("Expected 2 parents, got %d", len(workout_routing.Parents))
	}

	engine.Log(engine.TraceLevel, " > MultipleParentsTest")
	forest.Log()
}
