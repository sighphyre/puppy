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

        var output = new Dictionary<string, Dictionary<string, object>>();

        if (data.TryGetValue("tests", out var tests))
        {
            foreach (var test in tests)
            {
                var result = unleash.IsEnabled(test.ToggleName, test.Context);
                output[test.Description] = new Dictionary<string, object>
                {
                    { "toggle_name", test.ToggleName },
                    { "result", result },
                    { "context", test.Context }
                };
            }
        }
        else
        {
            throw new Exception("Input was found but missing 'tests' key.");
        }
        Console.WriteLine(JsonConvert.SerializeObject(output, Formatting.Indented));
    }
}