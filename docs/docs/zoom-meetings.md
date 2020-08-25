---
id: zoom-meetings
title: Zoom Meetings
---


# Zoom Virtual Meetings

_The pandemic situation made the portal team realize that there was a need to have virtual meetings enabled so that the portal users could hold meetings even in the lockdown situation._

Here are the Details regarding the implementation of the Virtual Meetings using Zoom API:

### Authorization

Every API requires authorization from the user. This is the API Authorization Process for ZOOM API using JWT:

- The API KEY for the App is signed to the payload of the jwt, along with the expiration time of the JWT;
- The expiration time for the jwt in the portal is being set to 30 seconds
- Using pyjwt the jwt is encoded using the payload, after being signed by the SECRET KEY.
- Once the JWT is created we can use this in the authorization header and make calls to the API.
