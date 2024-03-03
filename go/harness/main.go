// main.go
package main

import (
	"fmt"
	"github.com/Unleash/unleash-client-go/v4"
	"github.com/Unleash/unleash-client-go/v4/context"
	"net/http"
	"os"

	"bufio"
	"encoding/json"
	"io"
	"strings"
)

type Test struct {
	Description    string          `json:"description"`
	Context        context.Context `json:"context"`
	ToggleName     string          `json:"toggleName"`
	ExpectedResult bool            `json:"expectedResult"`
}

type TestData struct {
	Tests []Test `json:"tests"`
}

func init() {
	unleashURL := os.Getenv("UNLEASH_API_URL")
	if unleashURL == "" {
		unleashURL = "http://localhost:4242/api/"
	}

	unleash.Initialize(
		unleash.WithListener(&unleash.DebugListener{}),
		unleash.WithAppName("my-application"),
		unleash.WithUrl(unleashURL),
		unleash.WithCustomHeaders(http.Header{"Authorization": {"<API token>"}}),
	)

	unleash.WaitForReady()
}

func main() {
	reader := bufio.NewReader(os.Stdin)
	var inputBuilder strings.Builder
	for {
		input, err := reader.ReadString('\n')
		inputBuilder.WriteString(input)
		if err != nil {
			if err == io.EOF {
				break
			}
			fmt.Printf("Error reading input: %v\n", err)
			return
		}
	}
	jsonInput := inputBuilder.String()

	var testData TestData
	if err := json.Unmarshal([]byte(jsonInput), &testData); err != nil {
		fmt.Printf("Error parsing JSON input: %v\n", err)
		return
	}

	results := make(map[string]interface{})

	for _, test := range testData.Tests {
		isEnabled := unleash.IsEnabled(test.ToggleName, unleash.WithContext(test.Context))
		fmt.Printf("Test: %s, Expected: %v, Result: %v\n", test.Description, test.ExpectedResult, isEnabled)
		results[test.Description] = map[string]interface{}{
			"toggleName":   test.ToggleName,
			"actualResult": isEnabled,
			"context":      test.Context,
		}
	}

	jsonResult, err := json.MarshalIndent(results, "", "    ")
	if err != nil {
		fmt.Println("Error marshaling results to JSON:", err)
		return
	}

	fmt.Println(string(jsonResult))
}