package main

import (
	"_01"
	"engine"
)

func main() {
	// We first want to delete the log file if it exists, but we won't want to do this in production
	engine.NewFile("log.txt")
	err := engine.InitLogger(engine.DefaultConfig)

	if err != nil {
		engine.Log(engine.ErrorLevel, "Error initializing logger: %v", err)
		return
	}

	defer engine.Close()

	forest := _01.NewForest("forest")
	forest.PopulateBranches("health::workout::arms::pushups")
	forest.PopulateBranches("health::workout::arms::pullups")
	forest.PopulateBranches("health::workout::core::situps")
	forest.PopulateBranches("health::workout::lower::squats") // TODO: Fix this where we can have {lower,core, legs}
	forest.PopulateBranches("health::workout::lower::lunges")
	forest.PopulateBranches("health::workout::whole::burpees")    // TODO: Fix this where we can have {whole,upper,lower,core,legs,arms}
	forest.PopulateBranches("health::workout::upper::planks")     // TODO: Fix this where we can have {upper,core,arms}
	forest.PopulateBranches("health::workout::mountain climbers") //       .. or rather allow for a branch to be linked to multiple other branches e.g. `upper` -> `arms` and `core`
	forest.PopulateBranches("health::workout::whole::jumping jacks")
	forest.PopulateBranches("health::workout::lower::flutter kicks")

	forest.PopulateBranches("health::diet::breakfast")
	forest.PopulateBranches("health::diet::lunch")
	forest.PopulateBranches("health::diet::dinner")
	forest.PopulateBranches("health::diet::snacks")

	forest.PopulateBranches("health::mental::meditation")
	forest.PopulateBranches("health::mental::reading") // This needs to be able to link to education tree {health::mental, education}::reading

	forest.PopulateBranches("education::reading")
	forest.PopulateBranches("education::writing")
	forest.PopulateBranches("education::math")
	forest.PopulateBranches("education::science")

	forest.PopulateBranches("finance::budgeting")
	forest.PopulateBranches("finance::investing")
	forest.PopulateBranches("finance::saving")

	forest.PopulateBranches("relationships::family")
	forest.PopulateBranches("relationships::friends")
	forest.PopulateBranches("relationships::romantic")

	forest.Log()
}
