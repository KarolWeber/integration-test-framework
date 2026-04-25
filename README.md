An anonymized Python-based integration testing framework designed to validate real-money gaming platform workflows in a distributed environment.

It supports end-to-end validation of player lifecycles, wallet operations, game sessions, bonus engines, and third-party provider integrations across multiple execution contexts.

The framework is built with a layered architecture to ensure separation between test orchestration, business logic, and API communication.

---

## Table of contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Project structure](#project-structure)
- [How to write new tests](#how-to-write-new-tests)
- [Sample test](#sample-test)
- [Services](#services)
- [Running tests](#running-tests)
- [Logging and reporting](#logging-and-reporting)
- [Code quality](#code-quality)
- [Known limitations and possible improvements](#known-limitations-and-possible-improvements)

---

## Installation

The framework runs on Python 3.13.7.
Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Environment-specific configuration is managed via `.env` files to separate test logic from runtime environments.

This allows the same test suite to be executed across multiple environments (local, staging, integration) without code changes.

---

## Project structure

The framework is organized into a layered architecture that separates test execution, domain logic, API communication, and shared utilities.

- api → Core API layer responsible for communication with external systems
    - clients → Low-level API communication handlers (HTTP requests, responses)
    - services → Domain-level business logic and orchestration of API flows
    - request_api.py → Central HTTP abstraction layer (authentication, headers, error handling)

- entities → Data models representing API responses and structured objects used across services and tests

- infrastructure → Environment configuration and runtime dependencies (credentials, settings)

- tests → Test suites focused on system and integration-level validation
    - integration → End-to-end integration tests for platform workflows
      (test files follow pattern: test_*.py or *_test.py)

- urls → Centralized API endpoint definitions used by clients

- utils → Shared utilities supporting test execution and framework operations
    - assertions → Assertion engine and reporting utilities
    - cleanup → Environment and data cleanup helpers
    - converters → Data transformation utilities
    - enums → Shared enumerations for domain constants
    - files → File handling utilities
    - generators → Test data generation
    - logging → Logging and step tracking utilities
    - mappers → Data mapping between API and domain objects
    - payloads → Request payload builders
    - reports → Report generation utilities (Allure → unified HTML reports)
    - resources → Static test resources
    - waiters → Synchronization and condition waiting utilities

---

## How to write new tests

Each test in the framework should follow a consistent structure and use shared components.

It should include a defined title using `@allure.title()` and a severity level using `@allure.severity()` </br>
Allure supports the following severity levels:

- BLOCKER
- CRITICAL
- NORMAL
- MINOR
- TRIVIAL

The pytest `request` fixture is required by `CheckAssertions`. </br>
At the beginning of each test, the `CheckAssertions` class should be initialized. It is responsible for:

- adding and storing assertions,
- validating test results,
- generating readable Allure reports (stdout section),
- automatically creating test names based on their path.

The `assertion()` method of the `CheckAssertions` class allows multiple assertions to be added within a single test,
while the `check_assertions()` method executes their validation and returns the final test result.

---

## Sample test

```
@allure.title('Provider one player authentication')  # Test title
@allure.severity(allure.severity_level.NORMAL)  # Test severity
def test_provider_one_player_authentication(self, request):
    ca = CheckAssertions(request=request)  # Initialize assertion class

    player = PlayerService()  # Initialize player context
    player.user.login()  # Player login

    admin = AdminService()  # Initialize admin context
    admin.user.login()  # Admin login
    custom_game = admin.technical.game.create_custom_game()  # Create a technical game via admin

    player_run_game = player.game.run_provider_one_game(game=custom_game)  # Start game session

    ca.assertion(  # Add assertion
        name="Provider one authenticate status",  # Assertion name
        expected="SUCCESS",  # Expected result
        current=player_run_game.authenticate_status,  # Actual result
        operator='eq'  # Assertion operator
    )

    ca.check_assertions()  # Execute assertions and generate report
```

---

## Services

The framework is built around domain-specific services that abstract platform functionality into business-oriented operations.

Each service sits on top of API clients and is responsible for orchestration and domain logic:

- AdminService → provides control over the platform (users, games, bonuses, configuration)
- PlayerService → simulates end-user behavior (authentication, gameplay, wallet operations)
- Provider services → handle third-party game provider integrations (betting, wins, authentication flows)

### Architecture flow:

Test → Context (Player/Admin abstraction) → Service Layer (domain orchestration) → Client Layer (HTTP communication) → External API systems

---

## Running tests

***

Running all tests:

```bash
pytest
```

***

Running tests with selected tags(e.g. integration_test_provider_one):

```bash
pytest -m integration_test_provider_one
```

The list of available tags is in the pytest.ini file

***

Running tests and generating an allure report:

```bash
pytest --alluredir=allure-results
```

***

Running a report locally:

```bash
allure serve allure-results
```

***

Generating a report after the test session ends:

```bash
allure generate
```

To generate a report in a merged HTML file, after generating the report, run the script `utils/reports/report_generator.py`

---

## Logging and reporting

- The framework uses Allure for test reporting.
- The `StepLogger` class is used for logging test steps and API responses if added inside service methods.
- The `CheckAssertions` class executes multiple assertions without stopping the test until all of them are evaluated. In case of failures, it provides a full report with descriptions, expected values, and actual results.

---

## Code quality

The project uses `flake8` for static code analysis and to maintain PEP8 compliance.

Run code analysis:

```bash
flake8 .
```

---

## Known Limitations and Trade-offs

The framework intentionally prioritizes test readability and fast test development over strict architectural purity in certain areas.

- Test tagging system is simplified to reduce configuration overhead, with future support planned for dynamic grouping and filtering
- StepLogger currently uses in-memory state, which may require enhancements for highly parallel execution environments
- HTTP interception is not centralized to keep service-level behavior explicit and easier to debug
- CI/CD orchestration is intentionally excluded, as the framework focuses on test logic rather than execution infrastructure

---
