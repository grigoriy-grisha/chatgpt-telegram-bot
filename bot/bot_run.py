from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

import config
from bot.agreement import agreementRouter
from bot.gpt import gptRouter
from bot.images import imagesRouter
from bot.payment import paymentsRouter
from bot.start import startRouter
from bot.referral.router import referralRouter


def apply_routers(dp: Dispatcher) -> None:
    dp.include_router(referralRouter)
    dp.include_router(imagesRouter)
    dp.include_router(startRouter)
    dp.include_router(agreementRouter)
    dp.include_router(paymentsRouter)
    dp.include_router(gptRouter)
    


async def bot_run() -> None:
    dp = Dispatcher(storage=MemoryStorage())

    if config.IS_DEV:
        bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

        apply_routers(dp)

        await bot.delete_webhook()
        await dp.start_polling(bot, skip_updates=False, drop_pending_updates=True)
        return

    bot = Bot(
        token=config.TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
        session=AiohttpSession(
            api=TelegramAPIServer.from_base(config.ANALYTICS_URL)
        )
    )

    apply_routers(dp)

    await bot.delete_webhook()
    await dp.start_polling(bot, skip_updates=False, drop_pending_updates=True)
