package _01

import (
	"engine"
	. "fmt"
	"testing"
)

engine.InitLogger(engine.Config{
	Filename:    "../log.txt",
	MinLogLevel: engine.TraceLevel,
	ToConsole:   true,
})

func TestNewBranch(t *testing.T) {
	b := NewBranch("test")
	if b.Name != "test" {
		t.Errorf("Expected name to be 'test', got %s", b.Name)
	}
	engine.Log(engine.DebugLevel, " > NewBranchTest")
	engine.Log(engine.DebugLevel, "Branch: %v", b)
	engine.Log(engine.DebugLevel, " ")
}

func TestAddBranch(t *testing.T) {
	b := NewBranch("test")
	b.AddBranch(NewBranch("test2"))
	b.AddBranch(NewBranch("test1"))
	if b.Next["test2"] == nil {
		t.Error("Expected branch to be added")
	}
	Println(" > AddBranchTest")
	b.PrintAll()
	Println(" ")
}

func TestGetBranch(t *testing.T) {
	b := NewBranch("test")
	test1 := NewBranch("test1")
	test2 := NewBranch("test2")
	nested := NewBranch("nested")
	b.AddBranch(test1)
	b.AddBranch(test2)
	test2.AddBranch(nested)

	branch, err := b.GetBranch("test2")
	if err != nil {
		t.Error("Expected branch to be found")
	}
	if branch.Name != "test2" {
		t.Errorf("Expected name to be 'test2', got %s", branch.Name)
	}
	Println(" > GetBranchTest")
	branch.PrintAll()
	Println(" ")
}

func TestRemoveBranch(t *testing.T) {
	b := NewBranch("test")
	test1 := NewBranch("test1")
	test2 := NewBranch("test2")
	nested := NewBranch("nested")
	b.AddBranch(test1)
	b.AddBranch(test2)
	test2.AddBranch(nested)
	if b.Next["test"] != nil {
		t.Error("Expected branch to be removed")
	}
	Println(" > RemoveBranchTest")
	b.PrintAll()
	Println(" ")
}

func TestCutBranch(t *testing.T) {
	b := NewBranch("test")
	test1 := NewBranch("test1")
	test2 := NewBranch("test2")
	nested := NewBranch("nested")
	b.AddBranch(test1)
	b.AddBranch(test2)
	test2.AddBranch(nested)
	b.Cut("test2")
	if b.Next["test2"] != nil {
		t.Error("Expected branch to be pruned")
	}
	Println(" > PruneBranchTest")
	b.PrintAll()
	Println(" ")
}

func TestBranchFlower(t *testing.T) {
	b := NewBranch("test")
	b.AddFlower(NewFlower("test1"))
	b.AddFlower(NewFlower("test2"))
	if b.Flower["test1"] == nil {
		t.Error("Expected flower to be added")
	}
	Println(" > AddFlowerTest")
	b.PrintAll()
	Println(" ")
}
