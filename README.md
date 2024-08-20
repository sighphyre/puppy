# Puppy (Portable Unleash Poker.py)

Puppy is a portable tool for analyzing Unleash SDK evaluation and metric logic across arbitrary test cases.

A process affectionately referred to by myself as "Poking it with a stick."
<p align="center">
    <img src="./Puppy_white.png" />
</p>

### Why?

The existing SDK validation strategy is made of up of two components, both with limitations.

The first is client specification tests, which define how a toggle should execute. These are very rigid tests, since they're defined outside the SDK and consumed via their semantic version. Updating these tests needs consideration and forethought, since they're... well... our spec. This means they're a poor choice for understanding a wide range of behaviors for things like local testing or understanding the scope of bugs across SDKs. They also don't provide insight into how the HTTP layer or metrics work.

The second is the unit and integration tests largely written by original authors or maintainers. These tests cover behaviors not well covered by the client spec and generally provide excellent coverage but they're not standard and there's no way of asserting behaviors like metrics across a range of SDKs or versions.

Because of these limitations, it becomes quite difficult to achieve a few very nice things:

- Enforce how metrics evaluate across SDKs
- Fuzz test strategy, constraint, and variant logic
- Enforce that the client spec is correctly implemented end to end (there's been at least one case where a bug in the HTTP layer changed an SDK's evaluation of toggle logic)
- Understand the scope of a bug across versions
- Understand how legacy versions of SDKs may interact with modern Unleash responses or vice versa
- Prototype new feature logic safely

In practice these things are rarely needed but when you do need them it's great to have some of the details taken care of for you.

### Quickstart

This guide assumes you have at bare minimum:

- bash
- jq
- cat
- cURL
- awk
- docker
- firefox (optional, can use a different browser)

This will take you through the process of getting the Python SDK up and running for report generation. This is the same process for all SDKs so feel free to generalize it.

Start by cloning the SDK repo within the python folder:

`cd python && git clone https://github.com/Unleash/unleash-client-python`

Start the puppy server, this will serve toggles up to the SDK harness as it executes the test suite:

`./run-puppy-server.sh`

Hydrate the server with some feature toggles, you should change these for your own run:

`./hydrate.sh feature_toggles.json`

The `feature_toggles.json` file can be swapped out for any valid response from `/api/client/features` from an Unleash or Edge server.

Run a container in debug mode, this will stream out the results to std out. For example Python:

`./run-test.sh python ./testfile.json`

### Quickstart for reporting

This assumes you've cloned the child repositories for all the SDKs. We'll now do a full test run against all the SDKs and generate some nice HTML reports so we can visualize the data sets.

Turn off the debug flag in your shell so we can output the test files:

`export PUPPY_DEBUG=false`

Run all the SDK harnesses for your test file:

```sh
./run-test.sh dotnet ./testfile.json && \
./run-test.sh go ./testfile.json && \
./run-test.sh java ./testfile.json && \
./run-test.sh node ./testfile.json && \
./run-test.sh php ./testfile.json && \
./run-test.sh python ./testfile.json && \
./run-test.sh ruby ./testfile.json && \
./run-test.sh ygg ./testfile.json
```

Now you can run a report comparing the output of these runs against one another:

`./run-report.sh && firefox report.html`

### What's Puppy

Puppy is not a testing framework. Puppy is an evaluation framework. It will tell you information about how an SDK behaves but it will not make judgement calls. However, that information can be outputted in a format that can be used as a test.

## How Puppy works

### Components

#### Puppy Server

#### Harnesses

### Execution Model

### Understanding the inputs

### Understanding the output

### Putting it together

## Goals

