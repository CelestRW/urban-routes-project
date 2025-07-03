# Urban Routes Automated Testing Project

## Overview

This project contains an automated test suite for the Urban Routes web application. The tests verify core functionalities such as setting addresses, selecting plans, entering phone numbers, adding payment methods, and ordering items using Selenium WebDriver with Python and pytest.

## Project Structure

- `main.py` — Contains the test class and test methods using pytest  
- `pages.py` — Page Object Model class with element locators and interaction methods  
- `helpers.py` — Helper functions (e.g., URL reachability check, phone code retrieval)  
- `data.py` — Test data constants used across tests   

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/CelestRW/urban-routes-project.git
   cd urban-routes-project
