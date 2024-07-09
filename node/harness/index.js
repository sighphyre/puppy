const { initialize } = require('unleash-client');
const readline = require('readline');
const { stdin: input, stdout: output } = require('process');

const unleashApiUrl = process.env.UNLEASH_API_URL || 'http://localhost:4242/api/';
const unleashApiKey = process.env.UNLEASH_API_KEY || 'SOME-SECRET';

const client = initialize({
    url: unleashApiUrl,
    appName: 'node-test-harness',
    customHeaders: { Authorization: unleashApiKey },
    environment: 'default',
});

client.on('ready', () => {
    const rl = readline.createInterface({ input, output, terminal: false });

    let rawData = '';

    rl.on('line', (line) => {
        rawData += line;
    });

    rl.on('close', () => {
        const tests = JSON.parse(rawData).tests;
        const results = {};

        tests.forEach(test => {
            const { toggleName, context, description, _expectedResult } = test;

            let lastEnabled = client.isEnabled(toggleName, context);;

            results[description] = {
                toggleName,
                lastEnabled,
                time
            };
        });

        console.log(JSON.stringify(results, null, 4));
    });
});
