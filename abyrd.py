#coding: utf8

class VariableRegex(object):
    def __init__(self, regex, subVariables):
        """RequestVariable class
        Parameters:
            -regex: str
            -subVariables: str tuple list (without index)
        """

        if type(regex)==type('str'):
            self.regex=regex
        else:
            print 'ERROR: failed variable regex init: bad regex'

        if type(subVariables)==type([None,None]):
            self.subVariables=subVariables
        else:
            print 'ERROR: failed variable regex init: bad subvariables'

class RequestVariable(object):
    def __init__(self, variableName, variableRegex, variableQuestion):
        """RequestVariable class
        Parameters:
            -variableName: str
            -variableRegex: VariableRegex
            -variableQuestion: str
        """

        if type(variableName)==type('str'):
            self.variableName=variableName
        else:
            print 'ERROR: failed request variable init: bad name'

        if type(variableRegex)==type(VariableRegex('str', [None])):
            self.variableRegex=variableRegex
        else:
            print 'ERROR: failed request variable init: bad REGEX'

        if type(variableQuestion)==type('str'):
            self.variableQuestion=variableQuestion
        else:
            print 'ERROR: failed request variable init: bad question'


class Request(object):
    def __init__(self, name, idNumber, keywords, code, variables=None):
        """Request class
        Parameters:
            -name: str
            -idNumber: int
            -keywords: int list (without index)
            -code: str
            -variables: RequestVariable list (without index)
            -hasVariables: boolean
        """

        if type(name)==type('str'):
            self.name=name
        else:
            print 'ERROR: failed request init: bad name'

        if type(idNumber)==type(1):
            self.idNumber=idNumber
        else:
            print 'ERROR: failed request init: bad identification number'

        if type(keywords)==type([None,None]):
            self.keywords=keywords
        else:
            print 'ERROR: failed request init: bad keywords'

        if type(code)==type('str'):
            self.code=code
        else:
            print 'ERROR: failed request init: bad code'

        if variables==None:
            self.hasVariables=False
        elif type(variables)==type([None,None]):
            self.variables=variables
            self.hasVariables=True
        else:
            print 'ERROR: failed request init: bad variables'


class RequestsDictionnary(object):
    def __init__(self, requests, keywords, abyme):
        """RequestsDictionnary class
        Parameters:
            -requests: Request() list without index
            -keywords: str tuple list without index
        """
        self.abyme=abyme
        if type(requests)==type([None,None]):
            self.requests=requests
        else:
            print 'ERROR: failed requests dictionnary init: bad requests'
        if type(keywords)==type([None,None]):
            self.keywords=keywords
        else:
            print 'ERROR: failed requests dictionnary init: bad keywords'