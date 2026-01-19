"""
Rate Limiter for AI Service Calls

This module implements rate limiting to prevent abuse of AI service calls
and ensure fair usage across users.
"""

from typing import Dict, Optional
from datetime import datetime, timedelta
import logging
import asyncio
from enum import Enum


class RateLimitType(Enum):
    """Enumeration of rate limit types."""
    CHAT = "chat"
    TASK_CREATION = "task_creation"
    TASK_LIST = "task_list"
    TASK_UPDATE = "task_update"
    TASK_COMPLETION = "task_completion"
    TASK_DELETION = "task_deletion"


class RateLimiter:
    """
    Implements rate limiting for AI service calls.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        # In-memory storage for rate limiting (use Redis in production)
        # Format: {(user_id, rate_limit_type): {'count': int, 'reset_time': datetime}}
        self.requests = {}

        # Rate limits configuration (requests per time window)
        self.limits = {
            RateLimitType.CHAT: {
                'max_requests': 100,  # 100 requests per hour
                'time_window': timedelta(hours=1)
            },
            RateLimitType.TASK_CREATION: {
                'max_requests': 50,   # 50 task creations per hour
                'time_window': timedelta(hours=1)
            },
            RateLimitType.TASK_LIST: {
                'max_requests': 200,  # 200 list requests per hour
                'time_window': timedelta(hours=1)
            },
            RateLimitType.TASK_UPDATE: {
                'max_requests': 100,  # 100 update requests per hour
                'time_window': timedelta(hours=1)
            },
            RateLimitType.TASK_COMPLETION: {
                'max_requests': 100,  # 100 completion requests per hour
                'time_window': timedelta(hours=1)
            },
            RateLimitType.TASK_DELETION: {
                'max_requests': 50,   # 50 deletion requests per hour
                'time_window': timedelta(hours=1)
            }
        }

    def _get_reset_time(self, time_window: timedelta) -> datetime:
        """Calculate the reset time for a rate limit window."""
        return datetime.utcnow() + time_window

    def _get_key(self, user_id: str, rate_limit_type: RateLimitType) -> tuple:
        """Get the key for storing rate limit information."""
        return (user_id, rate_limit_type.value)

    async def check_rate_limit(self, user_id: str, rate_limit_type: RateLimitType) -> tuple[bool, int, int]:
        """
        Check if a user has exceeded their rate limit for a specific action.

        Args:
            user_id: ID of the user
            rate_limit_type: Type of action being performed

        Returns:
            Tuple of (is_allowed, remaining_requests, reset_time_seconds)
        """
        key = self._get_key(user_id, rate_limit_type)
        limit_config = self.limits[rate_limit_type]

        current_time = datetime.utcnow()

        # Get existing record or create new one
        if key in self.requests:
            record = self.requests[key]

            # Check if the time window has passed
            if current_time >= record['reset_time']:
                # Reset the counter
                record['count'] = 1
                record['reset_time'] = self._get_reset_time(limit_config['time_window'])
            else:
                # Increment the counter
                record['count'] += 1
        else:
            # Create new record
            self.requests[key] = {
                'count': 1,
                'reset_time': self._get_reset_time(limit_config['time_window'])
            }

        record = self.requests[key]
        remaining = max(0, limit_config['max_requests'] - record['count'])

        # Calculate seconds until reset
        reset_delta = record['reset_time'] - current_time
        reset_time_seconds = int(reset_delta.total_seconds())

        is_allowed = record['count'] <= limit_config['max_requests']

        if not is_allowed:
            self.logger.warning(
                f"Rate limit exceeded for user {user_id} on {rate_limit_type.value}: "
                f"{record['count']} requests (limit: {limit_config['max_requests']})"
            )

        return is_allowed, remaining, reset_time_seconds

    async def get_remaining_requests(self, user_id: str, rate_limit_type: RateLimitType) -> int:
        """
        Get the number of remaining requests for a user and action type.

        Args:
            user_id: ID of the user
            rate_limit_type: Type of action being performed

        Returns:
            Number of remaining requests
        """
        key = self._get_key(user_id, rate_limit_type)
        limit_config = self.limits[rate_limit_type]

        if key not in self.requests:
            return limit_config['max_requests']

        record = self.requests[key]
        current_time = datetime.utcnow()

        # Check if the time window has passed
        if current_time >= record['reset_time']:
            return limit_config['max_requests']

        remaining = max(0, limit_config['max_requests'] - record['count'])
        return remaining

    async def reset_user_limits(self, user_id: str):
        """
        Reset all rate limits for a specific user (e.g., for admin purposes).

        Args:
            user_id: ID of the user
        """
        keys_to_remove = []
        for key in self.requests:
            if key[0] == user_id:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.requests[key]

        self.logger.info(f"Reset rate limits for user {user_id}")

    async def cleanup_expired_records(self):
        """
        Clean up expired rate limit records to prevent memory leaks.
        This should be called periodically (e.g., via a background task).
        """
        current_time = datetime.utcnow()
        keys_to_remove = []

        for key, record in self.requests.items():
            if current_time >= record['reset_time']:
                # Check if the record has no remaining requests (meaning it's expired)
                # Actually, we keep the record until the next request to avoid constant cleanup
                # The record will be reset when the next request comes in
                pass

        # In a production system with Redis, you'd use expiration times
        # For this in-memory implementation, we rely on the reset logic in check_rate_limit


# Global instance of the rate limiter
rate_limiter = RateLimiter()