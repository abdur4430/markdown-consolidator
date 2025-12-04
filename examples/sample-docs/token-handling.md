---
title: Token Handling
modified: 2024-12-02
tags: [security, tokens]
---

# Token Handling

## Overview

This document describes how tokens are handled in our system.

## JWT Structure

Our JWT tokens contain:
- `sub`: User ID
- `roles`: Array of user roles
- `exp`: Expiration timestamp (24 hours from issue)
- `iat`: Issued at timestamp

## Validation

All tokens are validated using:
1. Signature verification (RS256)
2. Expiration check
3. Role-based access control

## Token Expiry

Tokens are valid for 24 hours. After expiry:
- User is redirected to login
- Refresh token can be used (if available)

## Security

- Tokens stored in memory only (not localStorage)
- HTTPS required for all token transmission
- Tokens are rotated on sensitive operations
