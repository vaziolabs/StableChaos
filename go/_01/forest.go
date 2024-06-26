

type Forest struct {
	Name string "json:'name'" 		// equivalent to the name of a database
	Branches []*Branch 				// list of branches in the forest
}