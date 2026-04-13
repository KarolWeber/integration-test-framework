# An anonymized production-grade integration test framework used in a real-world commercial environment.

---

# Integration Test Framework

A framework for writing and running automated tests for a casino platform.

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

Environment variables must be configured in the `.env` file.
Example:
- PLAYER_API='url'
- ADMIN_API='url'
- PROVIDER_ONE='url'
- PROVIDER_ONE_ORIGIN='url'
- PROVIDER_TWO='url'
- PLAYER_EMAIL='@example.com'
- ADMIN_TEST_USERNAME='username@example.com'
- ADMIN_TEST_PASSWORD='password'

---

## Project structure

- api -> API clients and services
    - clients -> API communication clients
    - services -> Business logic services
    - request_api.py -> HTTP request handling
- entities -> API response entities and data models
- infrastructure -> Configuration files
- tests -> Test directory
    - integration -> Integration tests
        - Test files must follow pattern: test_*.py or *_test.py
- urls -> API endpoint definitions
- utils -> Helper functions
    - assertions -> Assertion builders and reporting utilities
    - cleanup -> Environment cleanup functions
    - converters -> Data converters
    - enums -> Enums
    - files -> File management utilities
    - generators -> Test data generators
    - logging -> Test logging
    - mappers -> Data mappers
    - payloads -> Request payloads
    - reports/report_generator.py -> Allure report conversion to a unified HTML file
    - resources -> Test resource files
    - waiters -> Functions waiting for specific conditions

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

The framework provides a set of services for API communication and test operations. </br>
Each service is responsible for a specific functional area of the platform.

- AdminService -> enables management of the casino platform (e.g. users,
  games, bonuses).

- PlayerService -> enables player-side operations such as login,
  game execution, and gameplay.

<u>Currently, they only support the basic operations required for integration testing with providers.</u>

- ProviderOneService – handles integration with Provider One API, including authorization,
  betting, and payout processing.
- ProviderTwoService – handles integration with Provider Two API, including authorization,
  betting, and payout processing.

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

## Known limitations and possible improvements

- Test tagging system (pytest markers) is not fully implemented yet and can be added for better test grouping and execution control
- StepLogger uses global in-memory state which may require isolation improvements for parallel test execution
- Logging system is manual and could be extended with automatic HTTP interception
- Test execution configuration is basic and could be extended with CI pipelines and test matrix support

---
