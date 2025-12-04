---
title: Authentication Design
created: 2024-12-01
tags: [security, api]
---

# Authentication Design

## Overview

Our API uses JWT tokens for authentication. All requests must include a valid token in the Authorization header.

## Token Structure

The JWT token contains:
- User ID
- Roles/permissions
- Expiration timestamp

## Token Expiry

Tokens expire after 24 hours. Users must re-authenticate to obtain a new token.

## Security Considerations

- Tokens are signed with RS256
- Refresh tokens are stored in HTTP-only cookies
- All endpoints require HTTPS
