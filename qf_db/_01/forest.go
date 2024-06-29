package _01

import (
	"engine"
	"errors"
	"strings"
)

type Forest struct {
	Name         string              `json:"name"`         // equivalent to the name of a database
	Trees        map[string]*Branch  `json:"trees"`        // equivalent to a lookup table in a database
	Distribution map[string][]string `json:"distribution"` // equivalent to a distribution list in a database
}

func NewForest(name string) *Forest {
	return &Forest{
		Name:  name,
		Trees: make(map[string]*Branch),
	}
}

func (f *Forest) addTree(name string) *Branch {
	engine.Log(engine.TraceLevel, " > addTree: %s", name)

	root := NewBranch(name)
	f.Trees[name] = root
	return root
}

func (f *Forest) GetTree(name string) *Branch {
	engine.Log(engine.TraceLevel, " > GetTree: %s", name)

	if tree, ok := f.Trees[name]; ok {
		return tree
	}

	return f.addTree(name)
}

func (f *Forest) RemoveForest(name string) {
	engine.Log(engine.TraceLevel, " > RemoveForest: %s", name)
	delete(f.Trees, name)
}

func (f *Forest) Log() {
	engine.Log(engine.TraceLevel, "Forest: %s", f.Name)

	for _, tree := range f.Trees {
		tree.PrintAll()
	}
}

func (f *Forest) TreeConstructor(absolute_path string) (*Forest, error) {
	paths := strings.Split(absolute_path, "::")
	tree := paths[0]

	// If there's only one path, then we can just create a tree
	if len(paths) == 1 {
		f.GetTree(tree)
		return f, nil
	}

	// We have to have a safety check here to make sure that the first path is a tree
	start := strings.Index(tree, "[")
	end := strings.Index(tree, "]")

	if start > -1 || end > -1 {
		d_start := strings.Index(tree, "(")
		d_end := strings.Index(tree, ")")

		// If we have a declaration we need to split the distribution list and evolve the remaining paths
		if start > -1 || end > -1 {
			distribution_name := tree[start+1 : end][:d_start-1]
			distribution_list := strings.Split(tree[d_start+1:d_end], ",")

			for _, distribution := range distribution_list {
				f.Distribution[distribution_name] = append(f.Distribution[distribution_name], distribution)
				f.GetTree(distribution_name).Evolve(distribution_list)
			}
		} else { // Otherwise, we need to look up the distribution list and evolve the remaining paths
			distribution_name := tree[start+1 : end]
			distribution_list := f.Distribution[distribution_name]

			for _, distribution := range distribution_list {
				f.GetTree(distribution).Evolve(paths[1:])
			}
		}

	}

	start = strings.Index(paths[0], "{")
	end = strings.Index(paths[0], "}")

	if start > -1 && end > -1 {
		trees := strings.Split(paths[0][start+1:end], ",")
		remaining_paths := paths[1:]

		for _, tree := range trees {
			f.GetTree(tree).Evolve(remaining_paths)
		}
	} else {
		f.GetTree(paths[0]).Evolve(paths[1:])
	}

	return f, nil
}

// TODO: Add Test
func (f *Forest) SearchBranches(name string) (*Branch, error) {
	for key, branch := range f.Trees {
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

func (f *Forest) GetBranch(name string) (*Branch, error) {
	if branch, ok := f.Trees[name]; ok {
		return branch, nil
	}
	return nil, errors.New("Branch not found")
}

func (f *Forest) ClimbBranch(branches string) (*Branch, error) {
	keys := strings.Split(branches, "::")
	branch := f.Trees[keys[0]]

	for _, key := range keys {
		branch = branch.Branches[key]
		if branch == nil {
			return nil, errors.New("Branch not found")
		}
	}

	return branch, nil
}
