---
title: OAuth Implementation Notes
created: 2024-11-28
tags: [security, oauth]
---

# OAuth Implementation Notes

## JWT Token Handling

We're using JWT tokens for authentication. The token includes user information and permissions.

## Token Expiry

Note: Currently set to 1 hour for testing. Need to increase for production.

## Implementation Details

- Using `jsonwebtoken` library
- RS256 algorithm for signing
- Tokens verified on every request

## Questions

- Should we implement refresh tokens?
- How to handle token revocation?
