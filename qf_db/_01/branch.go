package _01

import (
	"engine"
	"fmt"
)

type Branch struct {
	Name         string              `json:"name"`          // equivalent to the name of a table in a database
	Next         map[string]*Branch  `json:"forks"`         // These are Forks in the branch
	Distribution map[string][]string `json:"distributions"` // These are the branches that are distributed from this branch
	Parents      []*Branch           `json:"parents"`       // These are the branches that lead to this branch
	Flower       map[string]*Flower  `json:"flowers"`       // These are the leaves in the branch
}

func (b *Branch) PrintAll() {
	engine.Log(engine.DebugLevel, "Branch: %v", b)
	for _, branch := range b.Next {
		branch.PrintAll()
	}
	for _, flower := range b.Flower {
		engine.Log(engine.DebugLevel, "Flower: %v", flower)
	}
}

func (b *Branch) Traverse(keys []string) (*Branch, error) {
	if len(keys) == 0 {
		return b, nil
	}
	next, err := b.GetBranch(keys[0])
	if err != nil {
		return nil, err
	}
	return next.Traverse(keys[1:])
}

func (b *Branch) GrowBranch(key string) *Branch {
	new_branch := NewBranch(key)
	new_branch.Parents = append(new_branch.Parents, b)
	b.Next[key] = new_branch
	return new_branch
}

func (b *Branch) AddBranch(branch *Branch) *Branch {
	branch.Parents = append(branch.Parents, b)
	b.Next[branch.Name] = branch
	return branch
}

func (b *Branch) GetBranch(name string) (*Branch, error) {
	if branch, ok := b.Next[name]; ok {
		return branch, nil
	}
	return nil, fmt.Errorf("Branch %s not found", name)
}

// This clears the branch and all its children so there's no fragments - Maybe this is a bit too much? I need proof either way
func (b *Branch) Clear() {
	for _, branch := range b.Next {
		branch.Clear()
		delete(b.Next, branch.Name)
	}

	b.Next = make(map[string]*Branch)
	b.Flower = make(map[string]*Flower)
}

// This actually removes the branch but leaves any potential children
func (b *Branch) Cut(name string) {
	b.Next[name].Clear()
	delete(b.Next, name)
}

// This scrapes all the values off the branch
func (b *Branch) PruneAll() {
	for _, branch := range b.Next {
		branch.PruneAll()
	}

	for _, flower := range b.Flower {
		delete(b.Flower, flower.Name)
	}
}

func (b *Branch) Prune(name string) {
	b.Next[name].PruneAll()
}

func (b *Branch) RemoveBranch(branch Branch) {
	delete(b.Next, branch.Name)
}

func (b *Branch) GrowFlower(name string) *Flower {
	// Check if the flower already exists
	if flower, ok := b.Flower[name]; ok {
		return flower
	}
	new_flower := NewFlower(name)
	b.Flower[name] = new_flower
	return new_flower
}

func (b *Branch) AddFlower(flower *Flower) {
	b.Flower[flower.Name] = flower
}

func (b *Branch) RemoveFlower(name string) {
	delete(b.Flower, name)
}

func (b *Branch) GetFlower(name string) *Flower {
	return b.Flower[name]
}

func NewBranch(name string) *Branch {
	return &Branch{
		Name:   name,
		Next:   make(map[string]*Branch),
		Flower: make(map[string]*Flower),
	}
}
