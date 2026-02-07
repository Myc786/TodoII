import asyncio
import threading
from datetime import datetime, timedelta
from typing import Dict, List
from sqlmodel import Session, create_engine
from sqlmodel.sql.expression import Select, select
from ..models.reminder import Reminder
from ..models.user import User
from ..database.session import get_session
from ..core.config import DATABASE_URL
from ..core.logging_config import get_logger
import time


class ReminderScheduler:
    """
    Service class for scheduling and sending reminders.
    """

    def __init__(self):
        self.logger = get_logger(__name__)
        self.running = False
        self.scheduler_thread = None
        self.check_interval = 60  # Check every minute for upcoming reminders

    def start_scheduler(self):
        """Start the reminder scheduler in a background thread."""
        if self.running:
            self.logger.warning("Reminder scheduler already running")
            return

        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        self.logger.info("Reminder scheduler started")

    def stop_scheduler(self):
        """Stop the reminder scheduler."""
        self.running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)  # Wait up to 5 seconds for graceful shutdown
        self.logger.info("Reminder scheduler stopped")

    def _scheduler_loop(self):
        """Main scheduler loop that runs in background thread."""
        while self.running:
            try:
                # Process any pending reminders
                self.process_pending_reminders()

                # Sleep for the check interval
                for _ in range(self.check_interval):
                    if not self.running:
                        break
                    time.sleep(1)

            except Exception as e:
                self.logger.error(f"Error in reminder scheduler loop: {e}")
                time.sleep(10)  # Wait 10 seconds before retrying

    def process_pending_reminders(self):
        """Process any pending reminders that should be sent now."""
        try:
            # Connect to the database
            engine = create_engine(DATABASE_URL)

            with Session(engine) as session:
                # Get current time
                current_time = datetime.utcnow()

                # Find all reminders that are due and not yet sent
                statement = select(Reminder).where(
                    Reminder.reminder_time <= current_time,
                    Reminder.sent_at.is_(None)
                )

                reminders = session.exec(statement).all()

                for reminder in reminders:
                    try:
                        # Send the reminder notification
                        self.send_reminder_notification(reminder)

                        # Mark the reminder as sent
                        reminder.sent_at = current_time
                        session.add(reminder)
                        session.commit()

                        self.logger.info(f"Sent reminder for task {reminder.task_id} to user {reminder.user_id}")

                    except Exception as e:
                        self.logger.error(f"Failed to send reminder {reminder.id}: {e}")

        except Exception as e:
            self.logger.error(f"Error processing pending reminders: {e}")

    def send_reminder_notification(self, reminder: Reminder):
        """
        Send a reminder notification based on the reminder type.

        Args:
            reminder: The reminder to send
        """
        # In a real implementation, this would send actual notifications
        # For now, we'll just log the reminder event

        # In a real app, you might:
        # - Send an email if reminder_type includes 'email'
        # - Send a browser notification if reminder_type includes 'browser_notification'
        # - Use a push notification service
        # - Log to a notification queue

        self.logger.info(f"Sending reminder notification - Type: {reminder.reminder_type}, Task: {reminder.task_id}")

    def schedule_reminder(self, reminder: Reminder):
        """
        Schedule a new reminder.

        Args:
            reminder: The reminder to schedule
        """
        # In a real implementation, you might add the reminder to an internal queue
        # or scheduling system. For now, this is handled by the periodic check.
        self.logger.info(f"Scheduled reminder for {reminder.reminder_time} - Task: {reminder.task_id}")


# Global scheduler instance
reminder_scheduler = ReminderScheduler()


def initialize_reminder_scheduler():
    """Initialize and start the reminder scheduler."""
    try:
        reminder_scheduler.start_scheduler()
    except Exception as e:
        get_logger(__name__).error(f"Failed to start reminder scheduler: {e}")


def shutdown_reminder_scheduler():
    """Shut down the reminder scheduler."""
    reminder_scheduler.stop_scheduler()