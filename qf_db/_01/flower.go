package _01

type Flower struct {
	Name string "json:'name'" 	// Absolute path to the bucket
	Units []*Unit 				// List of units in the bucket
	Flowered bool 				// Whether the bucket has been flowered
}


func (f *Flower) Pedals() []interface{} {
	values := make([]interface{}, len(f.Units))
	
	for i, u := range f.Units {
		values[i] = u.Value
	}

	return values
}

func (f *Flower) RemoveUnit(index int) {
	f.Units = append(f.Units[:index], f.Units[index+1:]...)
}

func (f *Flower) GetUnit(index int) *Unit {
	return f.Units[index]
}

func (f *Flower) GetUnitByName(name string) []*Unit {
	units := make([]*Unit, 0)
	for _, u := range f.Units {
		if u.Name == name {
			units = append(units, u)
		}
	}
	return units
}

func (f *Flower) FindUnit(name string, hash string, size int) *Unit {
	for _, u := range f.Units {
		if u.Name == name && u.Size == size && u.Hash == hash {
			return u
		}
	}
	return nil
}

func (f *Flower) AddUnit(u *Unit) {
	f.Units = append(f.Units, u) // We're going to have to check for duplicate names
}

func NewFlower(name string) *Flower {
	return &Flower{
		Name: name,
	}
}
