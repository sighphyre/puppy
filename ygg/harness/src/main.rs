use serde::{Deserialize, Serialize};
use serde_json;
use std::{
    collections::HashMap,
    io::{self, Read},
};
use unleash_types::client_features::ClientFeatures;
use unleash_yggdrasil::{self, EngineState};

#[derive(Serialize, Deserialize, Debug)]
struct Test {
    description: String,
    context: unleash_yggdrasil::Context,
    toggleName: String,
    expectedResult: bool,
    bench: Option<usize>,
}

#[derive(Serialize, Deserialize, Debug)]
struct TestSuite {
    tests: Vec<Test>,
}

#[derive(Serialize, Deserialize, Debug)]
struct TestOutput {
    result: bool,
    toggleName: String,
}

fn fetch_feature_toggles() -> ClientFeatures {
    let client = reqwest::blocking::Client::new();

    let base_api = std::env::var("UNLEASH_API_URL")
        .unwrap_or_else(|_| "http://localhost:4242/api/".to_string());

    let unleash_api_url = format!("{}client/features", base_api);

    let response = client
        .get(unleash_api_url)
        .header("Authorization", "some-key")
        .send()
        .expect("Failed to fetch features, test cannot continue");

    response
        .json::<ClientFeatures>()
        .expect("Failed to deserialize features, test cannot continue")
}

fn main() {
    let mut input = String::new();
    io::stdin()
        .read_to_string(&mut input)
        .expect("Expected test suite in std in");

    let suite: TestSuite =
        serde_json::from_str(&input).expect("Cannot parse test suite, cannot continue");

    let features = fetch_feature_toggles();

    let mut engine = EngineState::default();
    let warnings = engine.take_state(features.clone());
    if let Some(warnings) = warnings {
        eprintln!("Failed to take state: {:?}", warnings);
    }

    let mut test_output = HashMap::new();

    for test in suite.tests.iter() {
        let result = engine.is_enabled(&test.toggleName, &test.context, &None);
        test_output.insert(
            test.description.clone(),
            TestOutput {
                result,
                toggleName: test.toggleName.clone(),
            },
        );
    }

    println!(
        "{}",
        serde_json::to_string_pretty(&test_output).expect("Failed to materialize output")
    );
}
