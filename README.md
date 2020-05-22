# Opsdroid Trello Skill
A skill for [opsdroid](https://github.com/opsdroid/opsdroid) to use Trello App for use board, list and card. 

## Requirements 
Require [opsdroid](https://github.com/opsdroid/opsdroid) and [py-trello](https://github.com/sarumont/py-trello).


Install py-trello : 
```bash
pip install py-trello
```

## Configuration 
Go to config_trello.yaml for configure your api credential ([generate here](https://trello.com/app-key)). 

Trello skil need [databases](https://docs.opsdroid.dev/en/stable/databases/index.html). 

## Usage
In opsdroid you can use command : 
- ```trello board ``` for list your trello board. You can select active board with ```trello board numberboard``` (Ex : ```trello board 1 ```)
- ```trello lists``` for list your lists in trello board and select active list with  ```trello lists numberlist```
- ```trello list``` for list  card in trello list
- ```trello add card ``` for create card. (Ex : ```trello add card my new card ```) 