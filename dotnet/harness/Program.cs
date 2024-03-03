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

        string unleashApiUrl = Environment.GetEnvironmentVariable("UNLEASH_API_URL") ?? "http://localhost:4242/api/";

        var settings = new UnleashSettings()
        {
            AppName = "dotnet-test",
            UnleashApi = new Uri(unleashApiUrl),
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
            }
        }
        else
        {
            Console.WriteLine("The 'tests' key is missing or not in the expected format.");
        }
    }
}