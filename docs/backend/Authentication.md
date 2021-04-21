# Authentication

The majority of endpoints and the socket framework
are protected by an authentication layer.<br>
For REST calls, we utilize the Authorization Header with a Bearer token to get access:
```env
Authorization: "Bearer <token>"
```

And when connecting to socket.io the token is specified as url query parameter along with the boat emblem:
```
<socket_url>?token=<token>&boatEmblem=<boat_emblem>
```
*More on socket connection in [Socket Protocoll Documentation](https://github.com/Adwirawien/CosmicSail/tree/feature/docs/docs#socket-protocol)*

### Where to get a token?

You currently **cannot** register for CosmicSail, but if you have a login,
the process of getting a user token is fairly simple.

# Login
Get a jsonwebtoken for usage with the api.

### Request
POST `/auth/login`<br>
 
**Authorization:** None<br>
**Query Params:** None<br>
**Body:**
| Name       | Description    | Type   | Required |
| ---------- | -------------- | ------ | -------- |
| `username` | Username       | String | Yes      |
| `password` | Password       | String | Yes      |
 
### Response

`200` - Success<br>
The token is valid for 24h.
```json
{
  "Token": ...,
  "Username": "cosmicSailor"
}
```
 
`400` - Bad Request<br>
Your post body could not be parsed.

`403` - Forbidden<br>
Username or password not valid.
