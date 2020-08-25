---
id: environment-variables
title: Environment Variables
---


## The following Environment Variables need to be exported for the correct functioning of the Portal locally

***
### SECRET_KEY
A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
django-admin startproject automatically adds a randomly-generated SECRET_KEY to each new project.
Uses of the key shouldn’t assume that it’s text or bytes. Django will refuse to start if SECRET_KEY is not set.

```shell
export SECRET_KEY=foobarbaz
```

### GOOGLE_MAPS_API_KEY
To use the Maps Static API you must have an API key. The API key is a unique identifier that is used to authenticate requests associated with your project for usage and billing purposes.

Depending on your usage, a digital signature may also be required (see Other Usage Limits) The digital signature allows our servers to verify that any site generating requests using your API key is authorized to do so.

To get an API key:

- Go to the Google Cloud Platform Console.
- Click the project drop-down and select or create the project for which you want to add an API key.
- Click the menu button  and select APIs & Services > Credentials.
- On the Credentials page, click + Create Credentials > API key.
- The API key created dialog displays the newly created API key.
- Click Close.
- The new API key is listed on the Credentials page under API Keys.
(Remember to restrict the API key before using it in production.)

```shell
export GOOGLE_MAPS_API_KEY=<Your API Key>
```

## Environment Variable Description

| Variable Name      |  Description |
| --------- | ----------------------------------------------- |
| SECRET_KEY | A variable which cryptographically signs the Web App |
| GOOGLE_MAPS_API_KEY | Needed to Run Google Maps correctly locally |
