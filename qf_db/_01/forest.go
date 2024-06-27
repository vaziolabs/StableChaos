package _01

import (
	"engine"
	"errors"
	"strings"
)

type Tree struct {
	Name     string             `json:"name"`
	Branches map[string]*Branch `json:"branches"`
}

func NewTree(name string) *Tree {
	return &Tree{
		Name:     name,
		Branches: make(map[string]*Branch),
	}
}

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

func (f *Forest) AddTree(name string) *Tree {
	plant_tree := NewTree(name)
	f.Trees[name] = plant_tree
	return plant_tree
}

func (f *Forest) GetTree(name string) *Tree {
	return f.Trees[name]
}

func (f *Forest) RemoveTree(name string) {
	delete(f.Trees, name)
}

// This will evolve into our query language for the database
func (f *Forest) PopulateBranches(path string) {
	paths := strings.Split(path, "::")
	tree := f.Trees[paths[0]]

	if tree == nil {
		new_tree := NewTree(paths[0])
		f.Trees[paths[0]] = new_tree
		tree = new_tree
	}

	branches := tree.Branches
	for i := 1; i < len(paths); i++ {
		branch_name := paths[i]

		// We need to check if the branch_name is wrapped in curly braces to indicate forking
		if strings.Contains(branch_name, "{") && strings.Contains(branch_name, "}") {
			branch_name = strings.Trim(branch_name, "{}")
			branch_names := strings.Split(branch_name, ",")
		
			for _, name := range branch_names {
				branch := branches[name]

				if branch == nil {
					new_branch := NewBranch(name)
					branches[name] = new_branch
					branch = new_branch
				}
				
		branch := branches[branch_name]

		if branch == nil {
			new_branch := NewBranch(branch_name)
			branches[branch_name] = new_branch
			branch = new_branch
		}

		branches = branch.Next
	}
}

func (f *Forest) AddBranch(name string, b *Branch) {
	f.Trees[name].Branches[b.Name] = b
}

func (f *Forest) GrowBranch(tree_name string, name string) {
	f.Trees[tree_name].Branches[name] = NewBranch(name)
}

func (f *Forest) Prune(name string) {
	f.Trees[name] = NewTree(name)
}

func (f *Forest) ClimbBranch(name string, branches string) (*Branch, error) {
	keys := strings.Split(branches, "::")
	tree, ok := f.Trees[name]
	var next_branch *Branch

	if !ok {
		return nil, errors.New("tree not found")
	}

	for _, key := range keys {
		found := false
		for _, b := range tree.Branches {
			if b.Name == key {
				next_branch = b
				found = true
				break
			}
		}
		if !found {
			return nil, errors.New("branch not found")
		}
	}

	return next_branch, nil
}

func (f *Forest) Log() {
	engine.Log(engine.InfoLevel, "Forest: %s", f.Name)
	for name, tree := range f.Trees {
		engine.Log(engine.InfoLevel, "Tree: %s", name)
		for _, b := range tree.Branches {
			b.PrintAll()
		}
	}
}
