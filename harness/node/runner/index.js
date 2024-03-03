const { initialize } = require('unleash-client');
const readline = require('readline');
const { stdin: input, stdout: output } = require('process');

const client = initialize({
    url: 'http://seidr-core:4242/api/',
    appName: 'node-test-harness',
    customHeaders: { Authorization: 'SOME-SECRET' },
    disableMetrics: true,
    disableRegistration: true,
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
            const { toggleName, context, description, expectedResult } = test;
            const result = client.isEnabled(toggleName, context);

            results[description] = {
                toggleName,
                result,
                context
            };
        });

        console.log(JSON.stringify(results, null, 4));
    });
});
