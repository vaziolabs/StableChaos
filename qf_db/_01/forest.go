package _01

import (
	"engine"
)

type Forest struct {
	Name  string           `json:"name"`  // equivalent to the name of a database
	Trees map[string]*Tree `json:"trees"` // equivalent to a lookup table in a database
}

func NewForest(name string) *Forest {
	return &Forest{
		Name:  name,
		Trees: make(map[string]*Tree),
	}
}

func (f *Forest) addTree(name string) *Tree {
	plant_tree := NewTree(name)
	f.Trees[name] = plant_tree
	return plant_tree
}

func (f *Forest) GetTree(name string) *Tree {
	if tree, ok := f.Trees[name]; ok {
		return tree
	}
	return f.addTree(name)
}

func (f *Forest) RemoveTree(name string) {
	delete(f.Trees, name)
}

func (f *Forest) Log() {
	engine.Log(engine.InfoLevel, "Forest: %s", f.Name)
	for _, tree := range f.Trees {
		tree.Log()
	}
}
