using System;
using Newtonsoft.Json;
using System.Collections.Generic;
using Unleash;
using Unleash.ClientFactory;

class Test
{
    public Test(string description, UnleashContext context, string toggleName, bool expectedResult)
    {
        Description = description;
        Context = context;
        ToggleName = toggleName;
        ExpectedResult = expectedResult;
    }

    public string Description { get; set; }
    public UnleashContext Context { get; set; }
    public string ToggleName { get; set; }
    public bool ExpectedResult { get; set; }
}

class Program
{

    static async Task Main(string[] args)
    {
        await MainAsync(args);
    }

    static async Task MainAsync(string[] args)
    {
        string input = await Console.In.ReadToEndAsync();

        var data = JsonConvert.DeserializeObject<Dictionary<string, List<Test>>>(input);


        var settings = new UnleashSettings()
        {
            AppName = "dotnet-test",
            UnleashApi = new Uri("http://seidr-core:4242/api/"),
            CustomHttpHeaders = new Dictionary<string, string>()
            {
            {"Authorization","Test" }
            }
        };
        var unleashFactory = new UnleashClientFactory();

        IUnleash unleash = await unleashFactory.CreateClientAsync(settings, synchronousInitialization: true);

        if (data.TryGetValue("tests", out var tests))
        {
            foreach (var test in tests)
            {

                // print out the toggle name and context
                Console.WriteLine($"ToggleName: {test.ToggleName}, Context: {test.Context}");

                var awesome = unleash.IsEnabled(test.ToggleName, test.Context);
                Console.WriteLine($"Result {awesome}");

                while (awesome != test.ExpectedResult)
                {
                    Console.WriteLine("Waiting for the toggle to be enabled");
                    await Task.Delay(1000);
                    awesome = unleash.IsEnabled(test.ToggleName, test.Context);
                    Console.WriteLine($"Result {awesome}");
                }

                // Console.WriteLine($"ToggleName: {test.ToggleName}");
                // Console.WriteLine($"ExpectedResult: {test.ExpectedResult}");
                // Console.WriteLine("Context Properties:");
                // foreach (var kvp in test.Context)
                // {
                //     Console.WriteLine($"{kvp.Key}: {kvp.Value}");
                // }
            }
        }
        else
        {
            Console.WriteLine("The 'tests' key is missing or not in the expected format.");
        }


        // Process your data here...
        // Console.WriteLine("Received JSON data:" + data.Count);
        // foreach (var item in data["tests"])
        // {

        // Console.WriteLine(item.Key + "" + unleash.IsEnabled(item.Key));
        // Console.WriteLine($"{item.Key}: {item.Value}");
        // }
    }
}