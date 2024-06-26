package main

import (
	"fmt"
	"engine"
)

func main() {
	err := engine.InitLogger(engine.Config{
		Filename:    "log.txt",
		MinLogLevel: engine.TraceLevel,
		ToConsole:   true,
	})

	if err != nil {
		fmt.Println(err)
		return
	}

	defer engine.Close()

	engine.Log(engine.TraceLevel, " > CompressStringTest")
	engine.Log(engine.TraceLevel, "Compressed: %s", "String")
}
