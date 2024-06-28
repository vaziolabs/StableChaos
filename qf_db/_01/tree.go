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

func (tree *Tree) Log() {
	engine.Log(engine.DebugLevel, "Tree: %s", tree.Name)
	for _, branch := range tree.Branches {
		branch.PrintAll()
	}
}

////////////////
// Generation //
////////////////

// This will evolve into our query language for the database
func (tree *Tree) Evolution(branches []string) *Tree {
	engine.Log(engine.DebugLevel, " > Evolution: %v", branches)
	root := new(Branch).Prototype().Evolve(branches)
	tree.Branches = root.Next
	return tree
}

func (tree *Tree) AddBranch(name string, b *Branch) *Branch {
	tree.GrowBranch(name)
	b.Root = tree
	return b
}

// This is destructive and will overwrite the branch if it already exists
func (tree *Tree) GrowBranch(name string) *Branch {
	new_branch := NewBranch(name)
	new_branch.Root = tree
	tree.Branches[name] = new_branch
	return new_branch
}

func (tree *Tree) GrowBranches(names []string) *Tree {
	for _, name := range names {
		tree.GrowBranch(name)
	}
	return tree
}

///////////////
// Retrieval //
///////////////

// TODO: Add Test
func (f *Tree) SearchBranches(name string) (*Branch, error) {
	for key, branch := range f.Branches {
		if key == name {
			return branch, nil
		}

		b, e := branch.FindBranch(name)

		if e == nil {
			return b, nil
		}
	}

	return nil, errors.New("Branch not found")
}

func (f *Tree) GetBranch(name string) (*Branch, error) {
	if branch, ok := f.Branches[name]; ok {
		return branch, nil
	}
	return nil, errors.New("Branch not found")
}

func (f *Tree) ClimbBranch(branches string) (*Branch, error) {
	keys := strings.Split(branches, "::")
	branch := f.Branches[keys[0]]

	for _, key := range keys {
		branch = branch.Next[key]
		if branch == nil {
			return nil, errors.New("Branch not found")
		}
	}

	return branch, nil
}
