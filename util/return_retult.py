#!/usr/bin/env python
# -*- coding:utf-8 -*-


class JsonReturn:

    @staticmethod
    def success(err=0, msg='OK', data=None):
        res = dict(
            err=err,
            msg=msg
        )
        if data:
            res.setdefault('data', data)
        return res

    @staticmethod
    def failure(err=-1, msg='Unknown Error'):
        return dict(
            err=err,
            msg=msg
        )
