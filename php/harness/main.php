<?php

require __DIR__ . '/../unleash-client-php/vendor/autoload.php';

use Unleash\Client\UnleashBuilder;
use Unleash\Client\Configuration\UnleashContext;


function createContext(array $context): UnleashContext
{
    $contextObject = (new UnleashContext())
        ->setCurrentUserId($context['userId'] ?? null)
        ->setSessionId($context['sessionId'] ?? null)
        ->setEnvironment($context['environment'] ?? null)
        ->setIpAddress($context['remoteAddress'] ?? '');

    if (isset($context['properties'])) {
        foreach ($context['properties'] as $property => $value) {
            $contextObject->setCustomProperty($property, $value);
        }
    }

    foreach ($context as $key => $value) {
        if ($key === 'properties') {
            continue;
        }
        $contextObject->setCustomProperty($key, $value);
    }

    return $contextObject;
}


$unleashApiUrl = getenv('UNLEASH_API_URL') ?: 'http://localhost:4242/api';

$tests = json_decode(file_get_contents('php://stdin'), true)["tests"];

$unleash = UnleashBuilder::create()
    ->withAppName("php-test-harness")
    ->withAppUrl($unleashApiUrl)
    ->withInstanceId("test-instance-id")
    ->withHeader('Authorization', "test-key")
    ->build();

$output = [];

foreach ($tests as $test) {
    $context = createContext($test["context"]);

    $result = $unleash->isEnabled($test["toggleName"], $context);
    $output[$test["description"]] = [
        "toggle_name" => $test["toggleName"],
        "result" => $result,
    ];
}
echo json_encode($output, JSON_PRETTY_PRINT);

echo PHP_EOL;
