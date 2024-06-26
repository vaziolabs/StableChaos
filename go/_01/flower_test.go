package _01

import (
	"testing"
	. "fmt"
)

func TestNewFlower(t *testing.T) {
	f := NewFlower("test")
	if f.Name != "test" {
		t.Errorf("Expected name to be 'test', got %s", f.Name)
	}
	Println(" > NewFlowerTest")
	Println(f)
	Println(" ")
}

func TestAddFlower(t *testing.T) {
	b := NewBranch("test")
	f := NewFlower("test")
	b.AddFlower(f)
	if b.Flower["test"] == nil {
		t.Error("Expected flower to be added")
	}
	Println(" > AddFlowerTest")
	b.PrintAll()
	Println(" ")
}

func TestRemoveFlower(t *testing.T) {
	b := NewBranch("test")
	f := NewFlower("test")
	b.AddFlower(f)
	b.RemoveFlower(f.Name)
	if b.Flower["test"] != nil {
		t.Error("Expected flower to be removed")
	}
	Println(" > RemoveFlowerTest")
	b.PrintAll()
	Println(" ")
}


func TestGetFlower(t *testing.T) {
	b := NewBranch("test")
	f := NewFlower("test")
	b.AddFlower(f)
	flower := b.GetFlower("test")
	if flower == nil {
		t.Error("Expected flower to be found")
	}
	if flower.Name != "test" {
		t.Errorf("Expected name to be 'test', got %s", flower.Name)
	}
	Println(" > GetFlowerTest")
	b.PrintAll()
	Println(" ")
}