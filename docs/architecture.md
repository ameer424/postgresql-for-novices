# Architecture

![Program architecture sketch](./architecture.jpg)

## Backend

### Commands

Commands.py has a main-function that can be started by any user with command: "poetry run python -m src.pg4n.commands". Commands is a class that is simply used for configurations of the environment. When started, Commands creates an infinite loop that keeps running until user give command to exit. All commands are available to the admin user but only some for reqular user. 

Reqular commands:
help - prints out all commands that can be used. Separates them to admin and reqular commands  
address <url> - Configures pg4n to send Api-requests to specified URL.  
apikey <your_apikey> - Adds users apikey to configuration file.  
exit - Shuts down the application.  

Admin commands:
get (<list_of_ids> or "all") - Finds the users by their ids or returns all users.  
create <list_of_id_and_name_pairs> - Creates users for given ids and names. Id can be for example student number/id used in school.  
delete <list_of_ids> - Deletes users with given ids.  
setapi <ON_or_OFF> - Sets Api's availability. If defined ON, users can send their requests. If set OFF, requests can not be sent.  
setparams - Is used for setting parameters of the LLM. After giving command setparams, user is asked to give values for each parameter. Those parameters left blank wil not be modified.  
getparams - Prints out the current parameters of the LLM.  

In case an invalid argument is given, system alerts that command isn't found and then lists all possible commands.

### ErrorFormatter
Unified error formatting.
Each Checker class must use this to format their warning messages.

### PsqlConnInfo

`PsqlConnInfo` fetches PostgresSQL connection info by running a `psql` command with given arguments (usually same arguments as with what the main `psql` process was called with).

### QEPParser

See API docs.

### SemanticRouter

Runs SQLParser, QEPParser and semantic error analysis modules (as configured) against given SQL query string.


### SyntaxRouter

Class that is called when PostgreSQL gives a syntax error. When initialized, it gets users psql info: port, host, user, password and name and in addition optional configuration values. 

Run_analysis function gets the psql error message and the query as strings. Then it fetches the schema. SyntgaxRouter then creates an ModelHelper-object and uses it to send the request and getting the response-body.

### ModelHelper
Sends the Api-requests and receives them. Gets the url to lambda-function when the class is  initialized. In send_request function, the modelhelper gets the sql-query, errormessage and schema as parameters. It will send the parameters to the Api in reuqestbody. After sending the request it receives the response and returns the response it received.


### SQLParser

Transforms sql string into a syntax tree.
Also provides some utilities like finding all tables in a sql statement.

### Analysis modules

#### CmpDomainChecker

Does analysis for suspicous comparisons between different domains.
e.g., comparing columns off type VARCHAR(20) and VARCHAR(50)
Returns a warning message if something was found, otherwise None.

#### EqWildcardChecker

Returns warning message if the sql has equals operation to a string with
wild card character (the '%' character), otherwise None.

#### ImpliedExpressionChecker

Returns warning message if implied expression is detected, otherwise None.

#### InconsistentExpressionChecker

Inconsistent expression is some expression that is never true.
For example: x = 10 AND x = 20

This checker only finds a small subset of such expression, where postgresql
itself detects the inconsistent expression in its query optimizer and
exposes that information via its query execution plan.

#### StrangeHavingChecker

Returns warning message if there exists HAVING without a GROUP BY, otherwise None.

#### SubqueryOrderByChecker

Returns warning message if there exists ORDER BY in a subquery,
otherwise None.

This check gives misses some situations with redundant ORDER BY but
should never give false positives, only false negatives.

#### SubquerySelectChecker

Returns warning message if there no column SELECTed in a subquery is
not used in that subquery of its own columns, otherwise returns None.

#### SumDistinctChecker

Returns warning message if the sql has SUM/AVG(DISTINCT ...), otherwise None

### Program configuration

The configuration files are read in order from: /etc/pg4n.conf then from $XDG\_CONFIG\_HOME/pg4n.conf, or if $XDG\_CONFIG\_HOME is not set, from
$HOME/.config/pg4n.conf, and lastly from $PWD/pg4n.conf, with each new value
introduced in latter files overriding the previous value.

Options in the configuration file are written like: "option\_name value" where value may be: true, 1, yes, false, 0, no

By default all warnings are enabled. Warnings can be disabled by warning type (which can be found from every warning message's end) e.g.

`CmpDomains false`

#### ConfigParser

Parses a configuration file.

#### ConfigReader

Reads all configuration files and combines their option output into a `ConfigValues` class.

#### ConfigValues

Contains option values specied in the configuration files.

## Frontend

Frontend handles user's psql session completely transparently via `PsqlWrapper`, although also injecting insightful messages regarding user's semantic errors into the terminal output stream. It parses user's SQL queries via `PsqlParser` for consumption in the backend.

### PsqlParser

`PsqlParser` uses `pyparsing` parser combinator library to provide parsing functions for
- checking for non-obvious Return presses (`output_has_magical_return`)
- checking if given string has a new prompt (e.g `=> `) (`output_has_new_prompt`)
- parsing a new prompt and everything that precedes it in a string, to allow easy message injection (`parse_new_prompt_and_rest`)
- parsing last SQL SELECT query in a string (`parse_last_stmt`)
- parsing `psql --version` output for version number (`parse_psql_version`)
- parsing syntax errors (`ERROR:` .. `^`) (`parse_syntax_error`)

Parsing rules common to more than 1 of these functions are listed in `PsqlParser` body, but otherwise rules are inside respective functions.

### PsqlWrapper

`PsqlWrapper` is responsible for spawning and intercepting the user-interfacing `psql` process. `pexpect` library allows both spawning and intercepting the terminal control stream. `pyte` library keeps track of current terminal display.

Overall working logic is handled by `_check_and_act_on_repl_output`, where it can be seen that queries are checked for every time user presses Return. If `PsqlParser` finds an SQL SELECT query, it's passed to `SemanticRouter` for further analysis, and any insightful message returned is saved for later. Once all query results have been printed, and a new prompt (e.g `..=> `) is going to be printed next per `latest_output` parameter, the wrapper injects the returned message. If results included `ERROR:` .. `^`, it is sent to syntax error analysis, and any returned message will be injected immediately.

`PsqlWrapper` also checks `psql` version info and checks it against `PsqlWrapper.supported_psql_versions`.
