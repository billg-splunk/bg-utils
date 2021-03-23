# API - Teams

See details on [team management here](https://docs.signalfx.com/en/latest/managing/teams/index.html).

This document walks through examples of using the Teams API to manage teams. It has examples for:
[https://dev.splunk.com/observability/reference/api/teams/latest](https://dev.splunk.com/observability/reference/api/teams/latest)

Adjust your realm; these examples are based on us1.

## Example Scenario

This scenario will walk through the following:
* Viewing all users
* Creating a team (with an existing user)
* Updating a team (with a new set of users)
* Inviting users to the organization

For the API calls that create/update/delete the teams you will need to use a user API access token. You can find this on your [profile page](https://app.us1.signalfx.com/#/myprofile).

### View Users

Get the users in your organization. Use the limit and offset to get all users across multiple calls (i.e. limit 10, using offets of 0;10;20;30;40 to get 45 users). 

```
GET https://api.us1.signalfx.com/v2/organization/member?limit=10&offset=0
content-type: application/json
X-SF-TOKEN: <token>
```

To get users to add to teams, note down their **id**.

### Get Teams

Get a list of all the teams. The limits and offsets work the same way.

```
GET https://api.us1.signalfx.com/v2/team?limit=10&offset=0
content-type: application/json
X-SF-TOKEN: <token>

```

### Create a team

Create a new team, and add members to it:

```
POST https://api.us1.signalfx.com/v2/team
content-type: application/json
X-SF-TOKEN: <token>

{
  "name": "<team name>",
  "description": "<team description>",
  "members": [
    "<user id 1>",
    "<user id 2>"
  ]
}
```

### Update a team

Make updates to the team membership:

```
PUT https://api.us1.signalfx.com/v2/team/<team id>/members
content-type: application/json
X-SF-TOKEN: <token>

{
  [
    "<user id 1>"
  ]
}
```

### Delete a team

To delete a team:

```
DELETE https://api.us1.signalfx.com/v2/team/<team id>
content-type: application/json
X-SF-TOKEN: <token>
```

### Inviting users to the organization

To invite a user:

```
POST https://api.us1.signalfx.com/v2/organization/member
content-type: application/json
X-SF-Token: <token>

{
  "email": "<email-address>"
}
```