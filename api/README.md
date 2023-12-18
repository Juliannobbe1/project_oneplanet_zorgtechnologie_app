# Usage

## Run all tests
> Prerequisites:
- Run `docker run -e NEO4J_AUTH="neo4j/iVOG0qvVg9iYYGz6WVf8BW19Xv4zmmHbDIkH0ur9PCU" --publish=7474:7474 --publish=7687:7687 neo4j`

### Without output
Run `pyb`

### With output
Run `pyb -v`

## Run unit tests

### Without output
Run `pyb run_unit_tests`

### With output
Run `pyb run_unit_tests -v`

## Run integration tests
> Prerequisites:
- Run `docker run -e NEO4J_AUTH="neo4j/iVOG0qvVg9iYYGz6WVf8BW19Xv4zmmHbDIkH0ur9PCU" --publish=7474:7474 --publish=7687:7687 neo4j`

### Without output
Run `pyb run_integration_tests`

### With output
Run `pyb run_integration_tests -v`