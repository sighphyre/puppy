package org.example;

import io.getunleash.DefaultUnleash;
import io.getunleash.Unleash;
import io.getunleash.UnleashContext;
import io.getunleash.event.UnleashSubscriber;
import io.getunleash.lang.Nullable;
import io.getunleash.repository.FeatureToggleResponse;
import io.getunleash.util.UnleashConfig;

import java.lang.reflect.Type;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.Scanner;
import java.util.Optional;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.databind.node.ArrayNode;


public class App {
    public String getGreeting() {
        return "Hello World!";
    }

    static UnleashContext buildContext(JsonNode node) {
        UnleashContext.Builder builder = UnleashContext.builder();

        if (node.has("appName")) {
            builder.appName(node.get("appName").asText());
        }
        if (node.has("environment")) {
            builder.environment(node.get("environment").asText());
        }
        if (node.has("userId")) {
            builder.userId(node.get("userId").asText());
        }
        if (node.has("sessionId")) {
            builder.sessionId(node.get("sessionId").asText());
        }
        if (node.has("remoteAddress")) {
            builder.remoteAddress(node.get("remoteAddress").asText());
        }
        if (node.has("currentTime")) {
            ZonedDateTime currentTime = ZonedDateTime.parse(node.get("currentTime").asText());
            builder.currentTime(currentTime);
        }

        if (node.has("properties")) {
            JsonNode properties = node.get("properties");
            properties.fields().forEachRemaining(entry -> {
                builder.addProperty(entry.getKey(), entry.getValue().asText());
            });
        }

        return builder.build();
    }

    public static void main(String[] args) throws Exception {

        Scanner scanner = new Scanner(System.in);
        StringBuilder jsonInput = new StringBuilder();
        while (scanner.hasNextLine()) {
            jsonInput.append(scanner.nextLine());
        }
        scanner.close();

        ObjectMapper testMapper = new ObjectMapper();

        JsonNode rootNode = testMapper.readTree(jsonInput.toString());
        JsonNode testsNode = rootNode.get("tests");

        String unleashApiUrl = Optional.ofNullable(System.getenv("UNLEASH_API_URL"))
                .orElse("http://localhost:4242/api/");

        UnleashConfig config = UnleashConfig.builder().appName("java-test-harness")
                .customHttpHeader("Authorization",
                        "test-key")
                .unleashAPI(unleashApiUrl).instanceId("java-test-harness")
                .synchronousFetchOnInitialisation(true)
                .build();

        Unleash unleash = new DefaultUnleash(config);

        ObjectMapper outputMapper = new ObjectMapper();
        ObjectNode output = outputMapper.createObjectNode();

        if (testsNode.isArray()) {
            for (JsonNode testNode : testsNode) {
                String toggleName = testNode.get("toggleName").asText();
                String testDescription = testNode.get("description").asText();
                UnleashContext context = buildContext(testNode.get("context"));
                boolean enabled = unleash.isEnabled(toggleName, context);

                ObjectNode testResult = outputMapper.createObjectNode();
                testResult.put("toggle_name", toggleName);
                testResult.put("result", enabled);
                testResult.put("context", testNode.get("context"));

                output.put(testDescription, testResult);
            }
        }

        // Pretty print the JSON output
        String prettyJson = outputMapper.writerWithDefaultPrettyPrinter().writeValueAsString(output);
        System.out.println(prettyJson);
    }
}
