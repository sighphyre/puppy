const { initialize } = require('unleash-client');
const readline = require('readline');
const { stdin: input, stdout: output } = require('process');

const unleashApiUrl = process.env.UNLEASH_API_URL || 'http://localhost:4242/api/';
const unleashApiKey = process.env.UNLEASH_API_KEY || 'SOME-SECRET';

const client = initialize({
    url: unleashApiUrl,
    appName: 'node-test-harness',
    customHeaders: { Authorization: unleashApiKey },
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
            const { toggleName, context, description, _expectedResult, bench = 1 } = test;

            const start = performance.now();
            let lastEnabled = false;
            for (let i = 0; i < bench; i++) {
                lastEnabled = client.isEnabled(toggleName, context);
                // if (i % 100000 === 0) {
                //     const memoryUsage = process.memoryUsage();
                //     console.clear();
                //     outputBuffer = `Memory Usage: \n`;
                //     outputBuffer += `- Test: ${description}\n`;
                //     outputBuffer += `- RSS (Resident Set Size): ${memoryUsage.rss / 1024 / 1024} MB\n`;
                //     outputBuffer += `- Total Heap Size: ${memoryUsage.heapTotal / 1024 / 1024} MB\n`;
                //     outputBuffer += `- Used Heap Size: ${memoryUsage.heapUsed / 1024 / 1024} MB\n`;
                //     outputBuffer += `- External Memory: ${memoryUsage.external / 1024 / 1024} MB\n`;
                //     outputBuffer += `- Array Buffers: ${memoryUsage.arrayBuffers / 1024 / 1024} MB\n`;
                //     console.log(outputBuffer);
                // }
            }

            const time = performance.now() - start; //milliseconds

            results[description] = {
                toggleName,
                lastEnabled,
                time
            };
        });

        console.log(JSON.stringify(results, null, 4));
    });
});
