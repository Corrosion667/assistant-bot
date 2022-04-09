# Assistant bot

[![Maintainability](https://api.codeclimate.com/v1/badges/e0f4bc05e6177429c3c7/maintainability)](https://codeclimate.com/github/Corrosion667/assistant-bot/maintainability)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![linter check](https://github.com/Corrosion667/assistant-bot/actions/workflows/linter-check.yml/badge.svg)](https://github.com/Corrosion667/assistant-bot/actions/workflows/linter-check.yml)

---

## Overview

+ ***Assistant bot*** facilitates the work of the first line of support by answering frequently asked questions in the chat using **DialogFlow** technology from Google.    
+ It supports **Russian** and **English** languages and can be deployed in **Telegram** and **Vkontakte**.   
+ Bot will also send notification to admin user if unrecognised message received, to let human take control of the dialogue with the client. In case of error, notification will be also sent.

## Deployment

You can try to interact with the bot **here**:

| Service       | Link                             |
|---------------|----------------------------------|
| **Telegram**  | https://t.me/artem_secretary_bot |       
| **Vkontakte** | https://vk.com/assistantbotdemo  | 

Bot can answer questions on the following **topics**:

| English                       | Russian                          |
|-------------------------------|----------------------------------|
| Apply for a job               | Устройство на работу             |       
| Forgot password               | Забыл пароль                     | 
| Delete account                | Удаление аккаунта                | 
| Questions from banned users   | Вопросы от забаненных            | 
| Questions from conterpaties   | Вопросы от действующих партнёров | 

## Running

#### *Before Installation*
1. Create bot in **Telegram** with @BotFather and receive bot **token**;
2. Create public in **Vkontakte** and receive group **token**;
3. Create **project at DialogFlow** (here is the <a href="https://cloud.google.com/dialogflow/es/docs/quick/setup">guide</a>) and receive **project id**;
4. Create **DialogFlow agent** (here is the <a href="https://cloud.google.com/dialogflow/es/docs/quick/build-agent">guide</a>);
5. Create **JSON key** for Google cloud (here is the <a href="https://cloud.google.com/docs/authentication/getting-started">guide</a>).

#### *Installation*
1. clone the repository:
```bash
git clone https://github.com/Corrosion667/assistant-bot.git
```
2. Create **.env** file and set the <ins>following environmental variables</ins> *(as in the .env(example) file)*:

| Environmental       | Description                                                                                    |
|---------------------|------------------------------------------------------------------------------------------------|
| `TELEGRAM_TOKEN`    | bot token from @BotFather in telegram                                                          |       
| `TELEGRAM_ADMIN_ID` | id of admin user in telegram (can check using @userinfobot) to whom notifications will be sent |      
| `VKONTAKTE_TOKEN`   | group token of vkontakte                                                                       |
| `VKONTAKTE_ADMIN_ID`| id of admin user in vkontakte to whom notifications will be sent                               |
| `GOOGLE_APPLICATION_CREDENTIALS`| path to the file with JSON key from Google                                                     |
| `DIALOGFLOW_PROJECT_ID`| id of the project at DialogFlow                                                                |
3. Install dependencies:
```bash
make install
```
* Please take note that it requires *poetry*. If you do not have it yet, run:
```bash
make full-install
```
* So that *poetry* will also be installed into your user's environment with project dependencies.
4. Run the bots: `make run-tg` for **telegram** bot and `make run-vk` for **vkontakte** bot.

## Teaching the agent
You can easily create new training phrases for bot using script built inside the project.
Intents in the project are stored here:   
`bots/intents/english.json` for English;
`bots/intents/russian.json` for Russian.  
Configure them as you want and run `make teach-agent`   
It will create new intents and override intents if they already exist at your DialogFlow agent automatically.


## Demonstration
