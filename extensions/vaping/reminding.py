import logging

import aioschedule
from aioschedule import Job
from tortoise.signals import post_save

from bot import main
from extensions.vaping.models import VapingSettings

jobs: dict[int, Job] = {}
logger = logging.getLogger("vaping reminders")


async def notify(user_id: int):
    await main.bot.send_message(user_id, "Не забудь записать затяжки за сегодняшний день!")


def remove_job(user_id: int):
    logger.info(f"Removing job {user_id}")

    try:
        del jobs[user_id]
    except KeyError:
        pass


def set_job(user_id: int, time: str):
    logger.info(f"Created job for user {user_id}")

    jobs[user_id] = aioschedule.every().day.at(time).do(notify, user_id=user_id)


async def create_jobs():
    async for vaping in VapingSettings.all():
        if vaping.vaping_activated and vaping.notifications:
            set_job(vaping.user_id, vaping.notifications_time)


@post_save(VapingSettings)
async def vaping_post_save(sender, instance: VapingSettings, created, using_db, update_fields: list[str]) -> None:
    if update_fields is None:
        return

    if "vaping_activated" in update_fields:
        if instance.vaping_activated:
            set_job(instance.user_id, instance.notifications_time)
        else:
            remove_job(instance.user_id)
    elif "notifications" in update_fields and instance.vaping_activated:
        if instance.notifications:
            set_job(instance.user_id, instance.notifications_time)
        elif not instance.notifications:
            remove_job(instance.user_id)
    elif "notifications_time" in update_fields and instance.notifications and instance.vaping_activated:
        set_job(instance.user_id, instance.notifications_time)
