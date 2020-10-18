# -*- coding: utf-8 -*-


class FbsParserError(Exception):
    pass


class FbsLexerError(FbsParserError):
    pass


class FbsGrammerError(FbsParserError):
    pass
