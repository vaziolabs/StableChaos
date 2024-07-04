package _01

import (
	"engine"
	"fmt"
	"strings"
)

func UnwrapDeclaration(path string) (string, []string, error) {
	// Distributions are wrapped by [] and distributions declarations are wrapped in ()
	d_start := strings.Index(path, "[")
	d_end := strings.Index(path, "]")

	if d_start > -1 && d_end > -1 {
		distribution := path[d_start+1 : d_end]

		// If there's a distribution declaration
		dd_start := strings.Index(distribution, "(")
		dd_end := strings.Index(distribution, ")")

		if dd_start > -1 && dd_end > -1 {
			declaration := distribution[:dd_start]
			distribution_declaration := distribution[dd_start+1 : dd_end]
			distributions := strings.Split(distribution_declaration, ",")
			return declaration, distributions, nil
		}

		return distribution, []string{}, nil
	}
	return "", []string{}, fmt.Errorf("invalid distribution found: (%s)", path)
}

func UnwrapFork(path string) ([]string, error) {

}

func parseTokens(path string) ([]*Branch, error) {
	tokens := make([]Branch, 0)
	token := ""
	declaration := false

	for _, c := range path {
		branches := make([]Branch, 0)
		
		if c == '{' {
			d := c
			fork := ""
			comma_seen := false

			for d != '}' {
				if d == ',' {
					comma_seen = true
				}

				fork += string(d)
			}

			if !comma_seen {
				return tokens, fmt.Errorf("Invalid Fork found: (%s) must have at least 2 branches.", fork)
			}

			depth++

			forks := strings.Split(fork, ",")

			for _, f := range forks {
				branches, err = UnwrapFork(f)  This is where we would have to parse the rest of the tokens and unwrap them
				
				if err != nil {
					return tokens, err
				}

				for _, b := range branches {
					tokens = append(tokens, b)
				}
			}
		}

		if c == '[' {
			d := c
			distribution := ""
			declared := ""

			for d != ']' {
				peek := d
				peek++

				if d == ':' && peek == ':' {
					return tokens, fmt.Errorf("Invalid Distribution found: (%s) not allowed in Distributions.", distribution)
				}

				if d == '(' {
					declaration = true
					comma_seen := false

					for d != ')' {
						if d == ',' {
							comma_seen = true
						}

						declared += string(d)
					}

					if !comma_seen {
						return tokens, fmt.Errorf("Invalid Distribution Declaration found: (%s) must have at least 2 declarations.", declared)
					}
				} else {
					distribution += string(d)
				}
				// There's a chance tokens could 'fall in' here
			}

			if declaration {
				declarations := strings.Split(declared, ",")
				branch, err := UnwrapDeclaration(distribution, declarations)
				tokens = append(tokens, branch)
			} else {
				// TODO: We need to accept this as a lookup too
				// LookUpDeclaration(distribution)
			}
		}

		if c == ':' {

	}

	tokens = append(tokens, token)
	return tokens, nil
}

func UnwrapChain(path string) ([]string, error) {
	// Chains are separated by ::, but could be nested
	// So we have to unwrap the chains from left to right
	println(path)
	tokens, err := parseTokens(path)

	if err != nil {
		engine.Log(engine.ErrorLevel, "Error parsing tokens: %v", err)
		return tokens, err
	}

	return tokens, err
}
