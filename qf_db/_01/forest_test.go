package _01

import (
	"testing"
)

func TestAbstractForest(t *testing.T) {
	f, err := NewForest("test_forest").TreeConstructor("simple::nested::branches")

	if err != nil {
		t.Errorf("Expected no error, got %s", err)
	}

	if f.Name != "test_forest" {
		t.Errorf("Expected name to be 'test_forest', got %s", f.Name)
	}

	if len(f.Trees) != 1 {
		t.Errorf("Expected 1 tree, got %d", len(f.Trees))
	}

	tree := f.GetTree("simple")
	tree.Log()
	if tree.Name != "simple" {
		t.Errorf("Expected name to be 'simple', got %s", tree.Name)
	}

	if len(tree.Branches) != 1 {
		t.Errorf("Expected 1 branch, got %d", len(tree.Branches))
	}

}
