# finance-toolkit
A collection of scripts and functions useful for financial analysis. The repository includes an indicators file for technical indicators and a performance file for performance measures. All modules have unit tests in the tests folder.

### Usage
To use simply copy the technical.py or performance.py
to your project folder and import it inside your script.

### Needed packages
- Python 3.8
- Pandas 1.1.0
- Numpy 1.19.1

### Technical indicators list
- ADX
- ATR
- bollband (Bollinger bands)
- MACD
- RSI
- OBV

### Performance indicators list
- CAGR
- volatility
- sharpe
- max_dd (Max Drawdown)
- calmar

## Goals
My goal in doing this project is to organize and share some functions that I've been using and practice some programming skills. I learned how to implement unit tests in python and how to run tests inside a docker container. Also, it was an opportunity to learn the math behind those indicators.

## How to test
Using docker container:
    Clone the repo
    Move to repository
    Run
    ```
    docker built -t finance-toolkit-tests .
    docker run finance-toolkit-tests
    ```

Not using docker:
    Clone the repo
    Move to repository
    Run
    ```
    python3 -m unittest discover -s tests/ -p '*_test.py'
    ```

## Afterthoughts
I believe I have accomplished my goals with this project. There're other functions that I want to implement but right now let's move on to other projects. The tests could have been better implemented, especially the technical indicators tests which I implemented first. I learned a lot about the unittest module and how to use docker in this context.