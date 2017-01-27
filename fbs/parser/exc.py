# -*- coding: utf-8 -*-

from __future__ import absolute_import


class FbsParserError(Exception):
    pass


class FbsLexerError(FbsParserError):
    pass


class FbsGrammerError(FbsParserError):
    pass
