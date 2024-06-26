package _01

import (
	"testing"
	. "fmt"
)

func TestNewForest(t *testing.T) {
	f := NewForest("test_forest")
	if f.Name != "test_forest" {
		t.Errorf("Expected name to be 'test', got %s", f.Name)
	}
	Println(" > NewForestTest")
	Println(f)
	Println(" ")
}