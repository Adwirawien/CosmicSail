# 📖 Documentation

This documentation is split up into several parts for a better structure and overview
over the protocols and communitcation methods that CosmicSail utilizes.

## Backend

Our backend is written in Golang with the help of two amazing frameworks,
[Gorm](https://gorm.io) and [Fiber](https://gofiber.io).

- [Authentication](./backend/Authentication.md): To use the CosmicSail API, a user has to authenticate over these endpoints
- WIP [v1 User Endpoints](./backend/v1%20User%20Endpoints.md): Endpoints that a user can access to manage their boats
- WIP [v1 Boat Endpoints](): Endpoints which are made for the boat (telemetry updating or data loading)

## Socket Protocol

We are communicating over [Socket.io](https://socket.io) for realtime scenarios,
as it's much more stable and reliable compared to traditional WebSockets.

- WIP [Socket connection](): Documentation on how to establish an authenticated connection to the server
- WIP [User communication](): Events a user can send/receive to control boats and get data
- WIP [Boat communication](): Events a boat client should implement to work properly
