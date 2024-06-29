package _01

import (
	"engine"
	"errors"
	"strings"
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
	engine.Log(engine.TraceLevel, " > GetTree: %s", name)
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

func (f *Forest) TreeConstructor(absolute_path string) (*Forest, error) {
	paths := strings.Split(absolute_path, "::")

	// We have to have a safety check here to make sure that the first path is a tree
	start := strings.Index(paths[0], "[")
	end := strings.Index(paths[0], "]")

	if start > -1 || end > -1 {
		return f, errors.New("TreeConstructor: Tree's cannot start with a distribution list. Try using forking instead e.g. '{a, b}'")
	}

	start = strings.Index(paths[0], "{")
	end = strings.Index(paths[0], "}")

	if start > -1 && end > -1 {
		trees := strings.Split(paths[0][start+1:end], ",")
		remaining_paths := paths[1:]

		for _, tree := range trees {
			f.GetTree(tree).Evolution(remaining_paths)
		}
	} else {
		f.GetTree(paths[0]).Evolution(paths[1:])
	}

	return f, nil
}
