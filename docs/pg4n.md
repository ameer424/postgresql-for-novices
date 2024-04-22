# General information

## Installing pg4n

`pip install pg4n`

## Updating pg4n

`pip install --upgrade pg4n`

## Using pg4n

Before the usage of pg4n you should configure pg4n.

### Configuration

To configure pg4n you need to run command.py in the terminal. In your terminal, head to the profect-directory (directory with README.md) and run command "poetry run python -m src.pg4n.commands". Now you should have command.py running. 

#### Student/non-admin user

Non-admin users have four commands: help, exit, apikey and address. You need to use both apikey and address commands to configure Pg4n. You should get an apikey and address from an admin user. Address is needed to send the request and apikey is required for accepting the requests. Using commands: "apikey <your_apikey>" and "address <url_address>" you configuration file gets set up and Pg4n should work for you. If those configurations have not been done yet, system keeps printing out that you have not done them.

#### Admin

As admin you have access to same commands as a regular user. In addition you have commands to alter the state of the api and used LLM. You also have access to creating new users with new apikeys, deleting users, querying users. 

##### Creating, querying and deleting users

In order for students to use pg4n you need to use either create-command or createkeysfromcsv. These will add them in to the database with given id and their name. When they are added they get their apikeys and deafult amount of tokens they can use for the LLM. You need to give the students their apikeys so they get access to the LLM. In addition you need to give them the url to the api.

If you use create-command you need to give the command a list of students id/name pairs. This is handy when you only need to add few students. In case you create keys for a large amount of users you can also use command createkeysfromcsv and give a path to csv-file. This csv should have two columns with first one being for ids and the second one for names. The csv should use semicolon as separator.

Get-command has two ways it can be used. Get command returns and prints you the user info. You may either use "get <list_of_ids>" to get the info of some users or you can use command "get all" which returns all users from database.

Delete command also takes list of ids as parameter. It will delete users from database. After deleting, the deleted apikeys won't work anymore.

##### Api configuration

There are couple of things you can do for the api through commands.py. You can either close or open the api with command "setapi <ON_or_OFF>". If Api is turned off, users are not able to send api-request.

You can also both set and get parameters the LLM has. These include temperature, respones length in tokens, top p and prompt. 

Temperature = Affects the shape of the probability distribution for the predicted output and influences the likelihood of the model selecting lower-probability outputs. With lower values you get more likely outputs.  

TopP = a number between 0 to 1 that determinates how big portion of the probability distribution is selcted for deciding next output token. If the number is 0.7 it takes the 70% most likely output tokens of the total possible next token. Temperature decides how likely the LLM uses the most unlikely of the chosen portion.

Response length = Maximum amount of tokens the LLM can generate with each generated answer. With too small number the answers might not be finished but limiting it will save user's tokens and produce less costs.

Prompt = If you are not happy with the provided answers you can try to modify the prompt the LLM uses.


#### All commands

Reqular commands:
help - prints out all commands that can be used. Separates them to admin and reqular commands  
address <url> - Configures pg4n to send Api-requests to specified URL.  
apikey <your_apikey> - Adds users apikey to configuration file.  
exit - Shuts down the application.  

Admin commands:
get (<list_of_ids> or "all") - Finds the users by their ids or find all users.  
create <list_of_id_and_name_pairs> - Creates users for given ids and names. Id can be for example student number/id used in school.  
createkeysfromcsv - Give a csv-file with two columns and semicolon as separator. First column should be for ids and second column for names.  
delete <list_of_ids> - Deletes users with given ids.  
setapi <ON_or_OFF> - Sets Api's availability. If defined ON, users can send their requests. If set OFF, requests can not be sent.  
setparams - Is used for setting parameters of the LLM. After giving command setparams, user is asked to give values for each parameter. Those parameters left blank wil not be modified.  
getparams - Prints out the current parameters of the LLM.  

### Running Pg4n

To run Pg4n you need to make PostgreSQL listen to port 5432. This is the defaultport postgres will listen to when you install it. Then open your terminal and move to directory of the project. This is the directory with the file README.md-file in it. In that directory you need to run pg4n with command "poetry run python -m src.pg4n.main template1". Now the pg4n should be running.

Pg4n only injects messages for the user, and is otherwise completely transparent. For this reason, usage is identical to `psql` usage. [PostgreSQL: Documentation: 14: psql](https://www.postgresql.org/docs/14/app-psql.html)

### Semantic errors detected

- Comparison between different domains (Error 31 per Brass and Goldberg, 2005) (`CmpDomainChecker`)
- Condition in the subquery can be moved up (Error 30 per Brass and Goldberg, 2005) (`SubquerySelectChecker`)
- DISTINCT in SUM and AVG (Error 33 per Brass and Goldberg, 2005) (`SumDistinctChecker`)
- Implied expression (Table already enforces the given expression) (`ImpliedExpressionChecker`)
- Inconsistent expression (Error 1 per Brass and Goldberg, 2005) (`InconsistentExpressionChecker`)
- ORDER BY in a subquery (`SubqueryOrderByChecker`)
- SELECT in subquery uses no tuple variable of subquery (Error 29 per Brass and Goldberg, 2005) (`SubquerySelectChecker`)
- Strange HAVING (Error 32 per Brass and Goldberg, 2005) (`StrangeHavingChecker`)
- Wildcards without LIKE (Error 34 per Brass and Goldberg, 2005) (`EqWildcardChecker`)


### Syntax errors

If you have configured the pg4n like described earlier you should get LLM generated answers for you syntax errors. When your query gives you a syntax error, it will show you the error message just like psql normally does. But in case admin user has enabled the using LLM, you will also get the answer generated by it. This could take a little time.

Since the LLM is not free, all users will have limited amount of tokens the LLM can produce to help the users. If user has already ran out of their tokens, they will not receive anymore messages from the LLM. In this case you need to ask for more tokens from an admin user that has the authority to give them to you.

