package _01

import (
	"strings"
	"errors"

)

type Forest struct {
	Name string "json:'name'" 		// equivalent to the name of a database
	Trees map[string][]Branch 	// equivalent to a table in a database
}

func NewForest(name string) *Forest {
	return &Forest{
		Name: name,
		Trees: make(map[string][]Branch),
	}
}

func (f *Forest) AddTree(name string) {
	f.Trees[name] = make([]Branch, 0)
}

func (f *Forest) GetTree(name string) []Branch {
	return f.Trees[name]
}

func (f *Forest) RemoveTree(name string) {
	delete(f.Trees, name)
}

func (f *Forest) AddBranch(name string, b Branch){
	f.Trees[name] = append(f.Trees[name], b)
}

func (f *Forest) GrowBranch(name string) {
	f.Trees[name] = append(f.Trees[name], Branch{})
}

func (f *Forest) Prune(name string) {
	f.Trees[name] = make([]Branch, 0)
}

func (f *Forest) ClimbBranch(name string, branches string) (*Branch, error) {
	keys := strings.Split(branches, "::")
	branch, ok := f.Trees[name]
	var next_branch *Branch

	if !ok {
		return nil, errors.New("Tree not found")
	}

	for _, key := range keys {
		found := false
		for _, b := range branch {
			if b.Name == key {
				next_branch = &b
				found = true
				break
			}
		}
		if !found {
			return nil, errors.New("Branch not found")
		}
	}

	return next_branch, nil
}

func (f *Forest) GetBranch(name string) []Branch {
	return f.Trees[name]
}