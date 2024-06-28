# Puppy (Portable Unleash Poker.py)

Puppy is a portable tool for analyzing Unleash SDK evaluation and metric logic across arbitrary test cases.

A process affectionately referred to by myself as "Poking it with a stick."

![Puppy](./Puppy.png)

### Why?

The existing SDK validation strategy is made of up of two components, both with limitations.

The first is client specification tests, which define how a toggle should execute. These are very rigid tests, since they're defined outside the SDK and consumed via their semantic version. Updating this of tests needs consideration and forethought, since they're... well... our spec. This means they're a poor choice for understanding a wide range of behaviors for things like local testing or understanding the scope of bugs across SDKs. They also don't provide insight into how the HTTP layer or metrics work.

The second is the unit and integration tests largely written by original authors or maintainers. These tests cover behaviors not well covered by the client spec and generally provide excellent coverage but they're not standard and there's no way of asserting behaviors like metrics across a range of SDKs or versions.

Because of these limitations, it becomes quite difficult to achieve a few very nice things:

- Enforce how metrics evaluate across SDKs
- Fuzz test strategy, constraint, and variant logic
- Enforce that the client spec is correctly implemented end to end (there's been at least one case where a bug in the HTTP layer changed an SDK's evaluation of toggle logic)
- Understand the scope of a bug across versions
- Understand how legacy versions of SDKs may interact with modern Unleash responses or vice versa
- Prototype new feature logic safely

In practice these things are rarely needed but when you do need them it's great to have some of the details taken care of for you.

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

