#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : server.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2023/12/3

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apps import api_router, web_router
from starlette.middleware.cors import CORSMiddleware
from common.exceptions import customExceptions
from core.config import settings
from db.cache import registerRedis
from timer import scheduler
from workers import app as celery_app


class InitializeApp(object):
    """
    注册App
    """

    def __new__(cls, *args, **kwargs):
        app = FastAPI(title=settings.PROJECT_NAME)
        # set static files
        app.mount("/media", StaticFiles(directory="media"), name="media")  # 媒体文件
        app.mount("/static", StaticFiles(directory="static"), name="static")  # 静态文件
        app.mount("/web", StaticFiles(directory="templates"), name="templates")  # 模板静态文件
        # allow cross domain
        app.add_middleware(CORSMiddleware, allow_origins=settings.BACKEND_CORS_ORIGINS,
                           allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

        # set redis
        registerRedis(app)
        # set custom exceptions
        customExceptions(app)
        # set timer
        cls.event_init(app)
        # api router
        cls.register_router(app)

        # set socketio
        # app.mount('/', socket_app)

        # print all path
        # for _route in app.routes:
        #     r = _route.__dict__
        #     print(r['path'], r.get('methods', {}))
        # celery_app.worker_main(['-A','workers', 'worker','-l', 'info','-c',' 1'])
        # celery_app.beat_main(['-A','workers', 'beat', '-l', 'INFO'])
        return app

    @staticmethod
    def register_router(app: FastAPI) -> None:
        """
        注册路由
        :param app:
        :return:
        """
        # 项目API
        app.include_router(api_router, prefix="/api/v1")
        # 网页API
        app.include_router(web_router, prefix="")

    @staticmethod
    def event_init(app: FastAPI) -> None:
        """
        事件初始化
        :param app:
        :return:
        """

        @app.on_event("startup")
        async def startup():
            scheduler.start()  # 定时任务
            pass

        @app.on_event('shutdown')
        async def shutdown():
            """
            关闭
            :return:
            """
            # await mysql.close_mysql()
            scheduler.shutdown()